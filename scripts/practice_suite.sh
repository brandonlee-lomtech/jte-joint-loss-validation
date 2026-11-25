#!/usr/bin/env bash
# Official holdout harness on a 6-case practice suite (3 ADB + 3 World Bank cases).
# Uses the unmodified official `qjlb holdout` / `qjlb evaluate` commands. ~5-10 minutes on 1 core.
# SEED is our public practice seed; the official evaluation uses ADB's own seed.
set -euo pipefail
cd "$(dirname "$0")/.."
SEED="${SEED:-20261125}"
rm -rf practice-suite
qjlb holdout --output practice-suite/suite --data vendor/qjlb-benchmark/data --cases 6 --seed "$SEED"
qjlb evaluate practice-suite/suite --output practice-suite/report \
  --execution classical_cpu --trusted-code -- python "$PWD/team_solver.py"
cp practice-suite/report/summary.csv results/practice_suite_summary.csv
python - <<'PY'
import csv
rows = [r for r in csv.DictReader(open("results/practice_suite_summary.csv")) if r["method"] == "team"]
ok = sum(r["accuracy_pass"] == "True" for r in rows)
print(f"team solver: {ok}/{len(rows)} practice cases pass")
raise SystemExit(0 if ok == len(rows) == 6 else 1)
PY
