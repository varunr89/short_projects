"""
Chart 1: The Productivity Curve ("The Integral Problem")

Generates a chart showing why AI adoption by only the top percentile
of employees barely moves the organizational productivity needle.

Before AI: y = x^1.5 (normalized)
After AI: same curve + sigmoid bump for top ~10%

Output: ../charts/01_productivity_curve.png
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
OUTPUT_PATH = os.path.join(PROJECT_DIR, "charts", "01_productivity_curve.png")

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
x = np.linspace(0, 100, 1000)       # employee percentile 0-100
x_norm = x / 100.0                   # normalized to 0-1

# Before AI: power curve
y_before = x_norm ** 1.5

# After AI: same base curve + sigmoid bump kicking in around 88-92nd percentile
# Sigmoid centered at x=92, steep transition, maxing out at ~35% lift
sigmoid = 1.0 / (1.0 + np.exp(-0.8 * (x - 92)))
bump = 0.35 * sigmoid * x_norm      # scale bump by x_norm so it's proportional
y_after = y_before + bump

# ---------------------------------------------------------------------------
# Style setup
# ---------------------------------------------------------------------------
# Try to use a nice sans-serif font; fall back gracefully
PREFERRED_FONTS = ["Inter", "Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"]
available_fonts = {f.name for f in fm.fontManager.ttflist}
chosen_font = next((f for f in PREFERRED_FONTS if f in available_fonts), "sans-serif")

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": [chosen_font],
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "text.color": "#2d2d2d",
    "axes.labelcolor": "#2d2d2d",
    "xtick.color": "#555555",
    "ytick.color": "#555555",
})

# Muted color palette
COLOR_BEFORE = "#6c7a89"   # slate grey
COLOR_AFTER = "#2e86ab"    # muted teal-blue
COLOR_FILL = "#2e86ab"     # same as after-curve, with alpha

# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))

# Plot curves
ax.plot(x, y_before, color=COLOR_BEFORE, linewidth=2.4, label="Before AI", zorder=3)
ax.plot(x, y_after, color=COLOR_AFTER, linewidth=2.4, label="After AI", zorder=3)

# Shaded area between curves
ax.fill_between(x, y_before, y_after, color=COLOR_FILL, alpha=0.18, zorder=2)

# Label the shaded region
# Arrow points FROM the text TO the midpoint of the shaded area
mid_idx = 960   # index corresponding to ~96th percentile
ax.annotate(
    "Net organizational\nproductivity gain",
    xy=(x[mid_idx], (y_before[mid_idx] + y_after[mid_idx]) / 2),
    xytext=(58, 0.92),
    fontsize=9,
    color="#2d2d2d",
    fontstyle="italic",
    arrowprops=dict(
        arrowstyle="->",
        color="#888888",
        connectionstyle="arc3,rad=-0.2",
        lw=1.0,
    ),
    zorder=5,
)

# ---------------------------------------------------------------------------
# Axes and labels
# ---------------------------------------------------------------------------
ax.set_xlabel("Employee Percentile", fontsize=12, labelpad=10)
ax.set_ylabel("Productivity", fontsize=12, labelpad=10)
ax.set_xlim(0, 100)
ax.set_ylim(0, None)

# Remove y-axis tick labels (arbitrary units)
ax.set_yticklabels([])
ax.tick_params(axis="y", length=0)

# Minimal x-axis ticks
ax.set_xticks([0, 25, 50, 75, 100])
ax.tick_params(axis="x", labelsize=10)

# Remove gridlines (already off by default, but be explicit)
ax.grid(False)

# Legend -- upper left, no frame
ax.legend(
    loc="upper left",
    fontsize=10,
    frameon=False,
    handlelength=1.8,
    handletextpad=0.6,
)

# Title and subtitle
ax.set_title(
    "The Integral Problem",
    fontsize=16,
    fontweight="bold",
    pad=24,
    color="#1a1a1a",
)
fig.text(
    0.5, 0.91,
    "Organizational output = area under the curve. "
    "If only the top 5% adopt AI, the total area barely changes.",
    ha="center",
    fontsize=9.5,
    color="#666666",
    fontstyle="italic",
)

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
plt.tight_layout(rect=[0, 0, 1, 0.89])   # leave room for subtitle
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
fig.savefig(OUTPUT_PATH, dpi=300, bbox_inches="tight", facecolor="white")
plt.close(fig)

print(f"Chart saved to {OUTPUT_PATH}")
