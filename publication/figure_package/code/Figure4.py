# ============================================================
# Figure 4: Risk Decile Calibration and Process Interval Coverage
# Supports: Section 4.2, structured calibration error and incomplete process interval coverage qualify the deviance improvement
# Data: ARCCRAFT retrospective policy benchmark derived from the public Spanish motor insurance portfolio
# Output: figures/Figure4.png (300 dpi, publication ready)
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
# Values are the audited outputs reported in evidence tables 19 and 20.
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

deciles = np.arange(1, 11)
count_op = {
    2023: np.array([1.31334, 1.03711, 0.99943, 1.06992, 1.01803,
                    0.92373, 0.87734, 0.95384, 1.02640, 1.07544]),
    2024: np.array([1.43513, 1.17411, 1.08578, 0.99307, 0.95561,
                    0.93556, 0.91922, 0.99821, 1.00412, 1.10260]),
}
incurred_op = {
    2023: np.array([1.50562, 1.68403, 1.23103, 1.21400, 1.07808,
                    0.96467, 0.82375, 0.81907, 0.81407, 0.79069]),
    2024: np.array([1.92796, 1.97876, 1.25144, 1.22204, 0.95714,
                    0.91938, 0.86303, 1.13806, 0.99746, 0.95404]),
}

interval_rows = [
    {"year": 2023, "model": "Aggregate pooled", "claim_obs": 25158.0,
     "claim_mean": 24899.1094, "claim_low": 24589.8322, "claim_high": 25208.3867,
     "incurred_obs": 23488354.3540, "incurred_mean": 24122754.6960,
     "incurred_low": 23580209.4579, "incurred_high": 24665299.9341},
    {"year": 2023, "model": "Policy frequency, pooled cost", "claim_obs": 25158.0,
     "claim_mean": 24940.9902, "claim_low": 24631.4529, "claim_high": 25250.5274,
     "incurred_obs": 23488354.3540, "incurred_mean": 24163329.6175,
     "incurred_low": 23620328.2854, "incurred_high": 24706330.9495},
    {"year": 2023, "model": "Policy frequency, policy cost", "claim_obs": 25158.0,
     "claim_mean": 24940.9902, "claim_low": 24631.4529, "claim_high": 25250.5274,
     "incurred_obs": 23488354.3540, "incurred_mean": 25738401.3604,
     "incurred_low": 25116483.5201, "incurred_high": 26360319.2008},
    {"year": 2024, "model": "Aggregate pooled", "claim_obs": 39276.0,
     "claim_mean": 38341.1027, "claim_low": 37957.3174, "claim_high": 38724.8881,
     "incurred_obs": 38106351.2800, "incurred_mean": 36248281.8756,
     "incurred_low": 35577245.1525, "incurred_high": 36919318.5987},
    {"year": 2024, "model": "Policy frequency, pooled cost", "claim_obs": 39276.0,
     "claim_mean": 38322.2935, "claim_low": 37938.6023, "claim_high": 38705.9847,
     "incurred_obs": 38106351.2800, "incurred_mean": 36230499.3240,
     "incurred_low": 35559627.2184, "incurred_high": 36901371.4295},
    {"year": 2024, "model": "Policy frequency, policy cost", "claim_obs": 39276.0,
     "claim_mean": 38322.2935, "claim_low": 37938.6023, "claim_high": 38705.9847,
     "incurred_obs": 38106351.2800, "incurred_mean": 36413116.2861,
     "incurred_low": 35722604.2075, "incurred_high": 37103628.3647},
]

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

def calibration_panel(axis, values, title, y_limits):
    axis.axhline(1.0, color=NEUTRAL, linewidth=0.9, linestyle=":", label="Perfect calibration")
    for year in [2023, 2024]:
        style = YEAR_STYLE[year]
        axis.plot(deciles, values[year], color=style["color"], linewidth=1.3,
                  marker=style["marker"], markersize=4.5, label=style["label"])
    axis.set_title(title)
    axis.set_xlabel("Predicted risk decile")
    axis.set_ylabel("Observed to predicted ratio")
    axis.set_xticks(deciles)
    axis.set_ylim(*y_limits)

def interval_panel(axis, prefix, title, x_limits):
    labels = [f"{row['year']}  {row['model']}" for row in interval_rows]
    positions = np.arange(len(interval_rows))
    axis.axvline(1.0, color=NEUTRAL, linewidth=1.0, linestyle=":", label="Observed value")
    for position, row in zip(positions, interval_rows):
        observed = row[f"{prefix}_obs"]
        mean = row[f"{prefix}_mean"] / observed
        low = row[f"{prefix}_low"] / observed
        high = row[f"{prefix}_high"] / observed
        style = YEAR_STYLE[row["year"]]
        axis.plot([low, high], [position, position], color=style["color"], linewidth=1.3)
        axis.scatter(mean, position, color=style["color"], marker=style["marker"], s=43, zorder=3)
        covered = low <= 1.0 <= high
        axis.text(high + 0.004 * (x_limits[1] - x_limits[0]), position,
                  "covered" if covered else "missed", va="center", fontsize=8,
                  color=style["color"], fontstyle="italic")
    axis.set_title(title)
    axis.set_xlabel("Prediction and process interval relative to observed value")
    axis.set_yticks(positions, labels)
    axis.set_xlim(*x_limits)
    axis.invert_yaxis()

os.makedirs("figures", exist_ok=True)
fig, axes = plt.subplots(2, 2, figsize=(15.5, 9.5))

calibration_panel(axes[0, 0], count_op, "Claim count calibration by risk decile", (0.72, 1.52))
calibration_panel(axes[0, 1], incurred_op, "Incurred loss calibration by risk decile", (0.68, 2.10))
interval_panel(axes[1, 0], "claim", "Claim count process interval coverage", (0.955, 1.025))
interval_panel(axes[1, 1], "incurred", "Incurred loss process interval coverage", (0.91, 1.15))

for label, axis in zip(["(A)", "(B)", "(C)", "(D)"], axes.ravel()):
    axis.text(-0.18, 1.08, label, transform=axis.transAxes, fontsize=12,
              fontweight="bold", color=PRIMARY, va="top")
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.spines["left"].set_color(PRIMARY)
    axis.spines["bottom"].set_color(PRIMARY)
    axis.grid(axis="y")
    axis.grid(axis="x", visible=False)

handles, labels = axes[0, 0].get_legend_handles_labels()
fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 1.002),
           ncol=3, frameon=False)
fig.suptitle("Calibration and process interval diagnostics", fontsize=15,
             fontweight="bold", color=PRIMARY, y=1.04)

plt.tight_layout(pad=1.5)
plt.savefig("figures/Figure4.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.show()
