"""Tests for the public reference solver: it must reproduce the official exact references."""
import copy
import json
import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from qjlb.bond import BondModel, bond_exact  # noqa: E402
from qjlb.model import ELTModel, elt_exact  # noqa: E402
from jlref import two_site  # noqa: E402
from jlref.solver import adb_solve, solve  # noqa: E402

SCEN = ROOT / "vendor" / "qjlb-benchmark" / "scenarios"
TERMS = ROOT / "vendor" / "qjlb-benchmark" / "data" / "adb_terms.json"
ADB = ["adb-base", "adb-independent", "adb-common-shock", "adb-rain-stress", "adb-rain-cover"]


@pytest.mark.parametrize("name", ADB)
def test_all_official_adb_targets(name):
    m = BondModel.load(SCEN / f"{name}.json")
    ref = bond_exact(m)["estimates"]
    got = adb_solve(m)["estimates"]
    for k in two_site.TARGETS:
        assert got[k]["estimate"] == pytest.approx(ref[k]["estimate"], rel=1e-9, abs=1e-15)


@pytest.mark.parametrize("years", [1, 10])
def test_other_horizons_and_cent_limits(years):
    c = json.loads((SCEN / "adb-base.json").read_text())
    c["term_years"] = years
    c["earthquake_sublimit_usd"] = [51234567.89, 70000000.0]
    m = BondModel(copy.deepcopy(c), TERMS)
    ref = bond_exact(m)["estimates"]
    got = adb_solve(m)["estimates"]
    for k in two_site.TARGETS:
        assert got[k]["estimate"] == pytest.approx(ref[k]["estimate"], rel=1e-8, abs=1e-15)


def test_split_merge_is_exact():
    m = BondModel.load(SCEN / "adb-base.json")
    p = two_site.annual_matrix(m)
    assert np.abs(two_site.merge(two_site.split(p)) - p).max() < 1e-15


def test_independent_scenario_has_bond_one():
    m = BondModel.load(SCEN / "adb-independent.json")
    assert two_site.bond_dimension(two_site.annual_mps(m)) == 1
    assert adb_solve(m)["resources"]["term_bond_dimension"] == 1


def test_dependent_scenario_has_bond_above_one():
    m = BondModel.load(SCEN / "adb-base.json")
    assert two_site.bond_dimension(two_site.annual_mps(m)) > 1


@pytest.mark.parametrize("name", ["kaz-kgz-base", "tjk-uzb-base"])
def test_world_bank_elt_matches_official(name):
    m = ELTModel.load(SCEN / f"{name}.json")
    ref, got = elt_exact(m)["estimates"], solve(m)["estimates"]
    assert set(ref) == set(got)
    for k in ref:
        assert got[k]["estimate"] == pytest.approx(ref[k]["estimate"], rel=1e-10, abs=1e-12)


def test_output_is_labelled_classical_cpu():
    m = BondModel.load(SCEN / "adb-base.json")
    assert adb_solve(m)["resources"]["execution"] == "classical_cpu"
