# ============================================================
# Figure 7: Procedural Ablations, Computational Cost, and Stream Isolation
# Supports: Section 4.4, procedural choices affect reported failures, exact replay succeeds, and named streams isolate irrelevant random draws
# Data: Three registered 10,000 world runs per configuration and the stream isolation intervention
# Output: figures/Figure7.png (300 dpi, publication ready)
# ============================================================

# COLAB DEPENDENCIES
import importlib.util
import subprocess
import sys

REQUIRED = {"numpy": "numpy", "matplotlib": "matplotlib"}
missing = [package for module, package in REQUIRED.items() if importlib.util.find_spec(module) is None]
if missing:
    subprocess.check_call([sys.executable, "-m", "pip", "install", *missing])

# DATA LOADING
# Summary values are embedded from evidence tables 26 and 27 for portable execution.
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

config_labels = ["Full", "No transitions", "No validator", "Shared stream", "Strict rejection"]

failure_accepted_mean = np.array([35.9501, 35.7033, 35.7867, 35.2000, 36.8339])
failure_accepted_sd = np.array([0.2361, 0.2480, 0.2150, 0.6861, 0.3389])
failure_or_reject_mean = np.array([35.9800, 35.7333, 35.7867, 35.2367, 49.4100])
failure_or_reject_sd = np.array([0.2326, 0.2444, 0.2150, 0.6917, 0.4158])

runtime_mean = np.array([3.5929, 3.5011, 4.7432, 3.9656, 3.2109])
runtime_sd = np.array([1.0450, 0.1302, 1.0399, 0.8032, 0.4393])

# Rows: full named streams and shared stream. Columns: exact rerun and irrelevant draw intervention.
invariance_matrix = np.array([[1, 1], [1, 0]])

# PARAMETERS
PRIMARY = "#0A1940"
SECONDARY = "#193C78"
ACCENT = "#3769B4"
FILL_LIGHT = "#E1E8F5"
FILL_FROST = "#F0F4FC"
NEUTRAL = "#888888"

mpl.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Palatino", "DejaVu Serif"],
    "axes.titlesize": 13,
    "axes.titleweight": "bold",
    "axes.titlecolor": PRIMARY,
    "axes.labelsize": 11,
    "axes.labelcolor": PRIMARY,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "legend.fontsize": 9,
    "axes.edgecolor": PRIMARY,
    "axes.linewidth": 0.8,
    "grid.color": SECONDARY,
    "grid.alpha": 0.3,
    "grid.linestyle": ":",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})

os.makedirs("figures", exist_ok=True)
fig, axes = plt.subplots(1, 3, figsize=(18, 5.6), gridspec_kw={"width_ratios": [1.35, 1.05, 0.9]})

# PANEL A: failure definitions under procedural ablations
x = np.arange(len(config_labels))
offset = 0.12
axes[0].errorbar(
    x - offset,
    failure_accepted_mean,
    yerr=failure_accepted_sd,
    fmt="o",
    markersize=6,
    capsize=3,
    color=PRIMARY,
    ecolor=PRIMARY,
    linewidth=1.0,
    label="Failure among accepted worlds",
)
axes[0].errorbar(
    x + offset,
    failure_or_reject_mean,
    yerr=failure_or_reject_sd,
    fmt="s",
    markersize=5.5,
    capsize=3,
    color=ACCENT,
    ecolor=ACCENT,
    linewidth=1.0,
    label="Failure or structural rejection",
)
axes[0].set_title("Failure measures under procedural ablations")
axes[0].set_ylabel("Rate across generated worlds (%)")
axes[0].set_xticks(x, config_labels, rotation=18, ha="right")
axes[0].set_ylim(32, 52)
axes[0].grid(axis="y")
axes[0].grid(axis="x", visible=False)
axes[0].legend(loc="upper left", frameon=False)
axes[0].annotate(
    "Selection effect",
    xy=(4 + offset, failure_or_reject_mean[-1]),
    xytext=(3.15, 50.5),
    arrowprops={"arrowstyle": "->", "color": ACCENT, "linewidth": 0.9},
    fontsize=8.5,
    fontstyle="italic",
    color=PRIMARY,
)

# PANEL B: measured runtime for each registered configuration
bars = axes[1].bar(
    x,
    runtime_mean,
    yerr=runtime_sd,
    capsize=3,
    color=[PRIMARY, SECONDARY, ACCENT, "#7899C7", "#AFC2DF"],
    edgecolor=PRIMARY,
    linewidth=0.7,
    width=0.68,
)
axes[1].set_title("Measured computational cost")
axes[1].set_ylabel("Total runtime per 10,000 worlds (seconds)")
axes[1].set_xticks(x, config_labels, rotation=18, ha="right")
axes[1].set_ylim(0, 6.3)
axes[1].grid(axis="y")
axes[1].grid(axis="x", visible=False)
for bar, mean in zip(bars, runtime_mean):
    axes[1].text(
        bar.get_x() + bar.get_width() / 2,
        mean + 0.18,
        f"{mean:.2f}",
        ha="center",
        va="bottom",
        fontsize=8,
        color=PRIMARY,
    )

# PANEL C: exact replay and isolation intervention outcomes
cmap = ListedColormap([FILL_FROST, ACCENT])
axes[2].imshow(invariance_matrix, cmap=cmap, vmin=0, vmax=1, aspect="auto")
axes[2].set_title("Reproducibility and stream isolation")
axes[2].set_xticks([0, 1], ["Same seed\nrerun", "100 irrelevant\nworld draws"])
axes[2].set_yticks([0, 1], ["Named streams", "Shared stream"])
for row in range(2):
    for column in range(2):
        invariant = bool(invariance_matrix[row, column])
        axes[2].text(
            column,
            row,
            "Invariant" if invariant else "Changed",
            ha="center",
            va="center",
            fontsize=10,
            fontweight="bold",
            color="white" if invariant else PRIMARY,
        )
axes[2].text(
    0.5,
    -0.22,
    "Exact replay verified in 15 of 15 registered runs",
    transform=axes[2].transAxes,
    ha="center",
    fontsize=8.5,
    fontstyle="italic",
    color=PRIMARY,
)
axes[2].tick_params(length=0)

for axis, label in zip(axes, ["(A)", "(B)", "(C)"]):
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.spines["left"].set_color(PRIMARY)
    axis.spines["bottom"].set_color(PRIMARY)
    axis.spines["left"].set_linewidth(0.8)
    axis.spines["bottom"].set_linewidth(0.8)
    axis.tick_params(colors=PRIMARY)
    axis.text(-0.12, 1.06, label, transform=axis.transAxes, fontsize=12,
              fontweight="bold", color=PRIMARY)

plt.tight_layout(pad=1.5)
plt.savefig("figures/Figure7.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.show()
