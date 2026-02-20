"""
Chart 2: The Integral Problem -- three-curve visualization

Three lines across employee percentiles:
  1. Baseline productivity (power-law)
  2. With current AI adoption (barely differs from baseline)
  3. If everyone adopted AI (massive lift at bottom, converges to baseline at top)

Key: individual gain from AI approaches 0 at the top (top performers
don't gain much). All three lines converge at the 100th percentile.
The unrealized potential is entirely on the left side.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

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
t = percentile / 100

# --- Line 1: Baseline (power-law) ---
baseline = 12 + 88 * (t ** 2.5)

# --- Individual gain from AI ---
# Bottom: ~800% (9x). Drops to 0% at 100th percentile.
# Top performers are already productive; AI adds little.
individual_gain_pct = 800 * (1 - t ** 1.5)

# --- Adoption rate: sigmoid at ~93rd percentile ---
# Near 0% until 85th, ramps to ~100% at 100th.
adoption_rate = 100 / (1 + np.exp(-50 * (t - 0.93)))

# --- Line 2: Current reality ---
realized_gain = baseline * (individual_gain_pct / 100) * (adoption_rate / 100)
current_with_ai = baseline + realized_gain

# --- Line 3: If everyone adopted ---
full_gain = baseline * (individual_gain_pct / 100)
everyone_adopted = baseline + full_gain

# --- Stats ---
area_baseline = np.trapezoid(baseline, percentile)
area_current = np.trapezoid(current_with_ai, percentile)
area_everyone = np.trapezoid(everyone_adopted, percentile)
pct_realized = (area_current - area_baseline) / (area_everyone - area_baseline) * 100

# --- Plot ---

# Baseline fill and line
ax.fill_between(percentile, 0, baseline, alpha=0.12, color='#888888', zorder=1)
ax.plot(percentile, baseline, color='#555555', linewidth=2.2,
        label='Current productivity (no AI)', zorder=5)

# Realized gain (thin blue sliver)
ax.fill_between(percentile, baseline, current_with_ai, alpha=0.40,
                color='#2563eb', zorder=2)
ax.plot(percentile, current_with_ai, color='#2563eb', linewidth=2.2,
        label='With current AI adoption', zorder=5)

# Unrealized potential (large red area)
ax.fill_between(percentile, current_with_ai, everyone_adopted, alpha=0.18,
                color='#dc2626', zorder=2)
ax.plot(percentile, everyone_adopted, color='#dc2626', linewidth=2.2,
        linestyle='--', label='If everyone adopted AI', zorder=5)

# --- Annotations ---

# "Unrealized potential" in the large red area
idx_30 = int(0.30 * len(percentile))
unrealized_mid = (current_with_ai[idx_30] + everyone_adopted[idx_30]) / 2
ax.annotate('Unrealized\npotential',
            xy=(percentile[idx_30], unrealized_mid),
            fontsize=13, color='#dc2626', fontweight='bold',
            ha='center', va='center', zorder=6)

# Callout box
idx_50 = int(0.50 * len(percentile))
ax.annotate(f'Only {pct_realized:.0f}% of potential gain captured',
            xy=(50, (current_with_ai[idx_50] + everyone_adopted[idx_50]) / 2),
            xytext=(70, everyone_adopted[int(0.25 * len(percentile))] * 0.95),
            fontsize=10.5, fontweight='bold', color='#1a1a1a',
            ha='center', va='bottom',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#fff3f3',
                      edgecolor='#dc2626', linewidth=1.2, alpha=0.95),
            arrowprops=dict(arrowstyle='->', color='#dc2626', lw=1.3,
                            connectionstyle='arc3,rad=0.15'),
            zorder=7)

# Convergence note at right
ax.annotate('All lines converge:\ntop performers gain\nlittle from AI',
            xy=(93, baseline[int(0.93 * len(percentile))]),
            xytext=(72, baseline[int(0.60 * len(percentile))]),
            fontsize=8.5, color='#666666', fontstyle='italic',
            ha='center', va='top',
            arrowprops=dict(arrowstyle='->', color='#999999', lw=1,
                            connectionstyle='arc3,rad=-0.15'),
            zorder=6)

# --- Axes ---
ax.set_xlabel('Employee Percentile (by baseline performance)', fontsize=11, labelpad=10)
ax.set_ylabel('Productivity Output', fontsize=11, labelpad=10)
ax.set_xlim(0, 100)
ax.set_ylim(0, None)
ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xticklabels(['0th', '25th', '50th', '75th', '100th'])
ax.set_yticks([])

ax.legend(loc='upper left', frameon=False, fontsize=9.5)

fig.suptitle('The Integral Problem', fontsize=16, fontweight='bold',
             x=0.12, ha='left', y=0.97)
ax.set_title('Organizational output = area under the curve. The gains we\'re missing dwarf what we\'ve captured.',
             fontsize=10, color='#666666', loc='left', pad=12)

plt.tight_layout(rect=[0, 0.05, 1, 0.93])

fig.text(0.5, 0.01,
         'Sources: O\'Boyle & Aguinis (2012), Brynjolfsson et al. (2023), BCG-Harvard (2023), Bick et al. (2024)',
         fontsize=7.5, color='#999999', ha='center', va='bottom')

plt.savefig('/Users/varunr/projects/short_projects/ai-productivity-gap/charts/02_the_integral_problem.png',
            dpi=200, bbox_inches='tight', facecolor='white')
print(f'Saved. Realized: {pct_realized:.0f}%. Baseline={area_baseline:.0f}, Current={area_current:.0f}, Everyone={area_everyone:.0f}')
