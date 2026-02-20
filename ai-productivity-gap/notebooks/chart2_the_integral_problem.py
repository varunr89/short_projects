"""
Chart 2: The Integral Problem -- percentage increase framing

Y-axis = % productivity increase from baseline.
  - Blue line: near 0% everywhere (only top ~5% adopt)
  - Red line: literature-grounded gain curve, zero gradient at endpoints
  - Red shaded area = unrealized potential
  - Blue shaded area = realized gain (tiny sliver at far right)

Uses PchipInterpolator for shape-preserving smooth interpolation
with zero gradient at both endpoints.
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import CubicSpline

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

# --- Baseline (for weighted integral calculation) ---
baseline = 12 + 88 * (t ** 2.5)

# --- Gain curve from literature ---
# Anchor points with extra points near endpoints to force zero gradient.
gain_anchors_x = np.array([0, 5, 10, 25, 50, 75, 90, 95, 100]) / 100
gain_anchors_y = np.array([35, 35, 35, 43, 30, 17, 8, 5, 5])

# CubicSpline with clamped boundaries: zero derivative at both endpoints
gain_interp = CubicSpline(gain_anchors_x, gain_anchors_y,
                          bc_type=((1, 0), (1, 0)))
gain_pct = gain_interp(t)
gain_pct = np.maximum(gain_pct, 0)

# --- Adoption rate: sigmoid at 93rd percentile ---
adoption_rate = 1 / (1 + np.exp(-50 * (t - 0.93)))

# --- Realized gain % = gain * adoption ---
realized_pct = gain_pct * adoption_rate

# --- Aggregate org productivity increases (weighted by baseline) ---
total_baseline = np.trapezoid(baseline, t)
total_potential_increase = np.trapezoid(baseline * gain_pct / 100, t) / total_baseline * 100
total_realized_increase = np.trapezoid(baseline * realized_pct / 100, t) / total_baseline * 100

# --- Plot ---

# Realized gain (tiny blue area at far right)
ax.fill_between(percentile, 0, realized_pct, alpha=0.40,
                color='#2563eb', zorder=2)
ax.plot(percentile, realized_pct, color='#2563eb', linewidth=2.2,
        label='With current AI adoption', zorder=5)

# Unrealized potential (large red area)
ax.fill_between(percentile, realized_pct, gain_pct, alpha=0.18,
                color='#dc2626', zorder=2)
ax.plot(percentile, gain_pct, color='#dc2626', linewidth=2.2,
        linestyle='--', label='If everyone adopted AI', zorder=5)

# Zero baseline reference
ax.axhline(y=0, color='#555555', linewidth=1.5, zorder=3)

# --- Literature data point markers with dogleg leader lines ---
lit_points = [
    # (percentile, gain%, label, text_x_offset, text_y, ha)
    (10, 35, 'Brynjolfsson +35%', 28, 48, 'left'),
    (25, 43, 'BCG +43%',          12, 53, 'center'),
    (75, 17, 'BCG +17%',          65, 28, 'center'),
    (95, 5,  'Top performers +5%', 80, 13, 'center'),
]

for pctl, gain, label, tx, ty, ha in lit_points:
    # Diamond marker on the red line
    ax.plot(pctl, gain, marker='D', markersize=8, color='#dc2626',
            markeredgecolor='white', markeredgewidth=1.5, zorder=8)

    # Dogleg leader line: vertical from diamond up, then horizontal to label
    ax.annotate(label, xy=(pctl, gain),
                xytext=(tx, ty),
                fontsize=9, color='#333333', fontweight='bold',
                ha=ha, va='bottom',
                arrowprops=dict(arrowstyle='-',
                                color='#999999', lw=1,
                                connectionstyle='angle,angleA=0,angleB=90,rad=4'),
                zorder=7)

# --- Annotations ---

# "Unrealized potential" in center of red area
idx_45 = int(0.45 * len(percentile))
ax.annotate('Unrealized potential',
            xy=(percentile[idx_45], gain_pct[idx_45] / 2),
            fontsize=14, color='#dc2626', fontweight='bold',
            ha='center', va='center', zorder=6)

# Aggregate numbers box
box_text = (f'Total org productivity increase:\n'
            f'  Potential:  +{total_potential_increase:.0f}%\n'
            f'  Realized:    +{total_realized_increase:.1f}%')
ax.text(97, max(gain_pct) * 0.88,
        box_text,
        fontsize=9.5, color='#1a1a1a', fontweight='bold',
        ha='right', va='top',
        bbox=dict(boxstyle='round,pad=0.6', facecolor='#f8f8f8',
                  edgecolor='#cccccc', linewidth=1, alpha=0.95),
        zorder=7)

# --- Axes ---
ax.set_xlabel('Employee Percentile (by baseline performance)', fontsize=11, labelpad=10)
ax.set_ylabel('Productivity Increase from AI (%)', fontsize=11, labelpad=10)
ax.set_xlim(0, 100)
ax.set_ylim(-2, max(gain_pct) * 1.25)
ax.set_xticks([0, 25, 50, 75, 100])
ax.set_xticklabels(['0th', '25th', '50th', '75th', '100th'])
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f'{y:.0f}%'))

ax.legend(loc='upper right', frameon=False, fontsize=9.5)

fig.suptitle('The Integral Problem', fontsize=16, fontweight='bold',
             x=0.12, ha='left', y=0.97)
ax.set_title('Individual gains are real. But current adoption captures almost none of them.',
             fontsize=10, color='#666666', loc='left', pad=12)

plt.tight_layout(rect=[0, 0.05, 1, 0.93])

fig.text(0.5, 0.01,
         'Sources: Brynjolfsson et al. (2023), BCG-Harvard / Dell\'Acqua et al. (2023), Bick et al. (2024)',
         fontsize=7.5, color='#999999', ha='center', va='bottom')

plt.savefig('/Users/varunr/projects/short_projects/ai-productivity-gap/charts/02_the_integral_problem.png',
            dpi=200, bbox_inches='tight', facecolor='white')
print(f'Saved. Potential: +{total_potential_increase:.1f}%, Realized: +{total_realized_increase:.2f}%')
print(f'Gain at t=0.98: {gain_interp(0.98):.2f}%, at t=1.0: {gain_interp(1.0):.2f}%')
print(f'Gradient at t=1.0: {gain_interp(1.0, 1):.3f}')
