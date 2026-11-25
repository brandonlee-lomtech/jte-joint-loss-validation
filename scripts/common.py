import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
BENCH = ROOT / "vendor" / "qjlb-benchmark"
SCEN = BENCH / "scenarios"
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
ADB_SCENARIOS = ["adb-base", "adb-independent", "adb-common-shock", "adb-rain-stress", "adb-rain-cover"]
WB_SCENARIOS = ["kaz-kgz-base", "tjk-uzb-base"]
SAMPLERS = ["mc", "qmc", "stratified", "importance"]
SAMPLER_LABEL = {"mc": "MC", "qmc": "Sobol", "stratified": "Strat.", "importance": "IS"}
SHORT = {
    "term_expected_principal_loss_usd": "E[L]",
    "term_joint_attachment_probability": "P(joint attach)",
    "term_portfolio_loss_exceedance_probability": "P(L>80m)",
    "term_portfolio_stop_loss_usd": "Stop-loss",
    "term_both_bonds_exhausted_probability": "P(both exhausted)",
}


def tolerance(target, ref, principal=160e6):
    """Official evaluation-v1 tolerance (vendor/qjlb-benchmark/EVALUATION.md); P = USD 160m."""
    rel, absf = {
        "term_expected_principal_loss_usd": (0.01, 1e-4 * principal),
        "term_joint_attachment_probability": (0.05, 1e-4),
        "term_portfolio_loss_exceedance_probability": (0.05, 1e-4),
        "term_portfolio_stop_loss_usd": (0.05, 1e-5 * principal),
        "term_both_bonds_exhausted_probability": (0.10, 1e-6),
    }[target]
    return max(rel * abs(ref), absf)


def fmt(target, v):
    if target.endswith("_usd"):
        return f"{v / 1e6:.3f}m"
    return f"{v:.4%}" if v >= 1e-3 else f"{v:.3e}"


def dump(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, default=float) + "\n")
