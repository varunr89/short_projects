"""
Chart 2: The Integral Problem (area chart rework)
Filled area chart showing three zones:
  1. Baseline productivity (gray)
  2. Realized gains (small blue area -- only where people actually adopt)
  3. Unrealized potential (large red area -- the gap)

The productivity curve follows a power-law distribution (right-skewed),
reflecting that top performers have disproportionately high output.

The "after AI" realized curve shows small uplift on the right (high adopters,
low gain per person) and almost nothing on the left (high potential gain,
but very low adoption). The theoretical "if everyone adopted" curve shows
the full potential -- making the gap visually obvious.

Data grounding:
- Baseline productivity: power-law / right-skewed distribution
- Bottom performers: +35-43% gain, ~15-20% adoption
- Top performers: +7-17% gain, ~60-73% adoption
- Sources: Brynjolfsson et al. (2023), Dell'Acqua et al. (2023), Bick et al. (2024)
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
t = percentile / 100  # normalized 0-1

# --- Baseline productivity: power-law / right-skewed ---
# Follows a convex curve -- most employees cluster at moderate output,
# top performers have disproportionately high output.
baseline = 15 + 85 * (t ** 2.2)

# --- Individual gain if using AI (decreases with percentile) ---
# Bottom quintile: ~40% gain (Brynjolfsson +35%, Dell'Acqua +43%)
# Top quintile: ~10% gain (Brynjolfsson ~0%, Dell'Acqua +17%, average ~10%)
individual_gain_pct = 40 - 30 * (t ** 0.7)

# --- Adoption rate (increases with percentile) ---
# Bottom: ~15%, Top: ~65% (Bick et al. ~20-40%, Dropbox 59-73%)
adoption_rate = 15 + 50 * (t ** 1.3)

# --- Realized gain = baseline * gain% * adoption% ---
realized_gain = baseline * (individual_gain_pct / 100) * (adoption_rate / 100)

# --- Theoretical gain (if 100% adopted) ---
theoretical_gain = baseline * (individual_gain_pct / 100)

# Curves
after_ai = baseline + realized_gain
theoretical_after = baseline + theoretical_gain

# --- Compute percentage realized ---
total_theoretical_area = np.trapezoid(theoretical_gain, percentile)
total_realized_area = np.trapezoid(realized_gain, percentile)
pct_realized = total_realized_area / total_theoretical_area * 100

# --- Plot filled areas (bottom to top) ---

# 1. Baseline productivity (gray fill)
ax.fill_between(percentile, 0, baseline, alpha=0.08, color='#888888', zorder=1)
ax.plot(percentile, baseline, color='#888888', linewidth=2, label='Baseline (before AI)',
        zorder=3)

# 2. Realized gains (blue fill between baseline and after_ai)
ax.fill_between(percentile, baseline, after_ai, alpha=0.30, color='#2563eb',
                label='Realized gain', zorder=2)

# 3. Unrealized potential (red fill between after_ai and theoretical_after)
ax.fill_between(percentile, after_ai, theoretical_after, alpha=0.20, color='#dc2626',
                label='Unrealized potential', zorder=2)

# Top boundary line -- theoretical max
ax.plot(percentile, theoretical_after, color='#dc2626', linewidth=1.8,
        linestyle='--', alpha=0.7, zorder=3, label='If everyone adopted')

# After AI realized line
ax.plot(percentile, after_ai, color='#2563eb', linewidth=2.2, zorder=4)

# --- Annotations ---

# Label the realized gain area -- place in the blue band on the far right
# where the band is widest and clearly visible
idx_85 = int(0.85 * len(percentile))
realized_mid_y = (baseline[idx_85] + after_ai[idx_85]) / 2
ax.annotate('Realized\ngain',
            xy=(percentile[idx_85], realized_mid_y),
            fontsize=10, color='#2563eb', fontweight='bold',
            fontstyle='italic', ha='center', va='center', zorder=6)

# Label the unrealized potential area -- place in the red band, offset from blue label
idx_70 = int(0.70 * len(percentile))
unrealized_mid_y = (after_ai[idx_70] + theoretical_after[idx_70]) / 2
ax.annotate('Unrealized\npotential',
            xy=(percentile[idx_70], unrealized_mid_y),
            fontsize=10, color='#dc2626', fontweight='bold',
            fontstyle='italic', ha='center', va='center', zorder=6)

# Percentage callout box -- position in the upper right area, clear of legend
idx_arrow = int(0.55 * len(percentile))
ax.annotate(f'Only {pct_realized:.0f}% of potential\nproductivity gain realized',
            xy=(percentile[idx_arrow],
                (after_ai[idx_arrow] + theoretical_after[idx_arrow]) / 2),
            xytext=(72, theoretical_after[-1] * 0.92),
            fontsize=10.5, fontweight='bold', color='#1a1a1a',
            ha='center', va='bottom',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#fff3f3',
                      edgecolor='#dc2626', linewidth=1, alpha=0.95),
            arrowprops=dict(arrowstyle='->', color='#dc2626', lw=1.2,
                            connectionstyle='arc3,rad=0.2'),
            zorder=7)

# --- Axes ---
ax.set_xlabel('Employee Percentile (by baseline performance)', fontsize=11, labelpad=10)
ax.set_ylabel('Productivity Output', fontsize=11, labelpad=10)
ax.set_xlim(0, 100)
ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xticklabels(['0th', '25th', '50th', '75th', '100th'])
ax.set_yticks([])  # qualitative y-axis

# Legend
ax.legend(loc='upper left', frameon=False, fontsize=9.5)

# Title and subtitle
fig.suptitle('The Integral Problem', fontsize=16, fontweight='bold',
             x=0.12, ha='left', y=0.97)
ax.set_title('Total output = area under the curve. We are capturing only a fraction of the potential.',
             fontsize=10, color='#666666', loc='left', pad=12)

plt.tight_layout(rect=[0, 0.05, 1, 0.93])

# Source citations as figure caption below the chart
fig.text(0.5, 0.01,
         'Sources: Brynjolfsson et al. (2023), Dell\'Acqua et al. / BCG-Harvard (2023), Bick et al. (2024)',
         fontsize=7.5, color='#999999', ha='center', va='bottom')

plt.savefig('/Users/varunr/projects/short_projects/ai-productivity-gap/charts/02_the_integral_problem.png',
            dpi=200, bbox_inches='tight', facecolor='white')
print(f'Saved charts/02_the_integral_problem.png (realized: {pct_realized:.1f}%)')
