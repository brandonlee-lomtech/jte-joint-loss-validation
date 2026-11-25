"""World Bank ELT public scenarios: exact vectorised pass vs the official exact solver."""
import csv
import sys

from common import RESULTS, SCEN, WB_SCENARIOS

from qjlb.model import ELTModel, elt_exact
from jlref.solver import solve

rows = []
for s in WB_SCENARIOS:
    m = ELTModel.load(SCEN / f"{s}.json")
    ref, got = elt_exact(m)["estimates"], solve(m)["estimates"]
    for k in ref:
        e, o = ref[k]["estimate"], got[k]["estimate"]
        rows.append(dict(scenario=s, target=k, official_exact=e, ours=o, rel_error=abs(o - e) / max(abs(e), 1e-300)))
with open(RESULTS / "wb_targets.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)
worst = max(r["rel_error"] for r in rows)
print(f"{len(rows)} World Bank targets, max relative error vs official exact {worst:.1e}")
sys.exit(0 if worst <= 1e-10 else 1)
