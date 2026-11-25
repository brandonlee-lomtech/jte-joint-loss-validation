"""Exact two-site MPS (tensor-train) contraction of the official ADB two-country model.

Representation
--------------
Each country is one site with local state ``s = 2*e + r``:
``e`` in 0..4 is the earthquake payout level (quarter steps of the earthquake
sub-limit) and ``r`` in {0, 1} is the precipitation trigger, so the local dimension
is d = 10. The official annual law over 100 joint states is a 10 x 10 matrix
``P[s_KGZ, s_TJK]``. Its exact SVD gives two MPS cores::

    P = A[:, s1, :] @ B[:, s2, :]        A: (1, d, chi), B: (chi, d, 1)

where chi = rank(P) <= 10. chi = 1 means the two countries are independent.

Term law
--------
Over a Y-year term the per-country state accumulates and is capped
(``e <- min(e + e', 4)``, ``r <- min(r + r', 1)``). Because years are independent,
the term law is a Y-fold *site-wise* capped convolution of the annual MPS. After each
year we contract the two cores back to a 10 x 10 matrix and take an exact SVD again
(only singular values below 1e-14 relative are dropped, i.e. floating-point noise).
This two-site recompression is exact but costs O(d^n); it is a reference method for
n = 2 only, not a scalable algorithm.

Targets
-------
The five official targets are computed by a transfer pass over the two cores that
carries (bond index, accumulated loss in integer US cents), so the portfolio loss
distribution is obtained exactly.
"""
from __future__ import annotations

import numpy as np

EQ_LEVELS, RAIN_LEVELS = 5, 2
D = EQ_LEVELS * RAIN_LEVELS
NOISE_RTOL = 1e-14  # drop only floating-point-noise singular values

TARGETS = (
    "term_expected_principal_loss_usd",
    "term_joint_attachment_probability",
    "term_portfolio_loss_exceedance_probability",
    "term_portfolio_stop_loss_usd",
    "term_both_bonds_exhausted_probability",
)


# --------------------------------------------------------------------------- MPS basics
def split(matrix):
    """Exact SVD split of a d x d matrix into two MPS cores (1,d,chi) and (chi,d,1)."""
    u, s, vt = np.linalg.svd(np.asarray(matrix, float), full_matrices=False)
    keep = max(1, int(np.sum(s > NOISE_RTOL * s[0]))) if s[0] > 0 else 1
    a = (u[:, :keep] * s[:keep]).reshape(1, D, keep)
    b = vt[:keep].reshape(keep, D, 1)
    return [a, b]


def merge(cores):
    """Contract two cores back to the d x d matrix they represent."""
    a, b = cores
    return np.einsum("asx,xtb->st", a, b)


def bond_dimension(cores):
    return int(cores[0].shape[2])


def contract_with(cores, w1, w2):
    """sum_{s,t} P[s,t] w1[s] w2[t]."""
    a, b = cores
    return float(np.einsum("asx,s,xtb,t->", a, w1, b, w2))


# --------------------------------------------------------------------------- model
def cap_op():
    """Local accumulation map op[s, t, u] = 1 iff capped(s + t) == u."""
    op = np.zeros((D, D, D))
    for s in range(D):
        for t in range(D):
            e = min(s // 2 + t // 2, EQ_LEVELS - 1)
            r = min(s % 2 + t % 2, RAIN_LEVELS - 1)
            op[s, t, 2 * e + r] = 1.0
    return op


def annual_matrix(model):
    """Official 100-state annual law of a qjlb BondModel as a (KGZ e,r) x (TJK e,r) matrix."""
    p = model.probabilities.reshape(EQ_LEVELS, EQ_LEVELS, RAIN_LEVELS, RAIN_LEVELS)
    return p.transpose(0, 2, 1, 3).reshape(D, D)


def annual_mps(model):
    return split(annual_matrix(model))


def term_mps(annual, years):
    """Y-fold site-wise capped convolution, with exact two-site recompression each year."""
    op = cap_op()
    out = annual
    for _ in range(years - 1):
        a = np.einsum("asb,ctd,stu->acubd", out[0], annual[0], op)
        b = np.einsum("asb,ctd,stu->acubd", out[1], annual[1], op)
        la, ra = out[0].shape[2], annual[0].shape[2]
        a = a.reshape(1, D, la * ra)
        b = b.reshape(la * ra, D, 1)
        out = split(merge([a, b]))
    return out


def site_losses(eq_limit, rain_limit):
    e = np.arange(D) // 2
    r = np.arange(D) % 2
    return e * eq_limit / 4.0 + r * rain_limit


def targets(cores, eq_limits, rain_limits, threshold):
    """The five official targets by exact contraction of the term MPS."""
    eq_limits = np.asarray(eq_limits, float)
    rain_limits = np.asarray(rain_limits, float)
    principal = eq_limits + rain_limits
    ones = np.ones(D)
    z = contract_with(cores, ones, ones)

    # transfer pass: state = (bond index, accumulated loss in cents)
    vals = np.zeros(1, dtype=np.int64)
    v = np.ones((1, 1))
    for k, c in enumerate(cores):
        cents = np.rint(site_losses(eq_limits[k], rain_limits[k]) * 100).astype(np.int64)
        cand = (vals[None, :] + cents[:, None]).ravel()
        new_vals, inv = np.unique(cand, return_inverse=True)
        contrib = np.einsum("lsr,lk->rsk", c, v).reshape(c.shape[2], -1)
        new = np.zeros((c.shape[2], new_vals.size))
        np.add.at(new.T, inv, contrib.T)
        vals, v = new_vals, new
    dist = v[0] / z
    grid = vals / 100.0

    pays = [(site_losses(eq_limits[k], rain_limits[k]) > 0).astype(float) for k in range(2)]
    exhausted = [(site_losses(eq_limits[k], rain_limits[k]) >= principal[k] - 1e-6).astype(float) for k in range(2)]
    return {
        TARGETS[0]: float(dist @ grid),
        TARGETS[1]: contract_with(cores, *pays) / z,
        TARGETS[2]: float(dist[grid > threshold + 1e-9].sum()),
        TARGETS[3]: float(dist @ np.maximum(grid - threshold, 0.0)),
        TARGETS[4]: contract_with(cores, *exhausted) / z,
    }
