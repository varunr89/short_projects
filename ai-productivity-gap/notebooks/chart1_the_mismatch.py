"""
Chart 1: The Mismatch
Two overlaid curves showing AI adoption rate vs AI productivity gain by employee percentile.
The lines cross, showing adoption and impact are inversely correlated.

Data grounding:
- Adoption: Bick et al. (2024) ~20% non-college vs ~40% college; Dropbox 59% vs 73% by performance
- Productivity gain: Brynjolfsson (+35% bottom quintile, ~0% top); Dell'Acqua/BCG (+43% below-avg, +17% above-avg)
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

percentile = np.linspace(0, 100, 200)

# AI Adoption Rate curve (rises with percentile)
# Bottom performers: ~15-20% adoption, top performers: ~60-73%
# Smooth sigmoid-like curve grounded in Bick et al + Dropbox data
adoption = 15 + 55 * (1 / (1 + np.exp(-0.06 * (percentile - 55))))

# AI Productivity Gain curve (falls with percentile)
# Bottom performers: ~35-43% gain, top performers: ~5-17%
# Grounded in Brynjolfsson (bottom +35%, top ~0%) and Dell'Acqua (bottom +43%, top +17%)
gain = 42 - 30 * (1 / (1 + np.exp(-0.06 * (percentile - 45))))

# Plot the curves
line_adoption, = ax.plot(percentile, adoption, color='#2563eb', linewidth=2.5,
                         label='AI adoption rate', zorder=3)
line_gain, = ax.plot(percentile, gain, color='#dc2626', linewidth=2.5,
                     label='AI productivity gain', zorder=3)

# Fill the area between to highlight the mismatch
# Red region: gain > adoption (left side -- high potential, low usage)
ax.fill_between(percentile, gain, adoption,
                where=(gain >= adoption), alpha=0.12, color='#dc2626',
                interpolate=True, label='_nolegend_')
# Blue region: adoption > gain (right side -- high usage, low return)
ax.fill_between(percentile, adoption, gain,
                where=(adoption >= gain), alpha=0.12, color='#2563eb',
                interpolate=True, label='_nolegend_')

# Find and mark the crossover point
cross_idx = np.argmin(np.abs(adoption - gain))
cross_x = percentile[cross_idx]
cross_y = adoption[cross_idx]

# Prominent crossover marker
ax.plot(cross_x, cross_y, 'o', color='#1a1a1a', markersize=8, zorder=6,
        markeredgecolor='white', markeredgewidth=1.5)

# Crossover label with a box
ax.annotate(f'Crossover ~{int(round(cross_x))}th percentile',
            xy=(cross_x, cross_y),
            xytext=(cross_x + 14, cross_y + 10),
            fontsize=9.5, fontweight='bold', color='#1a1a1a',
            ha='center', va='bottom',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#f5f5f5',
                      edgecolor='#cccccc', linewidth=0.8),
            arrowprops=dict(arrowstyle='->', color='#666666', lw=1.2,
                            connectionstyle='arc3,rad=-0.15'),
            zorder=7)

# Region annotations
ax.annotate('High potential gain\nLow adoption',
            xy=(12, 37), fontsize=10, color='#dc2626', fontstyle='italic',
            fontweight='medium', ha='left', va='center')
ax.annotate('High adoption\nLow gain',
            xy=(78, 57), fontsize=10, color='#2563eb', fontstyle='italic',
            fontweight='medium', ha='center', va='center')

# (Source citation moved to figure caption below the plot)

# Labels
ax.set_xlabel('Employee Percentile (by baseline performance)', fontsize=11, labelpad=10)
ax.set_ylabel('Percentage (%)', fontsize=11, labelpad=10)
ax.set_xlim(0, 100)
ax.set_ylim(0, 75)
ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xticklabels(['0th', '25th', '50th', '75th', '100th'])

# Legend
ax.legend(loc='upper left', frameon=False, fontsize=10)

# Title and subtitle
fig.suptitle('The Mismatch', fontsize=16, fontweight='bold', x=0.12, ha='left', y=0.97)
ax.set_title('AI adoption is highest where productivity gains are smallest',
             fontsize=10.5, color='#666666', loc='left', pad=12)

plt.tight_layout(rect=[0, 0.05, 1, 0.93])

# Source citations as figure caption below the chart
fig.text(0.5, 0.01,
         'Sources: Brynjolfsson et al. (2023), BCG/Harvard (Dell\'Acqua et al., 2023), Bick et al. (2024), Dropbox (2024)',
         fontsize=7.5, color='#999999', ha='center', va='bottom')

plt.savefig('/Users/varunr/projects/short_projects/ai-productivity-gap/charts/01_the_mismatch.png',
            dpi=200, bbox_inches='tight', facecolor='white')
print('Saved charts/01_the_mismatch.png')
