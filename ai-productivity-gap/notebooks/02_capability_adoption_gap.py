"""
Chart 2: The Capability-Adoption Gap

Timeline of AI model releases (capability skyrocketing) vs enterprise adoption
(nearly flat), with the widening gap shaded as "Unrealized productivity."

Output: charts/02_capability_adoption_gap.png
"""

import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from scipy.interpolate import make_interp_spline
from matplotlib.lines import Line2D

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "charts", "02_capability_adoption_gap.png")

# Provider colors -- muted, modern palette
COLORS = {
    "OpenAI":    "#6B8E7B",   # sage green
    "Anthropic": "#7A85AD",   # muted steel blue
    "Google":    "#C4956A",   # warm terracotta
}

CAPABILITY_LINE_COLOR = "#3D3D3D"
ADOPTION_LINE_COLOR = "#9B5E4A"
GAP_COLOR = "#D4C5B0"  # warm beige for the shaded gap

# ---------------------------------------------------------------------------
# Data: AI Model/Tool Releases
# ---------------------------------------------------------------------------
# Each entry: (date, name, provider)
ALL_RELEASES = [
    (datetime.date(2023,  3, 14), "GPT-4",                "OpenAI"),
    (datetime.date(2023,  7,  6), "Code Interpreter",     "OpenAI"),
    (datetime.date(2023, 12,  6), "Gemini 1.0 Pro",       "Google"),
    (datetime.date(2024,  3,  4), "Claude 3 Opus",        "Anthropic"),
    (datetime.date(2024,  5, 13), "GPT-4o",               "OpenAI"),
    (datetime.date(2024,  6, 20), "Claude 3.5 Sonnet",    "Anthropic"),
    (datetime.date(2024, 12, 11), "Gemini 2.0 Flash",     "Google"),
    (datetime.date(2025,  2, 24), "Claude Code",          "Anthropic"),
    (datetime.date(2025,  4, 16), "Codex CLI",            "OpenAI"),
    (datetime.date(2025,  5, 22), "Claude Opus 4",        "Anthropic"),
    (datetime.date(2025,  6, 17), "Gemini 2.5 Pro",       "Google"),
    (datetime.date(2026,  2,  5), "Claude Opus 4.6",      "Anthropic"),
]

# Which releases to label (drop GPT-4o and Code Interpreter to reduce clutter)
LABELS_TO_SKIP = {"GPT-4o", "Code Interpreter"}
LABELED_RELEASES = [r for r in ALL_RELEASES if r[1] not in LABELS_TO_SKIP]

# Manual annotation offsets: (x_offset_pts, y_offset_pts) and ha/va for each
# labeled release, to avoid overlaps in the dense mid-2025 cluster.
# Index maps to position in LABELED_RELEASES list.
LABEL_PLACEMENT = {
    # GPT-4: above-right
    "GPT-4":             (8,   20,  "left",   "bottom"),
    # Gemini 1.0 Pro: below
    "Gemini 1.0 Pro":    (0,  -20,  "center", "top"),
    # Claude 3 Opus: above
    "Claude 3 Opus":     (0,   20,  "center", "bottom"),
    # Claude 3.5 Sonnet: below
    "Claude 3.5 Sonnet": (0,  -20,  "center", "top"),
    # Gemini 2.0 Flash: below
    "Gemini 2.0 Flash":  (0,  -20,  "center", "top"),
    # Claude Code: above
    "Claude Code":       (-5,  20,  "center", "bottom"),
    # Codex CLI: below-right
    "Codex CLI":         (8,  -18,  "left",   "top"),
    # Claude Opus 4: above
    "Claude Opus 4":     (0,   20,  "center", "bottom"),
    # Gemini 2.5 Pro: below
    "Gemini 2.5 Pro":    (0,  -20,  "center", "top"),
    # Claude Opus 4.6: above-left
    "Claude Opus 4.6":   (-5,  20,  "center", "bottom"),
}


# ---------------------------------------------------------------------------
# Build the capability curve
# ---------------------------------------------------------------------------
def _date_to_num(d):
    """Convert date to matplotlib float."""
    return mdates.date2num(d)


release_dates_num = np.array([_date_to_num(r[0]) for r in ALL_RELEASES])

