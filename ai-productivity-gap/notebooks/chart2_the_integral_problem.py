"""
Chart 2: The Integral Problem (research-accurate)
Before/after productivity curves where the "after" curve reflects BOTH
adoption rates AND gain magnitudes per percentile.

Key insight: The "after" curve lifts more on the left (big gains) but only for
the few who adopt. The right side lifts less (small gains) despite more adoption.
The total shaded area (realized gain) is small vs. the theoretical maximum.

Data grounding:
- Baseline productivity: standard distribution
- Bottom performers: +35-43% gain, ~20% adoption rate
- Top performers: +7-17% gain, ~40-73% adoption rate
- Realized gain at each point = gain_magnitude * adoption_rate
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

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

percentile = np.linspace(0, 100, 500)

# Baseline productivity curve (before AI)
# Roughly log-normal-ish: slow rise, then steeper at the top
baseline = 20 + 60 * (percentile / 100) ** 1.4

# Individual gain if using AI (decreases with percentile)
# Bottom: +40%, Top: +10%
individual_gain_pct = 40 - 28 * (percentile / 100) ** 0.8

# Adoption rate (increases with percentile)
# Bottom: ~15%, Top: ~65%
adoption_rate = 15 + 50 * (percentile / 100) ** 1.2

# Realized gain = baseline * (individual_gain_pct/100) * (adoption_rate/100)
realized_gain = baseline * (individual_gain_pct / 100) * (adoption_rate / 100)

# "After AI" curve = baseline + realized gain
after_ai = baseline + realized_gain

# Theoretical maximum (if everyone adopted)
theoretical_gain = baseline * (individual_gain_pct / 100)
theoretical_after = baseline + theoretical_gain

# Compute the "only X% realized" stat
total_theoretical_area = np.trapezoid(theoretical_gain, percentile)
total_realized_area = np.trapezoid(realized_gain, percentile)
pct_realized = total_realized_area / total_theoretical_area * 100

# Plot curves
ax.plot(percentile, baseline, color='#888888', linewidth=2, label='Before AI',
        linestyle='-', zorder=3)
ax.plot(percentile, after_ai, color='#2563eb', linewidth=2.5,
        label='After AI (realized)', zorder=4)
ax.plot(percentile, theoretical_after, color='#dc2626', linewidth=2,
        label='After AI (if everyone adopted)', linestyle='--', alpha=0.7, zorder=3)

# Shade realized gain (small blue area)
ax.fill_between(percentile, baseline, after_ai, alpha=0.20, color='#2563eb',
                label='_nolegend_', zorder=2)

# Shade unrealized gain (large red area)
ax.fill_between(percentile, after_ai, theoretical_after, alpha=0.15, color='#dc2626',
                label='_nolegend_', zorder=2)

# --- Annotations ---

# Realized gain label (positioned inside the blue area, right side where band is wider)
mid_blue_idx = 400  # ~80th percentile where blue band is most visible
mid_blue_y = (baseline[mid_blue_idx] + after_ai[mid_blue_idx]) / 2
ax.annotate('Realized\ngain',
            xy=(percentile[mid_blue_idx], mid_blue_y),
            fontsize=9.5, color='#2563eb', fontweight='medium',
            fontstyle='italic', ha='center', va='center')

# Unrealized gain label (positioned inside the red area, right side where it's widest)
mid_red_idx = 380  # ~76th percentile
mid_red_y = (after_ai[mid_red_idx] + theoretical_after[mid_red_idx]) / 2
ax.annotate('Unrealized\ngain',
            xy=(percentile[mid_red_idx], mid_red_y),
            fontsize=9.5, color='#dc2626', fontweight='medium',
            fontstyle='italic', ha='center', va='center')

# Percentage annotation with box (top-right area, clear of curves)
ax.annotate(f'Only {pct_realized:.0f}% of potential\nproductivity gain realized',
            xy=(65, theoretical_after[325]),
            xytext=(35, theoretical_after[400] + 5),
            fontsize=10, fontweight='bold', color='#1a1a1a',
            ha='center', va='bottom',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#fff3f3',
                      edgecolor='#dc2626', linewidth=0.8, alpha=0.9),
            arrowprops=dict(arrowstyle='->', color='#dc2626', lw=1,
                            connectionstyle='arc3,rad=-0.2'),
            zorder=6)

# Data callouts with arrows -- position text further away from curves
ax.annotate('Bottom quintile:\n+35% gain, but only ~20% adopt',
            xy=(10, after_ai[20]),
            xytext=(25, theoretical_after[0] + 18),
            fontsize=7.5, color='#888888',
            arrowprops=dict(arrowstyle='->', color='#bbbbbb', lw=0.8,
                            connectionstyle='arc3,rad=0.15'))

ax.annotate('Top quintile:\n+7-17% gain, ~60-73% adopt',
            xy=(92, after_ai[460]),
            xytext=(80, after_ai[480] + 12),
            fontsize=7.5, color='#888888',
            arrowprops=dict(arrowstyle='->', color='#bbbbbb', lw=0.8,
                            connectionstyle='arc3,rad=-0.15'))

# Source citation -- bottom-right where there's space
ax.text(98, baseline[0] - 4,
        'Brynjolfsson et al. (2023), Dell\'Acqua et al. (2023), Bick et al. (2024)',
        fontsize=7, color='#aaaaaa', ha='right', va='top')

# Labels
ax.set_xlabel('Employee Percentile (by baseline performance)', fontsize=11, labelpad=10)
ax.set_ylabel('Productivity', fontsize=11, labelpad=10)
ax.set_xlim(0, 100)
ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xticklabels(['0th', '25th', '50th', '75th', '100th'])
ax.set_yticks([])  # Qualitative y-axis

# Legend
ax.legend(loc='upper left', frameon=False, fontsize=9.5)

# Title
fig.suptitle('The Integral Problem', fontsize=16, fontweight='bold',
             x=0.12, ha='left', y=0.97)
ax.set_title('Total output = area under the curve. '
             'The gap between realized and potential is enormous.',
             fontsize=10, color='#666666', loc='left', pad=12)

plt.tight_layout(rect=[0, 0.01, 1, 0.93])
plt.savefig('/Users/varunr/projects/short_projects/ai-productivity-gap/charts/02_the_integral_problem.png',
            dpi=200, bbox_inches='tight', facecolor='white')
print(f'Saved charts/02_the_integral_problem.png (realized: {pct_realized:.1f}%)')
