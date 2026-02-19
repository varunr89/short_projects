"""
Chart 3: The Capability-Adoption Gap (reworked)
Timeline showing specific capability milestones with "wow factor" descriptions
vs. a corrected adoption curve that starts near 0, rises after ChatGPT launch,
then plateaus around 20-25%.

Selected milestones (8 most impactful):
- Mar 2023: GPT-4 passes bar exam (90th percentile)
- Sep 2023: AI gains "eyes" (GPT-4V)
- May 2024: Real-time voice conversations (GPT-4o)
- Sep 2024: PhD-level reasoning (OpenAI o1)
- Oct 2024: Nobel Prize for AI (AlphaFold)
- Feb 2025: Autonomous coding agents (Claude Code)
- May 2025: Multi-hour autonomous work (Claude Opus 4)
- Feb 2026: Original theoretical physics (GPT-5.2)

Adoption curve shape:
- Before Nov 2022: ~2%
- Nov 2022 - Mar 2023: rapid rise to ~15%
- Mar 2023 - Dec 2023: gradual rise to ~20%
- 2024: flatten ~20-22%
- 2025-2026: plateau ~22-25%

Sources: Bick et al. (2024), Pew Research (Oct 2025)
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

# =============================================================
# CAPABILITY MILESTONES (8 selected)
# =============================================================
milestones = [
    (datetime(2023, 3, 15),  15, 'Passes bar exam\n(90th percentile)',    'GPT-4'),
    (datetime(2023, 9, 15),  25, 'AI gains "eyes"\n(image understanding)', 'GPT-4V'),
    (datetime(2024, 5, 15),  38, 'Real-time voice\nconversations',         'GPT-4o'),
    (datetime(2024, 9, 15),  50, 'PhD-level\nreasoning',                   'o1'),
    (datetime(2024, 10, 15), 60, 'Nobel Prize\nfor AI discovery',          'AlphaFold'),
    (datetime(2025, 2, 15),  72, 'Autonomous\ncoding agents',              'Claude Code'),
    (datetime(2025, 5, 15),  83, 'Multi-hour\nautonomous work',            'Opus 4'),
    (datetime(2026, 2, 10),  96, 'Original theoretical\nphysics',          'GPT-5.2'),
]

milestones.sort(key=lambda m: m[0])

# --- Build staircase line for capability ---
start_date = datetime(2022, 7, 1)
end_date = datetime(2026, 5, 1)

stair_dates = []
stair_levels = []

# Start low before first milestone
stair_dates.append(start_date)
stair_levels.append(5)
stair_dates.append(milestones[0][0])
stair_levels.append(5)

for i, (date, level, label, model) in enumerate(milestones):
    # Vertical jump
    stair_dates.append(date)
    stair_levels.append(level)
    # Flat until next milestone
    if i < len(milestones) - 1:
        stair_dates.append(milestones[i + 1][0])
        stair_levels.append(level)
    else:
        stair_dates.append(end_date)
        stair_levels.append(level)

stair_dates_num = mdates.date2num(stair_dates)

# Plot capability staircase
ax.plot(stair_dates_num, stair_levels, color='#2563eb', linewidth=2.5,
        zorder=3, label='AI capability')
ax.fill_between(stair_dates_num, 0, stair_levels, alpha=0.04, color='#2563eb',
                zorder=1)

# Milestone dots
for date, level, label, model in milestones:
    ax.plot(mdates.date2num(date), level, 'o', color='#2563eb',
            markersize=6, zorder=5, markeredgecolor='white', markeredgewidth=1.2)

# --- Label milestones ---
# Manually tuned offsets: (x_pts, y_pts, ha, va)
# Careful spacing to avoid overlaps, especially for the Sep/Oct 2024 cluster
label_offsets = [
    (12,   8,  'left',  'bottom'),   # GPT-4 bar exam -- above, right
    (-12,  8,  'right', 'bottom'),   # GPT-4V eyes -- above, left
    (12,   8,  'left',  'bottom'),   # GPT-4o voice -- above, right
    (-15,  8,  'right', 'bottom'),   # o1 PhD reasoning -- left to avoid AlphaFold
    (12,   5,  'left',  'bottom'),   # AlphaFold Nobel -- right
    (-12,  8,  'right', 'bottom'),   # Claude Code -- left
    (12,   5,  'left',  'bottom'),   # Opus 4 -- right
    (12,   5,  'left',  'bottom'),   # GPT-5.2 physics -- right, above
]

for i, (date, level, label, model) in enumerate(milestones):
    date_num = mdates.date2num(date)
    x_off, y_off, ha, va = label_offsets[i]

    # Model name in bold, description below
    display_text = f'{model}: {label}'

    ax.annotate(display_text,
                xy=(date_num, level),
                xytext=(x_off, y_off),
                textcoords='offset points',
                fontsize=7, color='#333333', ha=ha, va=va,
                fontweight='medium',
                arrowprops=dict(arrowstyle='-', color='#cccccc', lw=0.6),
                zorder=6)

# =============================================================
# ADOPTION CURVE (corrected shape)
# =============================================================
# Key data points for the adoption curve:
# - Before Nov 2022: ~2% (early AI adopters, researchers)
# - Nov 2022 (ChatGPT launch): begins rising
# - Mar 2023: ~15% (rapid initial uptake)
# - Dec 2023: ~20%
# - Aug 2024: ~23% (Bick et al.)
# - Oct 2025: ~21% (Pew Research)
# - Feb 2026: ~23%

# Create smooth adoption curve using interpolated points
adopt_dates = [
    datetime(2022, 7, 1),   # start of chart
    datetime(2022, 10, 1),  # pre-ChatGPT
    datetime(2022, 11, 30), # ChatGPT launch
    datetime(2023, 1, 15),  # rapid rise
    datetime(2023, 3, 15),  # GPT-4 hype
    datetime(2023, 6, 1),   # settling
    datetime(2023, 12, 1),  # end of year
    datetime(2024, 3, 1),   # Q1 2024
    datetime(2024, 8, 1),   # Bick et al.
    datetime(2025, 1, 1),   # 2025 start
    datetime(2025, 10, 1),  # Pew Research
    datetime(2026, 2, 15),  # current
    datetime(2026, 5, 1),   # end of chart
]
adopt_values = [
    2,     # pre-ChatGPT baseline
    2,     # still pre-ChatGPT
    3,     # ChatGPT just launched
    10,    # rapid uptake
    15,    # GPT-4 wave
    18,    # settling
    20,    # end 2023
    21,    # gradual
    23,    # Bick et al. data point
    22,    # slight dip
    21,    # Pew data point
    23,    # slight recovery
    23,    # plateau
]

adopt_dates_num = [mdates.date2num(d) for d in adopt_dates]

# Smooth interpolation using numpy (no scipy dependency)
adopt_x_fine = np.linspace(adopt_dates_num[0], adopt_dates_num[-1], 500)
adopt_y_fine = np.interp(adopt_x_fine, adopt_dates_num, adopt_values)
# Clip to reasonable range
adopt_y_fine = np.clip(adopt_y_fine, 0, 30)
ax.plot(adopt_x_fine, adopt_y_fine, color='#dc2626', linewidth=2.2,
        zorder=3, label='AI adoption rate')

# Data point markers for cited research
cited_points = [
    (datetime(2024, 8, 1),  23, '~23%\nBick et al. (2024)'),
    (datetime(2025, 10, 1), 21, '~21%\nPew (Oct 2025)'),
]
for date, value, cite_label in cited_points:
    date_num = mdates.date2num(date)
    ax.plot(date_num, value, 's', color='#dc2626', markersize=7,
            zorder=5, markeredgecolor='white', markeredgewidth=1)
    ax.annotate(cite_label,
                xy=(date_num, value),
                xytext=(0, -25), textcoords='offset points',
                fontsize=7, color='#dc2626', ha='center', va='top',
                fontweight='medium')

# ChatGPT launch marker
chatgpt_date = mdates.date2num(datetime(2022, 11, 30))
ax.axvline(x=chatgpt_date, color='#999999', linewidth=0.8, linestyle=':', zorder=2)
ax.annotate('ChatGPT\nlaunches',
            xy=(chatgpt_date, 3),
            xytext=(-8, 12), textcoords='offset points',
            fontsize=7, color='#999999', ha='right', va='bottom',
            fontstyle='italic')

# =============================================================
# SHADE THE WIDENING GAP
# =============================================================
# Create staircase values at the fine x positions for fill_between
stair_interp = np.interp(adopt_x_fine, stair_dates_num, stair_levels)

# Fill gap between capability and adoption where capability > adoption
ax.fill_between(adopt_x_fine, adopt_y_fine, stair_interp,
                where=(stair_interp > adopt_y_fine),
                alpha=0.06, color='#dc2626', interpolate=True, zorder=1)

# Gap annotation with double arrow
gap_date = datetime(2025, 12, 1)
gap_date_num = mdates.date2num(gap_date)
gap_cap_level = np.interp(gap_date_num, stair_dates_num, stair_levels)
gap_adopt_level = float(np.interp(gap_date_num, adopt_x_fine, adopt_y_fine))

ax.annotate('',
            xy=(gap_date_num, gap_adopt_level + 1),
            xytext=(gap_date_num, gap_cap_level - 1),
            arrowprops=dict(arrowstyle='<->', color='#dc2626', lw=1.5,
                            shrinkA=0, shrinkB=0),
            zorder=6)
ax.text(gap_date_num + 10, (gap_adopt_level + gap_cap_level) / 2,
        'Widening\ngap', fontsize=9, color='#dc2626',
        fontweight='bold', fontstyle='italic', ha='left', va='center')

# =============================================================
# AXES AND STYLING
# =============================================================
ax.set_xlim(mdates.date2num(datetime(2022, 7, 1)),
            mdates.date2num(datetime(2026, 5, 1)))
ax.set_ylim(-8, 105)

# X-axis: semi-annual ticks
ax.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b\n%Y'))
ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[4, 10]))

# Y-axis: conceptual, no numeric ticks
ax.set_ylabel('AI Capability / Adoption (%)', fontsize=11, labelpad=10)
ax.set_yticks([])
ax.spines['left'].set_visible(False)

# Legend
ax.legend(loc='upper left', frameon=False, fontsize=10)

# Title and subtitle
fig.suptitle('The Capability-Adoption Gap', fontsize=16, fontweight='bold',
             x=0.12, ha='left', y=0.97)
ax.set_title('AI capability has transformed in 3 years. Adoption has barely moved.',
             fontsize=10, color='#666666', loc='left', pad=12)

plt.tight_layout(rect=[0, 0.05, 1, 0.93])

# Source citations as figure caption
fig.text(0.5, 0.01,
         'Sources: Bick et al. (2024), Pew Research (Oct 2025). '
         'Capability milestones from OpenAI, Anthropic, Google DeepMind.',
         fontsize=7.5, color='#999999', ha='center', va='bottom')

plt.savefig('/Users/varunr/projects/short_projects/ai-productivity-gap/charts/03_capability_adoption_gap.png',
            dpi=200, bbox_inches='tight', facecolor='white')
print('Saved charts/03_capability_adoption_gap.png')
