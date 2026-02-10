#!/usr/bin/env python3
"""
Tier 2/3 City Analysis from AQI Bulletins (2015-2023)
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.filterwarnings('ignore')

DATA_DIR = 'data'
CHARTS_DIR = 'charts'
CIGS_PER_UG = 1/22

plt.style.use('seaborn-v0_8-whitegrid')

# =============================================================================
# 1. Load and prepare data
# =============================================================================
print("Loading AQI Bulletins (2015-2023)...")
df = pd.read_csv(f'{DATA_DIR}/AQI_bulletins/data/Processed/AllIndiaBulletins_Master.csv', low_memory=False)
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['Year'] = df['date'].dt.year
df['Month'] = df['date'].dt.month
df = df.dropna(subset=['date', 'Index Value'])

print(f"Records: {len(df)}, Cities: {df['City'].nunique()}, Years: {df['Year'].min()}-{df['Year'].max()}")

# =============================================================================
# 2. City tier classification
# =============================================================================
# Based on Indian census/government classification
TIER_1 = ['Delhi', 'Mumbai', 'Kolkata', 'Chennai', 'Bengaluru', 'Hyderabad',
          'Ahmedabad', 'Pune']

TIER_2 = ['Lucknow', 'Kanpur', 'Jaipur', 'Patna', 'Nagpur', 'Indore',
          'Bhopal', 'Visakhapatnam', 'Thiruvananthapuram', 'Coimbatore',
          'Vadodara', 'Agra', 'Varanasi', 'Srinagar', 'Amritsar',
          'Allahabad', 'Ranchi', 'Jodhpur', 'Guwahati', 'Chandigarh',
          'Dehradun', 'Mysuru', 'Raipur', 'Kochi']

# Everything else = Tier 3+
all_cities = df['City'].unique()
tier_3 = [c for c in all_cities if c not in TIER_1 and c not in TIER_2]

def classify_tier(city):
    if city in TIER_1: return 'Tier 1 (Metro)'
    elif city in TIER_2: return 'Tier 2'
    else: return 'Tier 3+'

df['Tier'] = df['City'].apply(classify_tier)

print(f"\nTier breakdown:")
print(f"  Tier 1: {len(TIER_1)} cities")
print(f"  Tier 2: {len([c for c in TIER_2 if c in all_cities])} cities")
print(f"  Tier 3+: {len([c for c in tier_3])} cities")

# =============================================================================
# 3. PLOT: AQI Distribution by Tier
# =============================================================================
print("\n3. AQI Distribution by Tier...")

fig, ax = plt.subplots(figsize=(12, 6))

tier_colors = {'Tier 1 (Metro)': '#e41a1c', 'Tier 2': '#377eb8', 'Tier 3+': '#4daf4a'}

for tier in ['Tier 1 (Metro)', 'Tier 2', 'Tier 3+']:
    tier_data = df[df['Tier'] == tier]['Index Value']
    ax.hist(tier_data, bins=80, alpha=0.5, label=f'{tier} (mean: {tier_data.mean():.0f})',
            color=tier_colors[tier], density=True)

ax.axvline(x=100, color='orange', linestyle='--', linewidth=2, label='Satisfactory/Moderate boundary')
ax.axvline(x=200, color='red', linestyle='--', linewidth=2, label='Poor threshold')

ax.set_xlabel('AQI Index Value')
ax.set_ylabel('Density')
ax.set_title('AQI Distribution by City Tier (2015-2023)', fontsize=14, fontweight='bold')
ax.legend()
ax.set_xlim(0, 500)

plt.tight_layout()
plt.savefig(f'{CHARTS_DIR}/08_aqi_distribution_by_tier.png', dpi=150)
print(f"  Saved: 08_aqi_distribution_by_tier.png")
plt.close()

# =============================================================================
# 4. PLOT: Annual Average AQI by Tier
# =============================================================================
print("\n4. Annual Average AQI by Tier...")

tier_annual = df.groupby(['Tier', 'Year'])['Index Value'].mean().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))

for tier in ['Tier 1 (Metro)', 'Tier 2', 'Tier 3+']:
    tier_data = tier_annual[tier_annual['Tier'] == tier]
    ax.plot(tier_data['Year'], tier_data['Index Value'],
            marker='o', label=tier, color=tier_colors[tier], linewidth=2.5, markersize=8)

ax.axhline(y=100, color='orange', linestyle='--', linewidth=1.5, alpha=0.7, label='Satisfactory limit')
ax.set_xlabel('Year')
ax.set_ylabel('Average AQI')
ax.set_title('Annual Average AQI by City Tier (2015-2023)', fontsize=14, fontweight='bold')
ax.legend()
ax.set_xticks(range(2015, 2024))

plt.tight_layout()
plt.savefig(f'{CHARTS_DIR}/09_annual_aqi_by_tier.png', dpi=150)
print(f"  Saved: 09_annual_aqi_by_tier.png")
plt.close()

print("\n  Annual Average AQI by Tier:")
pivot = tier_annual.pivot(index='Year', columns='Tier', values='Index Value')
print(pivot.round(1).to_string())

# =============================================================================
# 5. PLOT: Top 20 Most Polluted Cities (Average AQI)
# =============================================================================
print("\n5. Top 20 Most Polluted Cities...")

# Only use cities with >500 records for reliability
city_counts = df.groupby('City').size()
reliable_cities = city_counts[city_counts > 500].index

city_avg = df[df['City'].isin(reliable_cities)].groupby(['City', 'Tier'])['Index Value'].agg(['mean', 'count']).reset_index()
city_avg.columns = ['City', 'Tier', 'Avg_AQI', 'Records']
city_avg = city_avg.sort_values('Avg_AQI', ascending=True)

top20 = city_avg.nlargest(20, 'Avg_AQI').sort_values('Avg_AQI', ascending=True)

fig, ax = plt.subplots(figsize=(12, 8))

bar_colors = [tier_colors[t] for t in top20['Tier']]
bars = ax.barh(range(len(top20)), top20['Avg_AQI'], color=bar_colors)

ax.set_yticks(range(len(top20)))
ax.set_yticklabels([f"{row['City']} ({row['Tier']})" for _, row in top20.iterrows()])

for i, (_, row) in enumerate(top20.iterrows()):
    ax.text(row['Avg_AQI'] + 2, i, f"{row['Avg_AQI']:.0f}", va='center', fontsize=9)

ax.axvline(x=100, color='orange', linestyle='--', linewidth=2, label='Satisfactory limit')
ax.axvline(x=200, color='red', linestyle='--', linewidth=2, label='Poor threshold')

ax.set_xlabel('Average AQI (2015-2023)')
ax.set_title('Top 20 Most Polluted Indian Cities by Average AQI\n(Color = City Tier)', fontsize=14, fontweight='bold')
ax.legend()

plt.tight_layout()
plt.savefig(f'{CHARTS_DIR}/10_top20_polluted_cities.png', dpi=150)
print(f"  Saved: 10_top20_polluted_cities.png")
plt.close()

print("\nTop 20 Most Polluted:")
for _, row in top20.sort_values('Avg_AQI', ascending=False).iterrows():
    print(f"  {row['City']:20s} {row['Tier']:15s} AQI: {row['Avg_AQI']:.0f}")

# =============================================================================
# 6. PLOT: Air Quality Category Breakdown by Tier
# =============================================================================
print("\n6. Air Quality Category Breakdown by Tier...")

categories = ['Good', 'Satisfactory', 'Moderate', 'Poor', 'Very Poor', 'Severe']
cat_colors = ['#2ca02c', '#98df8a', '#ffbb78', '#ff7f0e', '#d62728', '#8b0000']

tier_cat = df.groupby(['Tier', 'Air Quality']).size().unstack(fill_value=0)
# Reorder columns
tier_cat = tier_cat[[c for c in categories if c in tier_cat.columns]]
# Normalize to percentages
tier_cat_pct = tier_cat.div(tier_cat.sum(axis=1), axis=0) * 100

fig, ax = plt.subplots(figsize=(12, 6))

tier_cat_pct.plot(kind='barh', stacked=True, ax=ax,
                  color=[cat_colors[categories.index(c)] for c in tier_cat_pct.columns])

ax.set_xlabel('Percentage of Days (%)')
ax.set_title('Air Quality Category Distribution by City Tier (2015-2023)', fontsize=14, fontweight='bold')
ax.legend(title='AQI Category', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.savefig(f'{CHARTS_DIR}/11_aqi_category_by_tier.png', dpi=150)
print(f"  Saved: 11_aqi_category_by_tier.png")
plt.close()

print("\n  AQI Category % by Tier:")
print(tier_cat_pct.round(1).to_string())

# =============================================================================
# 7. PLOT: Monthly Seasonal Pattern by Tier
# =============================================================================
print("\n7. Monthly Seasonal Pattern by Tier...")

tier_monthly = df.groupby(['Tier', 'Month'])['Index Value'].mean().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))

month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

for tier in ['Tier 1 (Metro)', 'Tier 2', 'Tier 3+']:
    tier_data = tier_monthly[tier_monthly['Tier'] == tier]
    ax.plot(tier_data['Month'], tier_data['Index Value'],
            marker='o', label=tier, color=tier_colors[tier], linewidth=2.5, markersize=8)

ax.axhline(y=100, color='orange', linestyle='--', linewidth=1.5, alpha=0.7)
ax.axvspan(10.5, 12.5, alpha=0.15, color='gray', label='Winter')
ax.axvspan(0.5, 2.5, alpha=0.15, color='gray')

ax.set_xlabel('Month')
ax.set_ylabel('Average AQI')
ax.set_title('Seasonal AQI Pattern by City Tier', fontsize=14, fontweight='bold')
ax.set_xticks(range(1, 13))
ax.set_xticklabels(month_names)
ax.legend()

plt.tight_layout()
plt.savefig(f'{CHARTS_DIR}/12_seasonal_by_tier.png', dpi=150)
print(f"  Saved: 12_seasonal_by_tier.png")
plt.close()

# =============================================================================
# 8. PLOT: "Surprise" cities - Tier 3 cities worse than metros
# =============================================================================
print("\n8. Tier 3+ cities that are WORSE than metro average...")

metro_avg_aqi = df[df['Tier'] == 'Tier 1 (Metro)']['Index Value'].mean()
print(f"\n  Metro (Tier 1) average AQI: {metro_avg_aqi:.0f}")

tier3_cities = city_avg[city_avg['Tier'] == 'Tier 3+'].copy()
tier3_worse = tier3_cities[tier3_cities['Avg_AQI'] > metro_avg_aqi].sort_values('Avg_AQI', ascending=False)

print(f"\n  Tier 3+ cities WORSE than metro average ({metro_avg_aqi:.0f}):")
print(f"  {len(tier3_worse)} out of {len(tier3_cities)} Tier 3+ cities")
for _, row in tier3_worse.head(15).iterrows():
    print(f"    {row['City']:25s} AQI: {row['Avg_AQI']:.0f}  ({row['Records']} records)")

# =============================================================================
# Summary
# =============================================================================
print("\n" + "=" * 60)
print("KEY FINDINGS")
print("=" * 60)
print(f"\n1. Average AQI by Tier:")
for tier in ['Tier 1 (Metro)', 'Tier 2', 'Tier 3+']:
    avg = df[df['Tier'] == tier]['Index Value'].mean()
    print(f"   {tier}: {avg:.0f}")

print(f"\n2. Tier 3+ cities worse than metros: {len(tier3_worse)}")
print(f"3. PM2.5 is prominent pollutant in {df['Prominent Pollutant'].str.contains('PM2.5').sum()} records ({100*df['Prominent Pollutant'].str.contains('PM2.5').sum()/len(df):.1f}%)")
print(f"4. Total city-days analyzed: {len(df):,}")