# Capability scores on 0..1 scale -- exponential-ish growth
# One score per release in ALL_RELEASES order
raw_scores = np.array([
    0.08,  # GPT-4
    0.13,  # Code Interpreter
    0.20,  # Gemini 1.0 Pro
    0.30,  # Claude 3 Opus
    0.36,  # GPT-4o
    0.43,  # Claude 3.5 Sonnet
    0.52,  # Gemini 2.0 Flash
    0.60,  # Claude Code
    0.66,  # Codex CLI
    0.73,  # Claude Opus 4
    0.80,  # Gemini 2.5 Pro
    0.97,  # Claude Opus 4.6
])

# Add a synthetic midpoint between Gemini 2.5 Pro and Claude Opus 4.6
# so the spline keeps climbing steadily instead of dipping
extra_dates = np.array([_date_to_num(datetime.date(2025, 10, 15))])
extra_scores = np.array([0.88])

all_cap_x = np.concatenate([release_dates_num, extra_dates])
all_cap_y = np.concatenate([raw_scores, extra_scores])
# Sort by date
sort_idx = np.argsort(all_cap_x)
all_cap_x = all_cap_x[sort_idx]
all_cap_y = all_cap_y[sort_idx]

# Smooth interpolation
x_min = _date_to_num(datetime.date(2023, 2, 1))
x_max = _date_to_num(datetime.date(2026, 3, 15))
x_smooth = np.linspace(x_min, x_max, 600)

spline_cap = make_interp_spline(all_cap_x, all_cap_y, k=3)
y_cap_smooth = spline_cap(x_smooth)
y_cap_smooth = np.clip(y_cap_smooth, 0, 1)

# ---------------------------------------------------------------------------
# Build the adoption curve
# ---------------------------------------------------------------------------
# Adoption data points (normalized 0-1):
# Mid-2023: 55% org adoption -- but real employee use much lower -> ~0.15
# Early 2024: 65% regularly using -> employee level ~0.20
# Mid-2024: 62% of developers using AI tools -> ~0.22
# Early 2025: 31% regular employee use, 7% fully scaled -> ~0.18
# Late 2025 / Early 2026: slight uptick -> ~0.22
adoption_data = [
    (datetime.date(2023, 2,  1), 0.12),   # extrapolated start
    (datetime.date(2023, 6, 15), 0.15),   # McKinsey mid-2023
    (datetime.date(2024, 1, 15), 0.20),   # McKinsey early 2024
    (datetime.date(2024, 6, 15), 0.22),   # Stack Overflow mid-2024
    (datetime.date(2025, 1, 15), 0.18),   # McKinsey/Worklytics early 2025
    (datetime.date(2025, 6, 15), 0.22),   # slight recovery
    (datetime.date(2026, 3, 15), 0.25),   # extrapolated
]

adopt_x = np.array([_date_to_num(d) for d, _ in adoption_data])
adopt_y = np.array([v for _, v in adoption_data])

spline_adopt = make_interp_spline(adopt_x, adopt_y, k=3)
y_adopt_smooth = spline_adopt(x_smooth)
y_adopt_smooth = np.clip(y_adopt_smooth, 0, 1)

# ---------------------------------------------------------------------------
# Plot
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# Shaded gap between the two curves
ax.fill_between(
    x_smooth, y_adopt_smooth, y_cap_smooth,
    where=(y_cap_smooth > y_adopt_smooth),
    color=GAP_COLOR, alpha=0.55, zorder=1,
    label="_nolegend_",
)

# Capability line (solid)
ax.plot(x_smooth, y_cap_smooth, color=CAPABILITY_LINE_COLOR, linewidth=2.2, zorder=3)

# Adoption line (dashed)
ax.plot(x_smooth, y_adopt_smooth, color=ADOPTION_LINE_COLOR, linewidth=2.2,
        linestyle="--", zorder=3)

# ---------------------------------------------------------------------------
# Markers for all releases (color-coded by provider)
# ---------------------------------------------------------------------------
for date_obj, name, provider in ALL_RELEASES:
    xpos = _date_to_num(date_obj)
    ypos = float(spline_cap(xpos))
    ax.scatter(xpos, ypos, color=COLORS[provider], s=40, zorder=5,
               edgecolors="white", linewidths=0.6)

# ---------------------------------------------------------------------------
# Labels with manual placement to avoid overlaps
# ---------------------------------------------------------------------------
for date_obj, name, provider in LABELED_RELEASES:
    xpos = _date_to_num(date_obj)
    ypos = float(spline_cap(xpos))

    x_off, y_off, ha, va = LABEL_PLACEMENT[name]

    ax.annotate(
        name,
        xy=(xpos, ypos),
        xytext=(x_off, y_off),
        textcoords="offset points",
        fontsize=6.0,
        fontfamily="sans-serif",
        color=COLORS[provider],
        fontweight="medium",
        ha=ha,
        va=va,
        rotation=32,
        rotation_mode="anchor",
        arrowprops=dict(
            arrowstyle="-",
            color=COLORS[provider],
            alpha=0.4,
            lw=0.7,
        ),
        zorder=6,
    )

