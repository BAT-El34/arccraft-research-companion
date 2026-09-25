# ============================================================
# Figure 6: Scenario Class Failure Rates and Failure Atlas Composition
# Supports: Section 4.3, failure frequency varies by registered scenario class and the current atlas is dominated by the traceability gate
# Data: Canonical ARCCRAFT run at seed 20260825 with 10,000 generated worlds
# Output: figures/Figure6.png (300 dpi, publication ready)
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
# Values are fixed outputs of the canonical registered run reported in the paper.
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

scenario_labels = ["Baseline", "Alternative", "Adverse", "Severe plausible", "Exploratory"]
accepted_worlds = np.array([1173, 2189, 4422, 1201, 1010])
failure_rates = np.array([0.0000, 0.3399, 0.4012, 0.4988, 0.4673]) * 100

atlas_labels = ["Traceability gate", "Combined ratio gate", "Structural rejection"]
atlas_counts = np.array([3588, 1, 5])

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
fig, axes = plt.subplots(1, 2, figsize=(14, 5.4), gridspec_kw={"width_ratios": [1.25, 1]})

# PANEL A: conditional failure rates across registered scenario classes
x = np.arange(len(scenario_labels))
colors = [FILL_LIGHT, "#AFC2DF", "#7899C7", ACCENT, SECONDARY]
bars = axes[0].bar(x, failure_rates, color=colors, edgecolor=PRIMARY, linewidth=0.8, width=0.68)
axes[0].set_title("Failure rate by registered scenario class")
axes[0].set_ylabel("Failures among accepted worlds (%)")
axes[0].set_xticks(x, scenario_labels, rotation=18, ha="right")
axes[0].set_ylim(0, 58)
axes[0].grid(axis="y")
axes[0].grid(axis="x", visible=False)
for bar, rate, count in zip(bars, failure_rates, accepted_worlds):
    axes[0].text(
        bar.get_x() + bar.get_width() / 2,
        max(rate + 1.2, 1.2),
        f"{rate:.2f}%\n$n$ = {count:,}",
        ha="center",
        va="bottom",
        fontsize=8.2,
        color=PRIMARY,
    )

# PANEL B: atlas gate composition. A log scale preserves visibility of rare gates.
y = np.arange(len(atlas_labels))[::-1]
for ypos, count in zip(y, atlas_counts):
    axes[1].hlines(ypos, 1, count, color=FILL_LIGHT, linewidth=5, zorder=1)
    axes[1].scatter(count, ypos, s=80, color=ACCENT, edgecolor=PRIMARY, linewidth=0.9, zorder=2)
    axes[1].annotate(
        f"{count:,}",
        xy=(count, ypos),
        xytext=(7 if count < 100 else 8, 0),
        textcoords="offset points",
        va="center",
        fontsize=9,
        fontweight="bold",
        color=PRIMARY,
    )
axes[1].set_xscale("log")
axes[1].set_xlim(0.75, 9000)
axes[1].set_yticks(y, atlas_labels)
axes[1].set_xlabel("Recorded events, logarithmic scale")
axes[1].set_title("Failure Atlas composition")
axes[1].grid(axis="x")
axes[1].grid(axis="y", visible=False)
axes[1].text(
    0.04,
    0.08,
    "The experiment primarily exercises\nthe operational traceability gate.",
    transform=axes[1].transAxes,
    fontsize=9,
    fontstyle="italic",
    color=PRIMARY,
    bbox={"boxstyle": "round,pad=0.35", "facecolor": FILL_FROST, "edgecolor": FILL_LIGHT},
)

for axis, label in zip(axes, ["(A)", "(B)"]):
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.spines["left"].set_color(PRIMARY)
    axis.spines["bottom"].set_color(PRIMARY)
    axis.spines["left"].set_linewidth(0.8)
    axis.spines["bottom"].set_linewidth(0.8)
    axis.tick_params(colors=PRIMARY)
    axis.text(-0.12, 1.05, label, transform=axis.transAxes, fontsize=12,
              fontweight="bold", color=PRIMARY)

plt.tight_layout(pad=1.5)
plt.savefig("figures/Figure6.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.show()
