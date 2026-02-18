"""
Chart 3: The Capability-Adoption Gap
Timeline from mid-2023 to early 2026 showing capability milestones as a rising
staircase vs. a flat adoption line around 20-25%.

The visual story: capability rockets upward, adoption stays flat. The gap widens.

Data grounding:
- Capability milestones: see data/research_capability_milestones.md
- Adoption data: Bick et al. (Aug 2024) ~23%, Pew Research (Oct 2025) ~21%
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime

# --- Shared style ---
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 11,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'text.color': '#1a1a1a',
    'axes.labelcolor': '#1a1a1a',
    'xtick.color': '#666666',
    'ytick.color': '#666666',
})

fig, ax = plt.subplots(figsize=(10, 6))

# --- Capability milestones (curated 9 most dramatic) ---
# Each: (date, capability_level 0-100, label, label_side)
# Curated to 8 milestones -- combined the Oct 2024 cluster into one entry
milestones = [
    (datetime(2023, 3, 15),  10, 'Passes bar exam\n(90th percentile)', 'right'),
    (datetime(2024, 5, 15),  25, 'Real-time voice +\nvision conversation', 'right'),
    (datetime(2024, 9, 15),  40, 'PhD-level science\nbenchmarks', 'left'),
    (datetime(2024, 10, 15), 52, 'Computer use +\nNobel for AI discovery', 'right'),
    (datetime(2025, 2, 15),  62, 'Autonomous\ncoding agents', 'right'),
    (datetime(2025, 8, 15),  76, 'Near-perfect\ncompetition math', 'left'),
    (datetime(2025, 9, 15),  85, '30+ hour autonomous\ncoding sessions', 'right'),
    (datetime(2026, 2, 10),  96, 'Original physics\ndiscovery', 'right'),
]

# --- Build staircase line ---
# Sort by date
milestones.sort(key=lambda m: m[0])

# Create staircase: flat at each level, then jump to next
stair_dates = []
stair_levels = []

# Start from the left edge at level 0
start_date = datetime(2023, 1, 1)
stair_dates.append(start_date)
stair_levels.append(milestones[0][2] if False else 5)  # start low
stair_dates.append(milestones[0][0])
stair_levels.append(5)

for i, (date, level, label, side) in enumerate(milestones):
    # Vertical jump
    stair_dates.append(date)
    stair_levels.append(level)
    # Flat until next milestone (or end)
    if i < len(milestones) - 1:
        stair_dates.append(milestones[i + 1][0])
        stair_levels.append(level)
    else:
        end_date = datetime(2026, 4, 1)
        stair_dates.append(end_date)
        stair_levels.append(level)

# Convert to matplotlib dates
stair_dates_num = mdates.date2num(stair_dates)

# Plot capability staircase
ax.plot(stair_dates_num, stair_levels, color='#2563eb', linewidth=2.5,
        zorder=3, label='AI capability')

# Fill under the staircase lightly
ax.fill_between(stair_dates_num, 0, stair_levels, alpha=0.04, color='#2563eb',
                zorder=1)

# Plot milestone dots
for date, level, label, side in milestones:
    ax.plot(mdates.date2num(date), level, 'o', color='#2563eb',
            markersize=6, zorder=5, markeredgecolor='white', markeredgewidth=1)

# --- Label milestones with per-milestone positioning ---
# (x_offset_pts, y_offset_pts, ha, va) tuned to avoid overlaps
label_positions = {
    'Passes bar exam':        (15,   3, 'left', 'bottom'),
    'Real-time voice':        (-120, -15, 'left', 'top'),
    'PhD-level science':      (-120, 8,  'left', 'bottom'),
    'Computer use':           (15,   5, 'left', 'bottom'),
    'Autonomous\ncoding':     (15,   3, 'left', 'bottom'),
    'Near-perfect':           (-15,  3, 'right', 'bottom'),
    '30+ hour':               (15,   3, 'left', 'bottom'),
    'Original physics':       (15,   3, 'left', 'bottom'),
}

for i, (date, level, label, side) in enumerate(milestones):
    date_num = mdates.date2num(date)

    # Find matching position override by checking if label starts with a key
    x_off, y_off, ha, va = 15, 4, 'left', 'bottom'
    for key, (xo, yo, h, v) in label_positions.items():
        if label.startswith(key):
            x_off, y_off, ha, va = xo, yo, h, v
            break

    ax.annotate(label,
                xy=(date_num, level),
                xytext=(x_off, y_off),
                textcoords='offset points',
                fontsize=7.5, color='#333333', ha=ha, va=va,
                arrowprops=dict(arrowstyle='-', color='#cccccc', lw=0.6),
                zorder=6)

# --- Adoption line (flat) ---
adoption_points = [
    (datetime(2024, 8, 1), 23, 'Bick et al.\n(Aug 2024)'),
    (datetime(2025, 10, 1), 21, 'Pew Research\n(Oct 2025)'),
]

# Draw the flat adoption line across full range
adopt_x_start = mdates.date2num(datetime(2023, 1, 1))
adopt_x_end = mdates.date2num(datetime(2026, 4, 1))

# Slight connection between the two data points to show the flatness
adopt_dates_num = [mdates.date2num(d) for d, _, _ in adoption_points]
adopt_values = [v for _, v, _ in adoption_points]

# Extended flat line
ax.plot([adopt_x_start, adopt_x_end], [22, 22], color='#dc2626',
        linewidth=2, linestyle='-', alpha=0.7, zorder=3, label='AI adoption rate')

# Adoption data point markers
for date, value, cite_label in adoption_points:
    date_num = mdates.date2num(date)
    ax.plot(date_num, value, 's', color='#dc2626', markersize=7,
            zorder=5, markeredgecolor='white', markeredgewidth=1)

# Adoption citations
ax.annotate('~23%\nBick et al. (2024)',
            xy=(mdates.date2num(datetime(2024, 8, 1)), 23),
            xytext=(0, -28), textcoords='offset points',
            fontsize=7.5, color='#dc2626', ha='center', va='top',
            fontweight='medium')

ax.annotate('~21%\nPew (Oct 2025)',
            xy=(mdates.date2num(datetime(2025, 10, 1)), 21),
            xytext=(0, -28), textcoords='offset points',
            fontsize=7.5, color='#dc2626', ha='center', va='top',
            fontweight='medium')

# --- Shade the widening gap ---
# Between the capability staircase and the adoption line
ax.fill_between(stair_dates_num, 22, stair_levels,
                where=[s > 22 for s in stair_levels],
                alpha=0.06, color='#dc2626', interpolate=True, zorder=1)

# Gap annotation arrow
gap_date = datetime(2025, 11, 1)
gap_date_num = mdates.date2num(gap_date)
# Find staircase level at this date
gap_cap_level = 83  # approximate level at this date
ax.annotate('',
            xy=(gap_date_num, 22),
            xytext=(gap_date_num, gap_cap_level),
            arrowprops=dict(arrowstyle='<->', color='#dc2626', lw=1.5,
                            shrinkA=2, shrinkB=2),
            zorder=6)
ax.text(gap_date_num + 12, (22 + gap_cap_level) / 2,
        'Widening\ngap', fontsize=9, color='#dc2626',
        fontweight='bold', fontstyle='italic', ha='left', va='center',
        transform=ax.transData)

# --- Axes ---
ax.set_xlim(mdates.date2num(datetime(2023, 1, 1)),
            mdates.date2num(datetime(2026, 4, 1)))
ax.set_ylim(-8, 105)

# X-axis: quarterly ticks
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[4, 10]))

# Y-axis: qualitative
ax.set_ylabel('AI Capability', fontsize=11, labelpad=10)
ax.set_yticks([])  # no numeric ticks -- conceptual index

# Hide left spine since no y-axis numbers
ax.spines['left'].set_visible(False)

# Legend
ax.legend(loc='upper left', frameon=False, fontsize=10)

# Title
fig.suptitle('The Capability-Adoption Gap', fontsize=16, fontweight='bold',
             x=0.12, ha='left', y=0.97)
ax.set_title('AI capability has transformed in 3 years. Adoption has barely moved.',
             fontsize=10, color='#666666', loc='left', pad=12)

plt.tight_layout(rect=[0, 0.01, 1, 0.93])
plt.savefig('/Users/varunr/projects/short_projects/ai-productivity-gap/charts/03_capability_adoption_gap.png',
            dpi=200, bbox_inches='tight', facecolor='white')
print('Saved charts/03_capability_adoption_gap.png')
