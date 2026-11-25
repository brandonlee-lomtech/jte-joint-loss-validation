"""Team solver entry point for `qjlb evaluate` (execution: classical_cpu)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from qjlb.worker import run_solver  # noqa: E402
from jlref.solver import solve  # noqa: E402

if __name__ == "__main__":
    run_solver(solve)
