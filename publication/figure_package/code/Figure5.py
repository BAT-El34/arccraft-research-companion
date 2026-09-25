# ============================================================
# Figure 5: Frequency and Severity Stress Surface for the Motor Portfolio
# Supports: Section 4.3, the configured stress response is monotone and the joint 25 percent stress crosses the loss ratio threshold
# Data: Registered ARCCRAFT stress simulations using paper internal parameters
# Output: figures/Figure5.png (300 dpi, publication ready)
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
# Values are the registered 5 by 5 stress surface reported in evidence table 11.
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Rectangle

multipliers = np.array([0.75, 1.00, 1.25, 1.50, 1.75])
mean_loss_ratio = np.array([
    [0.39948, 0.53269, 0.66585, 0.79911, 0.93215],
    [0.53271, 0.71030, 0.88765, 1.06521, 1.24279],
    [0.66582, 0.88775, 1.10985, 1.33156, 1.55354],
    [0.79890, 1.06528, 1.33190, 1.59818, 1.86427],
    [0.93216, 1.24285, 1.55360, 1.86423, 2.17520],
])
diagonal_mean = np.array([0.39948, 0.71030, 1.10985, 1.59818, 2.17520])
diagonal_low = np.array([0.39098, 0.69711, 1.09131, 1.57376, 2.14516])
diagonal_high = np.array([0.40801, 0.72358, 1.12822, 1.62199, 2.20565])

# PARAMETERS
PRIMARY = "#0A1940"
SECONDARY = "#193C78"
ACCENT = "#3769B4"
FILL_LIGHT = "#E1E8F5"
FILL_FROST = "#F0F4FC"
NEUTRAL = "#888888"
NAVY_MAP = LinearSegmentedColormap.from_list(
    "arccraft_navy", ["#F0F4FC", "#E1E8F5", "#7A9BCB", "#3769B4", "#193C78", "#0A1940"]
)

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
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# PANEL A: complete two dimensional response surface
image = axes[0].imshow(mean_loss_ratio, cmap=NAVY_MAP, vmin=0.35, vmax=2.20,
                       aspect="equal", origin="lower")
axes[0].set_title("Mean loss ratio across joint stresses")
axes[0].set_xlabel("Severity multiplier")
axes[0].set_ylabel("Frequency multiplier")
axes[0].set_xticks(np.arange(5), [f"{value:.2f}" for value in multipliers])
axes[0].set_yticks(np.arange(5), [f"{value:.2f}" for value in multipliers])
for row in range(5):
    for column in range(5):
        value = mean_loss_ratio[row, column]
        text_color = "white" if value >= 1.18 else PRIMARY
        axes[0].text(column, row, f"{value:.2f}", ha="center", va="center",
                     fontsize=8.5, color=text_color,
                     fontweight="bold" if row == 2 and column == 2 else "normal")
axes[0].add_patch(Rectangle((1.5, 1.5), 1, 1, fill=False, edgecolor="white",
                            linewidth=2.0))
axes[0].annotate("Joint 25% stress", xy=(2, 2), xytext=(3.35, 1.25),
                 arrowprops={"arrowstyle": "->", "color": PRIMARY, "linewidth": 0.9},
                 bbox={"boxstyle": "round,pad=0.25", "facecolor": "white",
                       "edgecolor": FILL_LIGHT},
                 color=PRIMARY, fontsize=8, fontstyle="italic", ha="center")
colorbar = fig.colorbar(image, ax=axes[0], fraction=0.047, pad=0.04)
colorbar.set_label("Mean loss ratio", color=PRIMARY)
colorbar.outline.set_linewidth(0.7)

# PANEL B: diagonal joint stress path
axes[1].fill_between(multipliers, diagonal_low, diagonal_high,
                     color=FILL_LIGHT, alpha=0.8, label="95% process interval")
axes[1].plot(multipliers, diagonal_mean, color=PRIMARY, linewidth=1.5,
             marker="o", markersize=5, label="Mean loss ratio")
axes[1].axhline(1.0, color=NEUTRAL, linewidth=0.9, linestyle=":",
                label="Loss ratio threshold")
axes[1].scatter([1.25], [1.10985], color=ACCENT, edgecolor=PRIMARY,
                linewidth=0.7, s=72, zorder=4)
axes[1].annotate("Mean 1.11\n95% process interval: 1.09 to 1.13",
                 xy=(1.25, 1.10985), xytext=(1.36, 0.73),
                 arrowprops={"arrowstyle": "->", "color": ACCENT, "linewidth": 0.9},
                 bbox={"boxstyle": "round,pad=0.25", "facecolor": "white",
                       "edgecolor": FILL_LIGHT},
                 color=PRIMARY, fontsize=8, fontstyle="italic")
axes[1].set_title("Equal frequency and severity stress path")
axes[1].set_xlabel("Joint frequency and severity multiplier")
axes[1].set_ylabel("Loss ratio")
axes[1].set_xticks(multipliers)
axes[1].set_xlim(0.70, 1.80)
axes[1].set_ylim(0.25, 2.32)
axes[1].legend(frameon=False, loc="upper left")

for label, axis in zip(["(A)", "(B)"], axes):
    axis.text(-0.12, 1.06, label, transform=axis.transAxes, fontsize=12,
              fontweight="bold", color=PRIMARY, va="top")
    axis.spines["top"].set_visible(False)
    axis.spines["right"].set_visible(False)
    axis.spines["left"].set_color(PRIMARY)
    axis.spines["bottom"].set_color(PRIMARY)
    if axis is axes[1]:
        axis.grid(axis="y")
        axis.grid(axis="x", visible=False)

plt.tight_layout(pad=1.5)
plt.savefig("figures/Figure5.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.show()
