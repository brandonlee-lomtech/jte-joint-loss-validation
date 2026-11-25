"""Reproduce all 25 official ADB targets (5 scenarios x 5 targets) by exact two-site MPS contraction.

Writes official-format submission files to results/adb/<scenario>.json, validates each with
`qjlb validate --rtol 1e-9`, and writes results/adb_targets.{csv,md}.
Exit code is non-zero if any target misses the official exact value by more than 1e-9 relative.
"""
import csv
import subprocess
import sys
import time

from common import ADB_SCENARIOS, RESULTS, SCEN, SHORT, dump, fmt

from qjlb.bond import bond_exact
from qjlb.cli import load_model
from qjlb.validation import make_submission
from jlref.solver import adb_solve
from jlref.two_site import TARGETS

rows, worst, validate_ok = [], 0.0, True
for s in ADB_SCENARIOS:
    cfg = SCEN / f"{s}.json"
    runs = []  # (elapsed incl. load, preparation) per run; report the median-time run
    for _ in range(10):
        t0 = time.perf_counter()
        model, prep = load_model(cfg)
        out = adb_solve(model)
        runs.append((time.perf_counter() - t0, prep))
    elapsed, prep = sorted(runs)[len(runs) // 2]
    ref = bond_exact(model)["estimates"]
    sub = make_submission(model, out, out["resources"]["method"], elapsed, prep)
    path = RESULTS / "adb" / f"{s}.json"
    dump(path, sub)
    v = subprocess.run([sys.executable, "-m", "qjlb.cli", "validate", str(path), "--config", str(cfg),
                        "--rtol", "1e-9", "--output", str(RESULTS / "adb" / "validation" / s)],
                       capture_output=True, text=True)
    validate_ok &= v.returncode == 0
    for t in TARGETS:
        exact, ours = ref[t]["estimate"], sub["estimates"][t]
        rel = abs(ours - exact) / abs(exact)
        worst = max(worst, rel)
        rows.append(dict(scenario=s, target=t, short=SHORT[t], official_exact=exact, ours=ours, rel_error=rel,
                         annual_bond=out["resources"]["annual_bond_dimension"],
                         term_bond=out["resources"]["term_bond_dimension"]))
    print(f"{s:17s} qjlb validate exit={v.returncode}  bond(annual/term)={rows[-1]['annual_bond']}/{rows[-1]['term_bond']}")

with open(RESULTS / "adb_targets.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)

lines = ["| Scenario | Target | Official exact (qjlb) | This solver | Rel. error |", "|---|---|---:|---:|---:|"]
lines += [f"| {r['scenario']} | {r['short']} | {fmt(r['target'], r['official_exact'])} | "
          f"{fmt(r['target'], r['ours'])} | {r['rel_error']:.0e} |" for r in rows]
(RESULTS / "adb_targets.md").write_text("\n".join(lines) + "\n")

n_ok = sum(r["rel_error"] <= 1e-9 for r in rows)
print(f"\n{n_ok}/{len(rows)} official ADB targets reproduced (max relative error {worst:.1e}); "
      f"qjlb validate: {'all passed' if validate_ok else 'FAILED'}")
sys.exit(0 if n_ok == len(rows) and validate_ok else 1)
