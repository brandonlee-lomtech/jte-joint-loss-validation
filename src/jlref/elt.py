"""World Bank ELT track: exact vectorised pass over the catalogue rows.

This is NOT a tensor-network method. In the official `worldbank_elt` model every
target is a rate-weighted sum over catalogue rows with one conditional-mean loss per
row, so the exact answer is a single vectorised pass. Method label:
`jlref_elt_exact_vectorised`.
"""
from __future__ import annotations

import numpy as np


def elt_targets(model):
    loss = model.loss                                   # (rows, countries) USD
    h = model.peril                                     # 0 = seismic, 1 = flood
    att = model.attachment[h]
    exh = model.exhaustion[h]
    payout = model.limit * np.clip((loss - att) / (exh - att), 0.0, 1.0)
    total = payout.sum(axis=1)
    per_row = np.column_stack([
        loss.sum(axis=1),                               # annual economic loss
        total,                                          # annual layer payment
        np.all(payout > 0, axis=1),                     # joint layer exceedance
        total > model.threshold,                        # portfolio layer exceedance
        np.maximum(total - model.threshold, 0.0),       # stop-loss above threshold
    ]).astype(float)
    return model.rates @ per_row
