"""Official-interface solver (qjlb `run_solver` signature: solve(model, samples, seed))."""
from __future__ import annotations

import numpy as np
from qjlb.bond import BondModel, result
from qjlb.model import ELTModel, entries

from . import elt, two_site


def adb_solve(model, samples=0, seed=0):
    """ADB two-country track: exact two-site MPS contraction (deterministic)."""
    if not isinstance(model, BondModel):
        raise TypeError("adb_solve handles the ADB adb_drb track")
    annual = two_site.annual_mps(model)
    term = two_site.term_mps(annual, model.dimension)
    t = two_site.targets(term, model.eq_limit, model.rain_limit, model.threshold)
    values = np.array([t[k] for k in two_site.TARGETS])
    out = result(model, values, None, "jlref_two_site_mps_exact", 0,
                 annual_bond_dimension=two_site.bond_dimension(annual),
                 term_bond_dimension=two_site.bond_dimension(term))
    out["uncertainty"] = ("Deterministic exact contraction (two-site MPS, exact SVD up to 1e-14 relative "
                          "noise); floating-point error only.")
    return out


def elt_solve(model, samples=0, seed=0):
    values = elt.elt_targets(model)
    est = entries(values, None, metric_names=model.metric_names)
    for item in est.values():
        item.update(standard_error=0.0, ci95_low=item["estimate"], ci95_high=item["estimate"])
    return {
        "estimates": est,
        "resources": {"method": "jlref_elt_exact_vectorised", "model_evaluations": model.state_count,
                      "samples": 0, "execution": "classical_cpu"},
        "uncertainty": "Exact vectorised sum over catalogue rows; floating-point error only.",
    }


def solve(model, samples=0, seed=0):
    """Dispatch: ADB adb_drb -> two-site MPS; World Bank ELT -> exact vectorised pass."""
    if isinstance(model, ELTModel):
        return elt_solve(model, samples, seed)
    return adb_solve(model, samples, seed)
