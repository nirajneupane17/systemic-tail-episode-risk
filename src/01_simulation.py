"""
01 -- Cross-asset tail-dependence simulation.

Tests whether STER responds to CROSS-ASSET TAIL DEPENDENCE when marginals and
linear correlation are held fixed (the cross-sectional analogue of TER's response
to serial dependence). Tail dependence is isolated via the t-copula degrees of
freedom nu: small nu = strong joint extremes; large nu -> Gaussian = weak. Margins
are standard normal (fixed) and linear correlation rho is fixed, so only tail
dependence varies. Portfolio VaR/ES are computed on the equal-weight portfolio.

Outputs: results/simulation.csv, figures/simulation.{pdf,png}
Run: python src/01_simulation.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np, pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from lib_ster import RESULTS, FIGURES, SEED, worst_systemic_episode

RNG = np.random.default_rng(SEED)
d, RHO, H, KAPPA, P, N = 6, 0.35, 10, 2, 0.05, 60000
W = np.ones(d) / d
NUS = [50, 12, 6, 4, 3]
C = ["#1b263b", "#415a77", "#778da9", "#b08968"]
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False,
                     "font.family": "serif", "figure.dpi": 150})


def t_copula_normal_margins(n, nu):
    """t-copula with N(0,1) margins: fixed marginals, fixed linear correlation, tail-dep via nu."""
    Cc = (1 - RHO) * np.eye(d) + RHO * np.ones((d, d))
    z = RNG.standard_normal((n, d)) @ np.linalg.cholesky(Cc).T
    g = RNG.chisquare(nu, size=(n, 1))
    u = stats.t.cdf(z * np.sqrt(nu / g), df=nu)
    return stats.norm.ppf(np.clip(u, 1e-9, 1 - 1e-9))


def run_nu(nu):
    X = t_copula_normal_margins(N + H, nu)
    q = np.quantile(X, 1 - P, axis=0)
    port = X @ W
    pv = np.quantile(port, 1 - P); pe = port[port >= pv].mean()
    S = np.array([worst_systemic_episode(X[i:i + H], q, KAPPA, W) for i in range(N)])
    lam = 2 * stats.t.cdf(-np.sqrt((nu + 1) * (1 - RHO) / (1 + RHO)), df=nu + 1)  # t-copula upper tail dep
    return dict(nu=nu, taildep=round(float(lam), 3), portVaR95=round(float(pv), 3),
                portES95=round(float(pe), 3), STER95=round(float(np.quantile(S, 0.95)), 3),
                STER99=round(float(np.quantile(S, 0.99)), 3))


def main():
    R = pd.DataFrame([run_nu(nu) for nu in NUS])
    R.to_csv(RESULTS / "simulation.csv", index=False)
    print(R.to_string(index=False))
    fig, ax = plt.subplots(figsize=(5.2, 3.4))
    ax.plot(R.taildep, R.portVaR95, "o-", c=C[2], label="Portfolio VaR 95%")
    ax.plot(R.taildep, R.portES95, "s-", c=C[1], label="Portfolio ES 95%")
    ax.plot(R.taildep, R.STER95, "^--", c=C[3], label="STER 95%")
    ax.plot(R.taildep, R.STER99, "D-", c=C[0], label="STER 99%")
    ax.set_xlabel(r"cross-asset upper tail dependence $\lambda$"); ax.set_ylabel("risk (std units)")
    ax.legend(frameon=False, fontsize=8)
    ax.set_title("STER rises with cross-asset tail dependence;\nportfolio VaR/ES do not")
    plt.tight_layout()
    plt.savefig(FIGURES / "simulation.pdf"); plt.savefig(FIGURES / "simulation.png", dpi=300)
    print("\nSaved -> results/simulation.csv, figures/simulation.{pdf,png}")


if __name__ == "__main__":
    main()
