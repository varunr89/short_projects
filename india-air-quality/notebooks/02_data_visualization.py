#!/usr/bin/env python3
"""
India Air Quality Data Visualization
Generates plots to explore PM2.5 trends and cigarette equivalents
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Setup
DATA_DIR = Path('/home/user/short_projects/india_air_quality/data')
CHARTS_DIR = Path('/home/user/short_projects/india_air_quality/charts')
CHARTS_DIR.mkdir(exist_ok=True)

# Cigarette equivalent: 22 µg/m³ PM2.5 = 1 cigarette/day
CIGS_PER_UG = 1/22

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 11

print("=" * 60)
print("INDIA AIR QUALITY DATA EXPLORATION")
print("=" * 60)

# =============================================================================
# 1. Load Metro Cities Data (India-Air-Quality-Dataset)
# =============================================================================
print("\n1. LOADING METRO CITIES DATA...")

cities = ['Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Hyderabad']
metro_dfs = {}

for city in cities:
    path = DATA_DIR / 'India-Air-Quality-Dataset' / f'{city}_AQI_Dataset.csv'
    if path.exists():
        df = pd.read_csv(path)
        df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y', errors='coerce')
        df['City'] = city
        metro_dfs[city] = df
        print(f"  {city}: {len(df)} rows, {df['Date'].min().date()} to {df['Date'].max().date()}")

# Combine all metros
metro_all = pd.concat(metro_dfs.values(), ignore_index=True)
metro_all = metro_all.dropna(subset=['Date', 'PM2.5'])
metro_all['Year'] = metro_all['Date'].dt.year
metro_all['Month'] = metro_all['Date'].dt.month
metro_all['Cigarettes'] = metro_all['PM2.5'] * CIGS_PER_UG

print(f"\nTotal metro records: {len(metro_all)}")
print(f"PM2.5 range: {metro_all['PM2.5'].min():.1f} - {metro_all['PM2.5'].max():.1f} µg/m³")

# =============================================================================
# 2. PLOT: Daily PM2.5 Time Series for All Metros
# =============================================================================
print("\n2. GENERATING: Daily PM2.5 Time Series...")

fig, ax = plt.subplots(figsize=(14, 6))

colors = {'Delhi': '#e41a1c', 'Mumbai': '#377eb8', 'Bangalore': '#4daf4a',
          'Chennai': '#984ea3', 'Hyderabad': '#ff7f00'}

for city in cities:
    city_data = metro_all[metro_all['City'] == city].sort_values('Date')
    # Rolling 30-day average for clarity
    city_data['PM25_rolling'] = city_data['PM2.5'].rolling(30, min_periods=1).mean()
    ax.plot(city_data['Date'], city_data['PM25_rolling'],
            label=city, color=colors[city], alpha=0.8, linewidth=1.5)

# Add WHO guideline
ax.axhline(y=15, color='green', linestyle='--', linewidth=2, label='WHO Annual Guideline (15 µg/m³)')
ax.axhline(y=40, color='orange', linestyle='--', linewidth=2, label='India NAAQS (40 µg/m³)')

ax.set_xlabel('Date')
ax.set_ylabel('PM2.5 (µg/m³) - 30-day rolling average')
ax.set_title('Daily PM2.5 Levels in Major Indian Metros (2018-2024)', fontsize=14, fontweight='bold')
ax.legend(loc='upper right')
ax.set_ylim(0, 350)

plt.tight_layout()
plt.savefig(CHARTS_DIR / '01_metro_pm25_timeseries.png', dpi=150)
print(f"  Saved: {CHARTS_DIR / '01_metro_pm25_timeseries.png'}")
plt.close()

# =============================================================================
# 3. PLOT: Annual Average PM2.5 by City
# =============================================================================
print("\n3. GENERATING: Annual Average PM2.5 by City...")

annual_avg = metro_all.groupby(['City', 'Year'])['PM2.5'].mean().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))

for city in cities:
    city_data = annual_avg[annual_avg['City'] == city]
    ax.plot(city_data['Year'], city_data['PM2.5'],
            marker='o', label=city, color=colors[city], linewidth=2, markersize=8)

ax.axhline(y=15, color='green', linestyle='--', linewidth=2, label='WHO Guideline')
ax.axhline(y=40, color='orange', linestyle='--', linewidth=2, label='India NAAQS')

ax.set_xlabel('Year')
ax.set_ylabel('Annual Average PM2.5 (µg/m³)')
ax.set_title('Annual Average PM2.5 by Metro City', fontsize=14, fontweight='bold')
ax.legend(loc='upper right')
ax.set_xticks(annual_avg['Year'].unique())

plt.tight_layout()
plt.savefig(CHARTS_DIR / '02_annual_avg_by_city.png', dpi=150)
print(f"  Saved: {CHARTS_DIR / '02_annual_avg_by_city.png'}")
plt.close()

# Print the data
print("\n  Annual Average PM2.5 (µg/m³):")
pivot = annual_avg.pivot(index='Year', columns='City', values='PM2.5')
print(pivot.round(1).to_string())

# =============================================================================
# 4. PLOT: Cigarette Equivalent by City (Bar Chart)
# =============================================================================
print("\n4. GENERATING: Cigarette Equivalent by City...")

# Calculate overall average for each city
city_avg = metro_all.groupby('City').agg({
    'PM2.5': 'mean',
    'Cigarettes': 'mean'
}).round(2)
city_avg = city_avg.sort_values('Cigarettes', ascending=True)

fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.barh(city_avg.index, city_avg['Cigarettes'], color=[colors[c] for c in city_avg.index])

# Add value labels
for i, (idx, row) in enumerate(city_avg.iterrows()):
    ax.text(row['Cigarettes'] + 0.1, i, f"{row['Cigarettes']:.1f} cigs/day\n({row['PM2.5']:.0f} µg/m³)",
            va='center', fontsize=10)

ax.set_xlabel('Cigarettes per Day Equivalent')
ax.set_title('Air Pollution as Cigarette Equivalent\n(Based on Berkeley Earth: 22 µg/m³ = 1 cigarette/day)',
             fontsize=14, fontweight='bold')
ax.set_xlim(0, max(city_avg['Cigarettes']) + 2)

plt.tight_layout()
plt.savefig(CHARTS_DIR / '03_cigarette_equivalent_by_city.png', dpi=150)
print(f"  Saved: {CHARTS_DIR / '03_cigarette_equivalent_by_city.png'}")
plt.close()

print("\n  Cigarette Equivalent Summary:")
print(city_avg.to_string())

# =============================================================================
# 5. PLOT: Monthly Seasonal Pattern
# =============================================================================
print("\n5. GENERATING: Monthly Seasonal Pattern...")

monthly_avg = metro_all.groupby(['City', 'Month'])['PM2.5'].mean().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))

month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

for city in cities:
    city_data = monthly_avg[monthly_avg['City'] == city]
    ax.plot(city_data['Month'], city_data['PM2.5'],
            marker='o', label=city, color=colors[city], linewidth=2, markersize=8)

ax.axhline(y=15, color='green', linestyle='--', linewidth=2, alpha=0.7)
ax.axhline(y=40, color='orange', linestyle='--', linewidth=2, alpha=0.7)

# Highlight winter months
ax.axvspan(10.5, 12.5, alpha=0.2, color='gray', label='Winter (Oct-Dec)')
ax.axvspan(0.5, 2.5, alpha=0.2, color='gray')

ax.set_xlabel('Month')
ax.set_ylabel('Average PM2.5 (µg/m³)')
ax.set_title('Seasonal Pattern: Monthly Average PM2.5', fontsize=14, fontweight='bold')
ax.set_xticks(range(1, 13))
ax.set_xticklabels(month_names)
ax.legend(loc='upper right')

plt.tight_layout()
plt.savefig(CHARTS_DIR / '04_seasonal_pattern.png', dpi=150)
print(f"  Saved: {CHARTS_DIR / '04_seasonal_pattern.png'}")
plt.close()

# =============================================================================
# 6. PLOT: Delhi Deep Dive - Year over Year Comparison
# =============================================================================
print("\n6. GENERATING: Delhi Year-over-Year Comparison...")

delhi = metro_all[metro_all['City'] == 'Delhi'].copy()
delhi['DayOfYear'] = delhi['Date'].dt.dayofyear

fig, ax = plt.subplots(figsize=(14, 6))

years = sorted(delhi['Year'].unique())
cmap = plt.cm.viridis(np.linspace(0, 1, len(years)))

for i, year in enumerate(years):
    year_data = delhi[delhi['Year'] == year].sort_values('DayOfYear')
    year_data['PM25_rolling'] = year_data['PM2.5'].rolling(7, min_periods=1).mean()
    ax.plot(year_data['DayOfYear'], year_data['PM25_rolling'],
            label=str(year), color=cmap[i], linewidth=1.5, alpha=0.8)

ax.axhline(y=15, color='green', linestyle='--', linewidth=2)
ax.axhline(y=40, color='orange', linestyle='--', linewidth=2)

# Mark Diwali period (roughly Oct-Nov, days 275-320)
ax.axvspan(275, 320, alpha=0.15, color='red', label='Diwali/Post-monsoon')

ax.set_xlabel('Day of Year')
ax.set_ylabel('PM2.5 (µg/m³) - 7-day rolling average')
ax.set_title('Delhi: Year-over-Year PM2.5 Comparison', fontsize=14, fontweight='bold')
ax.legend(loc='upper left', ncol=2)
ax.set_xlim(1, 365)

plt.tight_layout()
plt.savefig(CHARTS_DIR / '05_delhi_year_comparison.png', dpi=150)
print(f"  Saved: {CHARTS_DIR / '05_delhi_year_comparison.png'}")
plt.close()

# =============================================================================
# 7. PLOT: Distribution of Daily PM2.5 (Histogram)
# =============================================================================
print("\n7. GENERATING: PM2.5 Distribution by City...")

fig, axes = plt.subplots(2, 3, figsize=(14, 8))
axes = axes.flatten()

for i, city in enumerate(cities):
    city_data = metro_all[metro_all['City'] == city]['PM2.5']
    axes[i].hist(city_data, bins=50, color=colors[city], alpha=0.7, edgecolor='white')
    axes[i].axvline(x=15, color='green', linestyle='--', linewidth=2, label='WHO')
    axes[i].axvline(x=40, color='orange', linestyle='--', linewidth=2, label='India')
    axes[i].axvline(x=city_data.mean(), color='red', linestyle='-', linewidth=2, label=f'Mean: {city_data.mean():.0f}')
    axes[i].set_title(f'{city}', fontsize=12, fontweight='bold')
    axes[i].set_xlabel('PM2.5 (µg/m³)')
    axes[i].legend(fontsize=8)

# Remove empty subplot
axes[5].axis('off')

plt.suptitle('Distribution of Daily PM2.5 Values by City', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(CHARTS_DIR / '06_pm25_distribution.png', dpi=150)
print(f"  Saved: {CHARTS_DIR / '06_pm25_distribution.png'}")
plt.close()

# =============================================================================
# 8. PLOT: COVID Impact - 2019 vs 2020 vs 2021
# =============================================================================
print("\n8. GENERATING: COVID Impact Analysis...")

covid_years = [2019, 2020, 2021, 2022]
delhi_covid = delhi[delhi['Year'].isin(covid_years)].copy()

# Monthly averages
covid_monthly = delhi_covid.groupby(['Year', 'Month'])['PM2.5'].mean().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))

colors_covid = {2019: '#1f77b4', 2020: '#2ca02c', 2021: '#d62728', 2022: '#9467bd'}
markers = {2019: 'o', 2020: 's', 2021: '^', 2022: 'D'}

for year in covid_years:
    year_data = covid_monthly[covid_monthly['Year'] == year]
    ax.plot(year_data['Month'], year_data['PM2.5'],
            marker=markers[year], label=str(year), color=colors_covid[year],
            linewidth=2, markersize=8)

# Mark lockdown period (March-May 2020)
ax.axvspan(3, 5, alpha=0.2, color='green', label='Lockdown Period')

ax.set_xlabel('Month')
ax.set_ylabel('Average PM2.5 (µg/m³)')
ax.set_title('Delhi: COVID Impact on Air Quality (2019-2022)', fontsize=14, fontweight='bold')
ax.set_xticks(range(1, 13))
ax.set_xticklabels(month_names)
ax.legend(loc='upper right')

plt.tight_layout()
plt.savefig(CHARTS_DIR / '07_covid_impact_delhi.png', dpi=150)
print(f"  Saved: {CHARTS_DIR / '07_covid_impact_delhi.png'}")
plt.close()

# Print COVID comparison
print("\n  Delhi Monthly PM2.5 (2019-2022):")
covid_pivot = covid_monthly.pivot(index='Month', columns='Year', values='PM2.5')
covid_pivot.index = month_names
print(covid_pivot.round(1).to_string())

# =============================================================================
# 9. Summary Statistics
# =============================================================================
print("\n" + "=" * 60)
print("SUMMARY STATISTICS")
print("=" * 60)

print("\n  Overall City Statistics:")
summary = metro_all.groupby('City').agg({
    'PM2.5': ['mean', 'median', 'std', 'min', 'max'],
    'Cigarettes': 'mean'
}).round(1)
summary.columns = ['Mean', 'Median', 'StdDev', 'Min', 'Max', 'Cigs/Day']
print(summary.to_string())

print("\n  Days exceeding thresholds:")
for city in cities:
    city_data = metro_all[metro_all['City'] == city]
    total = len(city_data)
    exceed_who = (city_data['PM2.5'] > 15).sum()
    exceed_india = (city_data['PM2.5'] > 40).sum()
    exceed_severe = (city_data['PM2.5'] > 150).sum()
    print(f"  {city}:")
    print(f"    > WHO (15 µg/m³):    {exceed_who:4d} days ({100*exceed_who/total:.1f}%)")
    print(f"    > India (40 µg/m³):  {exceed_india:4d} days ({100*exceed_india/total:.1f}%)")
    print(f"    > Severe (150 µg/m³): {exceed_severe:4d} days ({100*exceed_severe/total:.1f}%)")

print("\n" + "=" * 60)
print(f"Charts saved to: {CHARTS_DIR}")
print("=" * 60)
