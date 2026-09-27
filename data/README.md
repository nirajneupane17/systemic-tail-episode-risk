# Data

Daily log-return series (2000–2026) and stress indicators — same source as the CTER repo.

| File | Rows | Start | End |
| --- | --- | --- | --- |
| `returns_sp500.csv` | 6,717 | 2000-01-04 | 2026-09-18 |
| `returns_nasdaq.csv` | 6,717 | 2000-01-04 | 2026-09-18 |
| `returns_tlt_bonds.csv` | 6,073 | 2002-07-31 | 2026-09-18 |
| `returns_eurusd.csv` | 6,692 | 2000-01-04 | 2026-09-11 |
| `returns_usdjpy.csv` | 6,692 | 2000-01-04 | 2026-09-11 |
| `returns_btc.csv` | 4,386 | 2014-09-18 | 2026-09-20 |
| `stress_vix.csv` / `stress_nfci.csv` / `stress_stlfsi.csv` | — | — | — |

**Columns:** `date`, `logret` (daily log return). Losses used throughout are `L = -logret`.

The empirical STER analysis (`src/02_empirical.py`) uses the five markets spanning the 2008 crisis (S&P 500, Nasdaq, TLT, EUR/USD, USD/JPY) on their common 2002–2026 sample. VIX is daily; NFCI and STLFSI are weekly and would be carried forward (LOCF) for any CSTER conditioning.

Raw third-party market data may be subject to the original providers' licensing terms.
