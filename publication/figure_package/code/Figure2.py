# ============================================================
# Figure 2: Motor Portfolio Scale, Outcome Dynamics, and Composition Shift, 2022 to 2024
# Supports: Section 4.1, temporal evaluation is required because portfolio scale, outcomes, and composition change materially
# Data: Public Spanish motor insurance portfolio, 2022 to 2024, DOI 10.17632/sw4jmdb2sm.1
# Output: figures/Figure2.png (300 dpi, publication ready)
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
# Values are the audited paper internal aggregates derived from the cited public dataset.
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, PercentFormatter

years = np.array([2022, 2023, 2024])
policy_rows = np.array([67172, 118835, 168133])
claim_frequency = np.array([0.30218, 0.30532, 0.31168])
loss_ratio = np.array([0.65623, 0.66456, 0.74664])
new_business_share = np.array([0.9790537724, 0.7007194850, 0.5733675126])
portfolio_share = 1.0 - new_business_share

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
fig, axes = plt.subplots(1, 3, figsize=(16, 5.4))

# PANEL A: portfolio scale
axes[0].bar(years.astype(str), policy_rows, color=PRIMARY, width=0.62)
axes[0].set_title("Portfolio scale")
axes[0].set_xlabel("Calendar year")
axes[0].set_ylabel("Policy year records")
axes[0].yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value / 1000:.0f}k"))
for index, value in enumerate(policy_rows):
    axes[0].text(index, value + 4500, f"{value:,}", ha="center", va="bottom", color=PRIMARY, fontsize=9)
axes[0].set_ylim(0, 190000)

# PANEL B: observed outcomes
axes[1].plot(years, 100 * claim_frequency, color=SECONDARY, linewidth=1.4,
             marker="o", markersize=5, label="Claim frequency")
axes[1].plot(years, 100 * loss_ratio, color=PRIMARY, linewidth=1.4,
             marker="s", markersize=5, label="Loss ratio")
axes[1].set_title("Observed portfolio outcomes")
axes[1].set_xlabel("Calendar year")
axes[1].set_ylabel("Percent")
axes[1].set_xticks(years)
axes[1].set_ylim(25, 80)
axes[1].legend(frameon=False, loc="upper left")
axes[1].annotate("74.66%", xy=(2024, 74.664), xytext=(2023.55, 78.0),
                 arrowprops={"arrowstyle": "->", "color": ACCENT, "linewidth": 0.8},
                 color=PRIMARY, fontsize=8, fontstyle="italic")

# PANEL C: business composition
axes[2].bar(years.astype(str), 100 * new_business_share, color=PRIMARY,
            width=0.62, label="New business")
axes[2].bar(years.astype(str), 100 * portfolio_share, bottom=100 * new_business_share,
            color=FILL_LIGHT, edgecolor=SECONDARY, linewidth=0.8,
            width=0.62, label="Existing portfolio")
axes[2].set_title("Business type composition")
axes[2].set_xlabel("Calendar year")
axes[2].set_ylabel("Share of policy year records")
axes[2].set_ylim(0, 100)
axes[2].yaxis.set_major_formatter(PercentFormatter(100))
axes[2].text(2, 29, "New business\n57.34%", ha="center", va="center",
             color="white", fontsize=8)
axes[2].text(2, 78.7, "Existing portfolio\n42.66%", ha="center", va="center",
             color=PRIMARY, fontsize=8)
axes[2].annotate("Change in new business share:\nnegative 40.57 percentage points",
                 xy=(2, 57.34), xytext=(0.60, 47),
                 arrowprops={"arrowstyle": "->", "color": ACCENT, "linewidth": 0.8},
                 bbox={"boxstyle": "round,pad=0.25", "facecolor": "white",
                       "edgecolor": FILL_LIGHT, "alpha": 0.95},
                 color=PRIMARY, fontsize=8, fontstyle="italic", ha="center")

for label, axis in zip(["(A)", "(B)", "(C)"], axes):
    axis.text(-0.12, 1.06, label, transform=axis.transAxes, fontsize=12,
              fontweight="bold", color=PRIMARY, va="top")
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.spines["left"].set_color(PRIMARY)
    axis.spines["bottom"].set_color(PRIMARY)
    axis.grid(axis="y")
    axis.grid(axis="x", visible=False)

plt.tight_layout(pad=1.5)
plt.savefig("figures/Figure2.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.show()
