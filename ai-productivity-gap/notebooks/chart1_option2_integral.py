"""
Chart Option 2: The Integral Problem (research-accurate)
Before/after productivity curves where the "after" curve reflects BOTH
adoption rates AND gain magnitudes per percentile.

Key insight: The "after" curve lifts more on the left (big gains) but only for
the few who adopt. The right side lifts less (small gains) despite more adoption.
The total shaded area (realized gain) is small.

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

plt.rcParams.update({
    'font.family': 'system-ui, -apple-system, sans-serif',
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
# This models: at each percentile, only adoption_rate% of workers use AI,
# and those who do get individual_gain_pct% improvement
realized_gain = baseline * (individual_gain_pct / 100) * (adoption_rate / 100)

# "After AI" curve = baseline + realized gain
after_ai = baseline + realized_gain

# Theoretical maximum (if everyone adopted)
theoretical_gain = baseline * (individual_gain_pct / 100)
theoretical_after = baseline + theoretical_gain

# Plot
ax.plot(percentile, baseline, color='#888888', linewidth=2, label='Before AI', linestyle='-')
ax.plot(percentile, after_ai, color='#2563eb', linewidth=2.5, label='After AI (realized)')
ax.plot(percentile, theoretical_after, color='#2563eb', linewidth=1.5, label='After AI (if everyone adopted)',
        linestyle='--', alpha=0.5)

# Shade realized gain (small)
ax.fill_between(percentile, baseline, after_ai, alpha=0.15, color='#2563eb', label='_nolegend_')

# Shade unrealized gain (large)
ax.fill_between(percentile, after_ai, theoretical_after, alpha=0.08, color='#dc2626', label='_nolegend_')

# Annotations
# Find a good spot to label the realized gain
mid_idx = 350  # around 70th percentile
ax.annotate('Realized gain',
            xy=(percentile[mid_idx], (baseline[mid_idx] + after_ai[mid_idx]) / 2),
            fontsize=9, color='#2563eb', fontstyle='italic', ha='center')

ax.annotate('Unrealized gain',
            xy=(percentile[250], (after_ai[250] + theoretical_after[250]) / 2),
            fontsize=9, color='#dc2626', fontstyle='italic', ha='center')

# Add data callouts
ax.annotate('Bottom quintile:\n+35% gain, but only 20% adopt',
            xy=(10, after_ai[20]),
            xytext=(18, theoretical_after[20] + 8),
            fontsize=7.5, color='#888888',
            arrowprops=dict(arrowstyle='->', color='#cccccc', lw=0.8))

ax.annotate('Top quintile:\n+7-17% gain, 60-73% adopt',
            xy=(90, after_ai[450]),
            xytext=(72, after_ai[450] + 6),
            fontsize=7.5, color='#888888',
            arrowprops=dict(arrowstyle='->', color='#cccccc', lw=0.8))

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
fig.suptitle('The Integral Problem', fontsize=16, fontweight='bold', x=0.12, ha='left', y=0.97)
ax.set_title('Organizational output = area under the curve. The gap between realized and potential is enormous.',
             fontsize=9.5, color='#666666', loc='left', pad=12)

plt.tight_layout(rect=[0, 0, 1, 0.93])
plt.savefig('/Users/varunr/projects/short_projects/ai-productivity-gap/charts/option2_integral.png',
            dpi=200, bbox_inches='tight', facecolor='white')
print('Saved option2_integral.png')
