"""Two-country comparison against the official classical baselines.

Runs the unmodified official samplers (`qjlb run`: MC, Sobol QMC, stratified, importance sampling;
10 repeats x 8,192 samples, seed 0) on the five ADB scenarios, and compares their relative RMSE with
the deterministic error of this reference solver. Pass/fail uses the official evaluation-v1
tolerances. Writes results/baseline_comparison.{csv,md} and results/timing.md.
"""
import csv
import subprocess
import sys
import time

import numpy as np
from common import ADB_SCENARIOS, RESULTS, SAMPLER_LABEL, SAMPLERS, SCEN, SHORT, fmt, tolerance

from qjlb.bond import bond_exact
from qjlb.cli import load_model
from jlref.solver import adb_solve
from jlref.two_site import TARGETS

rows, timing = [], []
for s in ADB_SCENARIOS:
    cfg = SCEN / f"{s}.json"
    out_dir = RESULTS / "baseline" / s
    subprocess.run([sys.executable, "-m", "qjlb.cli", "run", "--config", str(cfg), "--output", str(out_dir),
                    "--samples", "8192", "--repeats", "10", "--seed", "0"], check=True, capture_output=True)
    base = {}
    with open(out_dir / "summary.csv") as f:
        for r in csv.DictReader(f):
            base[(r["method"], r["target"])] = r
    times = []
    for _ in range(10):
        t0 = time.perf_counter()
        model, _ = load_model(cfg)
        ours = adb_solve(model)["estimates"]
        times.append(time.perf_counter() - t0)
    ref = bond_exact(model)["estimates"]
    for t in TARGETS:
        exact = ref[t]["estimate"]
        row = dict(scenario=s, target=SHORT[t], exact=exact, exact_fmt=fmt(t, exact),
                   ours_rel_err=abs(ours[t]["estimate"] - exact) / abs(exact),
                   ours_pass=abs(ours[t]["estimate"] - exact) <= tolerance(t, exact))
        for m in SAMPLERS:
            b = base[(m, t)]
            row[f"{m}_rel_rmse"] = float(b["relative_rmse"])
            row[f"{m}_pass"] = float(b["rmse"]) <= tolerance(t, exact)
        rows.append(row)
    timing.append(dict(scenario=s, ours=float(np.median(times)),
                       exact=float(base[("exact", TARGETS[0])]["median_one_off_seconds"]),
                       mc=float(base[("mc", TARGETS[0])]["median_one_off_seconds"]),
                       importance=float(base[("importance", TARGETS[0])]["median_one_off_seconds"])))

with open(RESULTS / "baseline_comparison.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]))
    w.writeheader()
    w.writerows(rows)

hdr = "| Scenario | Target | Exact (qjlb) | This solver: rel. error | " + " | ".join(SAMPLER_LABEL[m] for m in SAMPLERS) + " |"
lines = [hdr, "|---|---|---:|---:|" + "---:|" * len(SAMPLERS)]
for r in rows:
    cells = [f"{r[m + '_rel_rmse']:.1%}{'' if r[m + '_pass'] else ' ✗'}" for m in SAMPLERS]
    lines.append(f"| {r['scenario']} | {r['target']} | {r['exact_fmt']} | {r['ours_rel_err']:.0e} | " + " | ".join(cells) + " |")
lines += ["", "Sampler cells: relative RMSE over 10 repeats x 8,192 samples (seed 0); ✗ = outside the official "
          "evaluation-v1 tolerance. This solver is deterministic; its cell is the relative error vs the official exact value."]
(RESULTS / "baseline_comparison.md").write_text("\n".join(lines) + "\n")

tl = ["| Scenario | This solver | Official exact | MC | IS |", "|---|---:|---:|---:|---:|"]
tl += [f"| {t['scenario']} | {t['ours'] * 1e3:.1f} ms | {t['exact'] * 1e3:.1f} ms | {t['mc'] * 1e3:.1f} ms | "
       f"{t['importance'] * 1e3:.1f} ms |" for t in timing]
tl += ["", "Median wall time including model load (this solver: 10 in-process runs; others: `qjlb run` "
       "median_one_off_seconds). Parity with the official exact solver; no speed-up is claimed."]
(RESULTS / "timing.md").write_text("\n".join(tl) + "\n")

ours_all = all(r["ours_pass"] for r in rows)
fails = {m: sum(not r[m + "_pass"] for r in rows) for m in SAMPLERS}
exh = [r for r in rows if r["target"] == "P(both exhausted)"]
print(f"This solver passes {sum(r['ours_pass'] for r in rows)}/{len(rows)} targets.")
print("Official samplers failing (of 25): " + ", ".join(f"{SAMPLER_LABEL[m]} {fails[m]}" for m in SAMPLERS))
print(f"P(both exhausted): samplers passing in {sum(any(r[m + '_pass'] for m in SAMPLERS) for r in exh)}/5 scenarios")
sys.exit(0 if ours_all else 1)
