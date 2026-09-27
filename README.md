# Systemic Tail Episode Risk (STER / CSTER)

**A path-dependent framework for _synchronized_, _persistent_ extreme-loss episodes across markets.**

Niraj Neupane, CA (ICAI) — Quantitative Researcher, Korvane; Financial Economist, Calderyn Institute
ORCID: 0009-0003-7026-7026

![Status](https://img.shields.io/badge/Status-Working%20Paper-orange)
![Domain](https://img.shields.io/badge/Domain-Systemic%20Risk-1f6feb)
![Code](https://img.shields.io/badge/Code-Python-3776ab)
![License](https://img.shields.io/badge/License-MIT-green)

---

## What this is

This repository accompanies the **multivariate extension** of Tail Episode Risk (TER) and Conditional Tail
Episode Risk (CTER). The univariate framework — introduced in the companion paper *Conditional Tail Episode
Risk: A Path-Dependent Framework for Extreme-Loss Episodes Beyond Value-at-Risk and Expected Shortfall*
([repo](https://github.com/nirajneupane17/conditional-tail-episode-risk)) — measures the worst *sustained*
tail episode in **one** series. This project extends it to the question that the univariate measure cannot
answer: **how severe is the worst episode of _synchronized, persistent_ stress across _several_ markets?**

**Systemic Tail Episode Risk (STER)** is the conditional upper-tail quantile of the worst contiguous,
breadth-gated, cross-asset threshold-exceedance episode over a forecast horizon; **CSTER** is its conditional
(probability × severity) extension.

> **What existing systemic measures do vs. what STER adds.** CoVaR, marginal expected shortfall / SRISK, and
> co-exceedances quantify the *magnitude of contemporaneous joint tail stress*; spillover-persistence
> statistics measure the *timing* of transmission. STER targets a different object — the *persistence and
> cumulative severity of a synchronized stress episode* — which the point-in-time measures, by construction,
> cannot see (Proposition 3).

## Honest scope

- **Established here (real, reproducible):** the STER object and its properties (reduction to TER,
  breadth-monotonicity, separation from point-in-time measures), a simulation showing STER rises with
  cross-asset tail dependence while portfolio VaR/ES stay flat, and an empirical demonstration that realized
  STER isolates the broad historical crises.
- **Specified, not yet run:** the CSTER **forecasting** evaluation. As in the companion paper we separate
  *measure innovation* from *forecasting performance*; the conditional-forecasting empirics are specified in
  the paper and left to companion work. Given the rarity of systemic episodes we do **not** anticipate a
  large incremental forecasting gain, and will report it honestly whatever it shows.
- The object is a **multivariate max cluster functional** (Basrak & Segers, 2009); novelty is claimed in the
  financial, conditional, breadth-gated formulation, **not** in the underlying functional.

## The object

For assets `i = 1..d` with per-asset tail thresholds `q_i` (trailing (1−α)-quantiles), at each step define
breadth `b = #{i : L_i > q_i}` and weighted cross-asset excess `c = Σ_i w_i (L_i − q_i)₊`. A **systemic
episode** is a contiguous run with `b ≥ κ`; its severity is the cumulative `c` over the run; and

```
S^sys*        = max over systemic episodes of their cumulative severity
STER_{α,β,H,t} = Q_β( S^sys*  | F_t )
CSTER          = P(systemic episode | X) · ES_β( S^sys* | systemic episode, X, Z )
```

## Key results (reproducible)

**Simulation — STER rises with cross-asset tail dependence, portfolio VaR/ES do not** (`results/simulation.csv`):

| tail dep. λ | Portfolio VaR95 | Portfolio ES95 | STER95 | STER99 |
| --- | --- | --- | --- | --- |
| 0.000 | 1.108 | 1.399 | 0.424 | 0.685 |
| 0.109 | 1.103 | 1.437 | 0.513 | 0.846 |
| 0.238 | 1.081 | 1.448 | 0.592 | 0.991 |

STER99 rises ≈45% as λ goes 0→0.24 while portfolio VaR95 is unchanged — the cross-sectional analogue of
TER's response to serial dependence.

**Empirical — realized STER flags the broad, sustained crises** (`results/ster_episodes.csv`, 5 markets, 2002–2026):

| Episode | S^sys* (%) |
| --- | --- |
| Mar 2020 (COVID) | 8.34 |
| Sep 2008 (Lehman / GFC) | 6.18 |
| Apr 2025 (selloff) | 3.59 |
| Aug 2015 (China / global selloff) | 2.58 |
| Jun 2016 (Brexit) | 1.81 |

**Theory checks** (`results/theory_checks.txt`): separation (STER 6 vs 2 on marginally-identical paths),
breadth-monotonicity (0/5000 violations), reduction to TER (0/5000 mismatches).

## Repository structure

```
├── README.md
├── LICENSE  requirements.txt  CITATION.cff  .gitignore
├── data/                 # daily log returns, 2000–2026 (same source as the CTER repo)
│   ├── returns_{sp500,nasdaq,tlt_bonds,eurusd,usdjpy,btc}.csv
│   ├── stress_{vix,nfci,stlfsi}.csv     # for optional CSTER conditioning
│   └── README.md
├── src/
│   ├── lib_ster.py       # STER object: breadth-gated systemic episode severity
│   ├── 01_simulation.py  # tail-dependence simulation      -> results/simulation.csv, figures/simulation.*
│   ├── 02_empirical.py   # realized STER crisis identification -> results/ster_episodes.csv, figures/episodes.*
│   └── 03_theory_checks.py  # numerical verification of Propositions 1–3
├── results/              # committed outputs used in the paper
├── figures/              # simulation.pdf/png, episodes.pdf/png
└── paper/                # STER_paper.pdf, .tex
```

## Reproduce

```bash
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/01_simulation.py     # simulation table + figure
python src/02_empirical.py      # crisis-identification table + figure
python src/03_theory_checks.py  # verify the three propositions
```

All stochastic components use `SEED = 0` (`src/lib_ster.py`); the empirical analysis is deterministic. The
committed files under `results/` are those reported in the paper.

## Data

Six daily log-return series spanning 2000–2026 (TLT from 2002, Bitcoin from 2014), plus three stress
indicators (VIX daily; NFCI, STLFSI weekly, carried forward) — the same source data as the CTER repo. The
empirical STER analysis uses the five markets that span the 2008 crisis (S&P 500, Nasdaq, TLT, EUR/USD,
USD/JPY) on their common 2002–2026 sample. See `data/README.md`.

## Citation

```bibtex
@article{neupane2026ster,
  author  = {Neupane, Niraj},
  title   = {Systemic Tail Episode Risk: Persistence and Cumulative Severity of
             Synchronized Extreme-Loss Episodes Across Markets},
  year    = {2026},
  note    = {Working Paper; multivariate extension of Conditional Tail Episode Risk (TER/CTER)}
}
```

## Disclaimer

Academic research only; not investment, trading, or risk-management advice. Historical and simulated results
do not guarantee future performance. Code is MIT-licensed; raw third-party market data may be subject to the
original providers' terms.
