#!/usr/bin/env bash
# Reproduce every number and figure produced by this public repository (~1 minute, 1 CPU core).
# Add PRACTICE=1 to also run the official qjlb holdout/evaluate practice suite (~5-10 minutes more).
set -euo pipefail
cd "$(dirname "$0")"
python -m pytest -q tests
python scripts/reproduce_adb.py
python scripts/reproduce_wb.py
python scripts/compare_baselines.py
python scripts/make_figures.py
if [[ "${PRACTICE:-0}" == "1" ]]; then ./scripts/practice_suite.sh; fi
