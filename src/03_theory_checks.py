"""
03 -- Numerical verification of the theoretical propositions.

Confirms, by construction, the three propositions in the paper:
  Prop 1 (Reduction):  d=1 => STER = TER.
  Prop 2 (Breadth monotonicity): S^sys* is non-increasing in kappa.
  Prop 3 (Separation): paths that are temporal reorderings of one another share
      per-asset and portfolio marginals and co-exceedance counts (hence identical
      portfolio VaR/ES, CoVaR, MES) yet differ in STER.

Output: results/theory_checks.txt
Run: python src/03_theory_checks.py
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
from lib_ster import RESULTS, SEED, worst_systemic_episode

out = []


def log(x):
    print(x); out.append(str(x))


# ---- Prop 3: separation ----
q = np.array([2., 2.]); w = np.array([.5, .5]); kappa = 2
A = np.array([[4, 4], [4, 4], [4, 4], [0, 0], [0, 0], [0, 0]], float)
B = np.array([[4, 4], [0, 0], [4, 4], [0, 0], [4, 4], [0, 0]], float)
coexc = lambda p: int(((p > q).sum(1) >= 2).sum())
portmarg = lambda p: sorted((p @ w).round(3))
log("Prop 3 (Separation):")
log(f"  A,B are reorderings of the same daily vectors : {sorted(map(tuple,A))==sorted(map(tuple,B))}")
log(f"  co-exceedance count           A={coexc(A)}  B={coexc(B)}  (equal)")
log(f"  portfolio marginal identical  : {portmarg(A)==portmarg(B)}  (=> equal portfolio VaR/ES, CoVaR, MES)")
log(f"  STER                          A={worst_systemic_episode(A,q,kappa,w)}  "
    f"B={worst_systemic_episode(B,q,kappa,w)}  (DIFFERENT => STER separates)")

# ---- Prop 2: breadth monotonicity ----
rng = np.random.default_rng(SEED + 1); d = 5; w5 = np.ones(d) / d; q5 = np.full(d, 2.)
viol = 0
for _ in range(5000):
    path = np.abs(rng.standard_normal((10, d))) * 1.5 + rng.binomial(1, 0.15, (10, d)) * 3
    vals = [worst_systemic_episode(path, q5, k, w5) for k in [1, 2, 3, 4, 5]]
    if any(vals[i] < vals[i + 1] - 1e-12 for i in range(4)):
        viol += 1
log("\nProp 2 (Breadth monotonicity):")
log(f"  STER non-increasing in kappa : violations in {viol}/5000 random paths")

# ---- Prop 1: reduction to TER ----
rng = np.random.default_rng(SEED + 2); mism = 0
for _ in range(5000):
    L1 = np.abs(rng.standard_normal((10, 1))) * 1.5 + rng.binomial(1, 0.2, (10, 1)) * 3
    q1 = np.array([2.0])
    ster1 = worst_systemic_episode(L1, q1, 1, np.array([1.0]))
    # univariate TER worst-episode severity (single series)
    exc = np.clip(L1[:, 0] - 2.0, 0, None); over = L1[:, 0] > 2.0
    best = cur = 0.0
    for e, o in zip(exc, over):
        cur = cur + e if o else 0.0; best = max(best, cur)
    if abs(ster1 - best) > 1e-12:
        mism += 1
log("\nProp 1 (Reduction to TER):")
log(f"  d=1 STER == univariate TER   : mismatches in {mism}/5000 random paths")

(RESULTS / "theory_checks.txt").write_text("\n".join(out) + "\n")
log("\nSaved -> results/theory_checks.txt")
