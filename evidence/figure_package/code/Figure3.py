# ============================================================
# Figure 3: Temporal Forecast Performance Across Matched Actuarial Comparators
# Supports: Section 4.2 and H5, policy level frequency improves deviance but not every aggregate error, while policy level cost is unstable
# Data: ARCCRAFT retrospective policy benchmark derived from the public Spanish motor insurance portfolio
# Output: figures/Figure3.png (300 dpi, publication ready)
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
# Values are the audited outputs reported in the paper and evidence table 19.
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

models = [
    "Aggregate pooled",
    "Policy frequency, pooled cost",
    "Policy frequency, policy cost",
]
years = [2023, 2024]
claim_error = {
    2023: np.array([-1.0291, -0.8626, -0.8626]),
    2024: np.array([-2.3803, -2.4282, -2.4282]),
}
incurred_error = {
    2023: np.array([2.7009, 2.8737, 9.5794]),
    2024: np.array([-4.8760, -4.9227, -4.4435]),
}
claim_deviance = {
    2023: np.array([0.84808, 0.78714, 0.78714]),
    2024: np.array([0.91532, 0.83304, 0.83304]),
}
incurred_deviance = {
    2023: np.array([1200.0798, 1150.3540, 1174.0425]),
    2024: np.array([1353.5359, 1296.2574, 1302.4222]),
}

# PARAMETERS
PRIMARY = "#0A1940"
SECONDARY = "#193C78"
ACCENT = "#3769B4"
FILL_LIGHT = "#E1E8F5"
NEUTRAL = "#888888"
YEAR_STYLE = {
    2023: {"color": PRIMARY, "marker": "o", "label": "Evaluation year 2023"},
    2024: {"color": ACCENT, "marker": "s", "label": "Evaluation year 2024"},
}

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

def comparison_panel(axis, values, title, xlabel, zero_reference=False, value_format="{:.2f}"):
    positions = np.arange(len(models))
    offsets = {2023: -0.10, 2024: 0.10}
    if zero_reference:
        axis.axvline(0, color=NEUTRAL, linewidth=0.9, linestyle=":", zorder=1)
    for year in years:
        style = YEAR_STYLE[year]
        y = positions + offsets[year]
        axis.scatter(values[year], y, s=47, color=style["color"], marker=style["marker"],
                     label=style["label"], zorder=3)
        for x_value, y_value in zip(values[year], y):
            horizontal = 5 if x_value >= 0 else -5
            alignment = "left" if x_value >= 0 else "right"
            axis.annotate(value_format.format(x_value), (x_value, y_value),
                          xytext=(horizontal, 0), textcoords="offset points",
                          ha=alignment, va="center", fontsize=8, color=style["color"])
    axis.set_title(title)
    axis.set_xlabel(xlabel)
    axis.set_yticks(positions, models)
    axis.invert_yaxis()
    axis.grid(axis="x")
    axis.grid(axis="y", visible=False)
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.spines["left"].set_color(PRIMARY)
    axis.spines["bottom"].set_color(PRIMARY)

os.makedirs("figures", exist_ok=True)
fig, axes = plt.subplots(2, 2, figsize=(14, 8.5))

comparison_panel(axes[0, 0], claim_error, "Aggregate claim count error",
                 "Error relative to observed count (%)", zero_reference=True)
axes[0, 0].set_xlim(-3.05, 0.35)

comparison_panel(axes[0, 1], incurred_error, "Aggregate incurred loss error",
                 "Error relative to observed incurred loss (%)", zero_reference=True)
axes[0, 1].set_xlim(-6.0, 11.1)

comparison_panel(axes[1, 0], claim_deviance, "Policy level count deviance",
                 "Mean Poisson deviance", value_format="{:.3f}")
axes[1, 0].set_xlim(0, 1.02)

comparison_panel(axes[1, 1], incurred_deviance, "Policy level incurred deviance",
                 "Mean Poisson deviance", value_format="{:.1f}")
axes[1, 1].set_xlim(0, 1510)

for label, axis in zip(["(A)", "(B)", "(C)", "(D)"], axes.ravel()):
    axis.text(-0.18, 1.08, label, transform=axis.transAxes, fontsize=12,
              fontweight="bold", color=PRIMARY, va="top")

handles, labels = axes[0, 0].get_legend_handles_labels()
fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 1.005),
           ncol=2, frameon=False)
fig.suptitle("Matched temporal forecast performance", fontsize=15,
             fontweight="bold", color=PRIMARY, y=1.045)

plt.tight_layout(pad=1.5)
plt.savefig("figures/Figure3.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.show()
