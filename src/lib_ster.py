"""
Systemic Tail Episode Risk (STER) -- core library.

STER extends univariate Tail Episode Risk (TER) to the cross-market setting: it is
the conditional upper-tail quantile of the worst contiguous, breadth-gated,
cross-asset threshold-exceedance episode over a forecast horizon.

Companion paper: Neupane, N. (2026). Conditional Tail Episode Risk (TER/CTER).
This repo accompanies the multivariate extension (STER/CSTER).
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
SEED = 0

# assets that span the 2008 crisis (common sample from 2002) -- used for empirics
ASSETS_2008 = ["sp500", "nasdaq", "tlt_bonds", "eurusd", "usdjpy"]


def load(asset):
    df = pd.read_csv(DATA / f"returns_{asset}.csv", parse_dates=["date"]).dropna()
    return df.rename(columns={"logret": asset})[["date", asset]]


def load_panel(assets):
    """Inner-join returns of `assets` on common dates; return (dates, loss matrix L)."""
    m = load(assets[0])
    for a in assets[1:]:
        m = m.merge(load(a), on="date", how="inner")
    m = m.sort_values("date").reset_index(drop=True)
    L = -m[assets].values                      # losses = -log returns
    return pd.to_datetime(m["date"].values), L


def worst_systemic_episode(Lwin, q, kappa, w):
    """Worst breadth-gated cross-asset episode severity in a window.

    Lwin : (H, d) losses over the horizon.
    q    : (d,)   per-asset tail thresholds (fixed at the forecast origin).
    kappa: breadth gate -- a step is 'systemic' iff at least kappa assets exceed.
    w    : (d,)   portfolio weights.
    Returns S^sys* : severity of the worst contiguous systemic run (0 if none).
    """
    exc = np.clip(Lwin - q, 0.0, None)                       # (H, d) excesses
    breadth = (Lwin > q).sum(axis=1)                         # (H,)
    step = (exc * w).sum(axis=1) * (breadth >= kappa)        # 0 unless systemic
    best = cur = 0.0
    for s, sys in zip(step, breadth >= kappa):
        cur = cur + s if sys else 0.0
        best = max(best, cur)
    return best