# ---------------------------------------------------------------------------
# "Unrealized productivity" label inside the gap
# ---------------------------------------------------------------------------
label_date = datetime.date(2025, 9, 1)
label_x = _date_to_num(label_date)
cap_at_label = float(spline_cap(label_x))
adopt_at_label = float(spline_adopt(label_x))
label_y = (cap_at_label + adopt_at_label) / 2

ax.text(
    label_x, label_y,
    "Unrealized\nproductivity",
    fontsize=10,
    fontfamily="sans-serif",
    fontstyle="italic",
    color="#6B6050",
    ha="center",
    va="center",
    zorder=4,
    alpha=0.85,
)

# ---------------------------------------------------------------------------
# Line labels at right edge (instead of a boxy legend)
# ---------------------------------------------------------------------------
cap_end_x = x_smooth[-1]
cap_end_y = y_cap_smooth[-1]
ax.text(
    cap_end_x + 3, cap_end_y,
    "AI capability",
    fontsize=8.5,
    fontfamily="sans-serif",
    fontweight="bold",
    color=CAPABILITY_LINE_COLOR,
    va="center",
    ha="left",
    zorder=6,
)

adopt_end_y = y_adopt_smooth[-1]
ax.text(
    cap_end_x + 3, adopt_end_y,
    "Enterprise\nadoption",
    fontsize=8.5,
    fontfamily="sans-serif",
    fontweight="bold",
    color=ADOPTION_LINE_COLOR,
    va="center",
    ha="left",
    zorder=6,
)

# ---------------------------------------------------------------------------
# Provider legend (small dots, top-left)
# ---------------------------------------------------------------------------
legend_elements = [
    Line2D([0], [0], marker="o", color="w", markerfacecolor=COLORS["OpenAI"],
           markersize=6, label="OpenAI", linewidth=0),
    Line2D([0], [0], marker="o", color="w", markerfacecolor=COLORS["Anthropic"],
           markersize=6, label="Anthropic", linewidth=0),
    Line2D([0], [0], marker="o", color="w", markerfacecolor=COLORS["Google"],
           markersize=6, label="Google", linewidth=0),
]
ax.legend(
    handles=legend_elements,
    loc="upper left",
    frameon=False,
    fontsize=7,
    handletextpad=0.3,
    labelspacing=0.4,
)

# ---------------------------------------------------------------------------
# Axes formatting
# ---------------------------------------------------------------------------
ax.set_xlim(x_min, _date_to_num(datetime.date(2026, 4, 15)))
ax.set_ylim(-0.05, 1.08)

# X-axis: quarter ticks
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b\n%Y"))
ax.xaxis.set_minor_locator(mdates.MonthLocator())
ax.tick_params(axis="x", labelsize=7, length=3, color="#CCCCCC")
ax.tick_params(axis="x", which="minor", length=0)

# Y-axis: qualitative
ax.set_yticks([0.05, 0.95])
ax.set_yticklabels(["Low", "High"], fontsize=8, fontfamily="sans-serif", color="#888888")
ax.tick_params(axis="y", length=0)

# Spines
for spine in ax.spines.values():
    spine.set_visible(False)
ax.spines["bottom"].set_visible(True)
ax.spines["bottom"].set_color("#CCCCCC")
ax.spines["bottom"].set_linewidth(0.8)

ax.grid(False)

# Title
ax.set_title(
    "The capability-adoption gap",
    fontsize=14,
    fontfamily="sans-serif",
    fontweight="bold",
    color="#2D2D2D",
    pad=18,
    loc="left",
)

# Subtitle
ax.text(
    x_min, 1.12,
    "AI models ship faster than organizations can absorb them",
    fontsize=9,
    fontfamily="sans-serif",
    color="#777777",
    transform=ax.get_xaxis_transform(),
    va="bottom",
    ha="left",
)

plt.tight_layout()
plt.savefig(OUTPUT_PATH, dpi=300, bbox_inches="tight", facecolor="white")
plt.close()

print(f"Chart saved to: {OUTPUT_PATH}")
