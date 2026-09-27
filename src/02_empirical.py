"""
02 -- Realized systemic tail-episode severity on real data.

Computes realized S^sys* on five markets that span the 2008 crisis (S&P 500,
Nasdaq, TLT, EUR/USD, USD/JPY), daily 2002-2026, and lists the worst distinct
systemic episodes -- the economic reality check that STER isolates broad,
sustained crises.

Outputs: results/ster_episodes.csv, figures/episodes.{pdf,png}
Run: python src/02_empirical.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from lib_ster import RESULTS, FIGURES, ASSETS_2008, load_panel, worst_systemic_episode

W_WIN, H, P, KAPPA = 1250, 10, 0.05, 2
C = ["#1b263b", "#415a77", "#778da9"]
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "font.family": "serif", "figure.dpi": 150})


def main():
    dates, L = load_panel(ASSETS_2008)
    n, d = L.shape
    w = np.ones(d) / d
    print(f"common sample: {dates[0].date()} to {dates[-1].date()}, n={n}, d={d}")
    sev = np.full(n, np.nan)
    for t in range(W_WIN, n - H):
        q = np.quantile(L[t - W_WIN:t], 1 - P, axis=0)
        sev[t] = worst_systemic_episode(L[t + 1:t + 1 + H], q, KAPPA, w)
    s = pd.Series(sev * 100, index=dates)

    # worst distinct episodes (dedup within 30 days)
    top = s.dropna().sort_values(ascending=False)
    picked, used = [], []
    for dt, val in top.items():
        if all(abs((dt - u).days) > 30 for u in used):
            picked.append((dt.date(), round(float(val), 3))); used.append(dt)
        if len(picked) >= 8:
            break
    ep = pd.DataFrame(picked, columns=["date", "S_sys_star_pct"])
    ep.to_csv(RESULTS / "ster_episodes.csv", index=False)
    print("\nWorst distinct systemic episodes:\n", ep.to_string(index=False))

    fig, ax = plt.subplots(figsize=(7.2, 3.2))
    ax.fill_between(s.index, s.values, color=C[2], alpha=0.5)
    ax.plot(s.index, s.values, lw=0.5, c=C[1])
    for lbl, dt in [("2008", "2008-09-29"), ("2020", "2020-03-04"), ("2025", "2025-04-02")]:
        d0 = pd.Timestamp(dt)
        ax.annotate(lbl, (d0, s.asof(d0)), fontsize=7, ha="center", va="bottom", c=C[0])
    ax.set_ylabel(r"systemic episode severity $S^{\mathrm{sys}*}$ (%)")
    ax.set_title("Realized systemic tail-episode severity, 2002-2026 (5 markets)")
    plt.tight_layout()
    plt.savefig(FIGURES / "episodes.pdf"); plt.savefig(FIGURES / "episodes.png", dpi=300)
    print("\nSaved -> results/ster_episodes.csv, figures/episodes.{pdf,png}")


if __name__ == "__main__":
    main()
