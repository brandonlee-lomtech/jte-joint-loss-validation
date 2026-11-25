"""Figure 1: per-target error of the official samplers vs this solver on the five ADB scenarios."""
import csv

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from common import ADB_SCENARIOS, FIGURES, RESULTS, SAMPLER_LABEL, SAMPLERS, SHORT  # noqa: E402

rows = list(csv.DictReader(open(RESULTS / "baseline_comparison.csv")))
targets = list(SHORT.values())
fig, axes = plt.subplots(1, len(ADB_SCENARIOS), figsize=(18, 4), sharey=True)
x = np.arange(len(targets))
w = 0.16
for ax, s in zip(axes, ADB_SCENARIOS):
    sub = {r["target"]: r for r in rows if r["scenario"] == s}
    for i, m in enumerate(SAMPLERS):
        ax.bar(x + (i - 2) * w, [float(sub[t][m + "_rel_rmse"]) for t in targets], w, label=SAMPLER_LABEL[m])
    ax.bar(x + 2 * w, [max(float(sub[t]["ours_rel_err"]), 1e-16) for t in targets], w, label="This solver (exact)",
           color="black")
    ax.set_yscale("log")
    ax.set_title(s)
    ax.set_xticks(x, targets, rotation=45, ha="right", fontsize=8)
axes[0].set_ylabel("relative RMSE (samplers) / relative error (exact)")
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="lower center", ncol=5, fontsize=8)
fig.suptitle("Official ADB scenarios: official samplers (10 x 8,192) vs two-site MPS exact contraction")
fig.tight_layout(rect=(0, 0.06, 1, 1))
FIGURES.mkdir(exist_ok=True)
fig.savefig(FIGURES / "fig1_adb_errors.png", dpi=110)
print("wrote figures/fig1_adb_errors.png")
