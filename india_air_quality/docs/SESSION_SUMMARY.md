# India Air Quality Analysis - Session Summary

## Project Goal
Create a blog post that makes everyday Indians viscerally understand air pollution's health impact through **cigarette-equivalent comparisons**.

## Target Audience
- **Primary**: General public - everyday Indians who may not be aware of health impacts
- **Secondary**: Tech/data community (open-source notebooks)

## Agreed Blog Structure

| Section | Content | Visualization |
|---------|---------|---------------|
| **1. Hook** | "Every breath you take in Delhi = 0.17 cigarettes" | Hero image |
| **2. The Math** | Berkeley Earth formula (22 µg/m³ = 1 cig) | Infographic |
| **3. Your City** | Metro rankings + Tier comparison | Bar chart |
| **4. The 25-Year Story** | 1998→2024 trend (rise then plateau) | Line chart |
| **5. The Bad Days** | Diwali, winter, crop burning peaks | Calendar heatmap |
| **6. North vs South** | Geographic disparity | India choropleth map |
| **7. What Now** | Masks, purifiers, advocacy, open-source link | CTA box |

---

## Key Formula
**Berkeley Earth Cigarette Equivalent:**
```
cigarettes_per_day = PM2.5 (µg/m³) / 22
```
Source: https://berkeleyearth.org/air-pollution-and-cigarette-equivalence/

---

## Datasets Downloaded

| Dataset | Location | Coverage | Key Variables |
|---------|----------|----------|---------------|
| India-Air-Quality-Dataset | `data/India-Air-Quality-Dataset/` | 5 metros, 2018-2024 | Daily PM2.5, AQI |
| AQI Bulletins | `data/AQI_bulletins/` | 277 cities, 2015-2023 | Daily AQI, category |
| CPCB Air Quality | `data/cpcb_air_quality/` | Various stations | PM2.5 |
| Historical Summary | `data/india_historical_pm25_summary.csv` | 1998-2024 | Annual averages |
| Delhi Historical | `data/delhi_historical_pm25.csv` | 1999-2024 | Annual PM2.5 |

---

## Key Findings from Data Analysis

### 1. Cigarette Equivalents by Metro City (2018-2024 avg)
| City | PM2.5 (µg/m³) | Cigarettes/Day |
|------|---------------|----------------|
| Delhi | 115 | **5.2** |
| Mumbai | 59 | 2.7 |
| Hyderabad | 47 | 2.1 |
| Chennai | 43 | 1.9 |
| Bangalore | 41 | 1.9 |

### 2. The "Improvement" Narrative is False
- **2020 COVID dip was temporary** - Delhi dropped to 102 µg/m³, bounced back to 112-115
- **No sustained improvement** - Delhi still at 115 µg/m³ in 2024
- **Research confirms**: ~30% of apparent improvements due to weather, not policy
- **NCAP has "no evidence" of contribution** (Science Advances 2024)

### 3. Tier 2/3 Cities - The Hidden Crisis
| Tier | Avg AQI | Finding |
|------|---------|---------|
| Tier 1 (Metro) | 117 | "Cleanest" due to monitoring/policy attention |
| **Tier 2** | **131** | **Worst of all tiers** |
| Tier 3+ | 124 | 74 cities worse than metro average |

**Top 5 Most Polluted (not metros!):**
1. Ghaziabad (Tier 3+) - AQI 222
2. Delhi (Tier 1) - AQI 217
3. Siwan (Tier 3+) - AQI 216
4. Bhiwadi (Tier 3+) - AQI 216
5. Chhapra (Tier 3+) - AQI 215

### 4. Seasonal Pattern
- **Worst months**: Nov-Dec (AQI 170-195 across all tiers)
- **Best months**: Jul-Sep monsoon (AQI 70-85)
- **Winter cigarette equivalent**: Delhi = 8+ cigs/day

### 5. Threshold Exceedances (Delhi)
- **100%** of days exceed WHO guideline (15 µg/m³)
- **93%** of days exceed India's own standard (40 µg/m³)
- **29%** of days are "severe" (>150 µg/m³)

---

## Charts Generated

| File | Description |
|------|-------------|
| `charts/01_metro_pm25_timeseries.png` | Daily PM2.5 time series (5 metros) |
| `charts/02_annual_avg_by_city.png` | Annual averages by metro |
| `charts/03_cigarette_equivalent_by_city.png` | Cigarette equivalent bar chart |
| `charts/04_seasonal_pattern.png` | Monthly pattern by metro |
| `charts/05_delhi_year_comparison.png` | Delhi year-over-year |
| `charts/06_pm25_distribution.png` | PM2.5 distribution histograms |
| `charts/07_covid_impact_delhi.png` | COVID lockdown impact |
| `charts/08_aqi_distribution_by_tier.png` | AQI distribution by tier |
| `charts/09_annual_aqi_by_tier.png` | Annual trend by tier |
| `charts/10_top20_polluted_cities.png` | Top 20 most polluted |
| `charts/11_aqi_category_by_tier.png` | AQI categories by tier |
| `charts/12_seasonal_by_tier.png` | Seasonal pattern by tier |

---

## Scripts Created

| File | Purpose |
|------|---------|
| `notebooks/01_data_exploration.ipynb` | Initial data exploration |
| `notebooks/02_data_visualization.py` | Metro city visualizations |
| `notebooks/03_tier_analysis.py` | Tier 2/3 analysis |

---

## Remaining Tasks

1. **Finalize blog design document** - Write to `docs/plans/`
2. **Create India choropleth map** - North vs South visualization
3. **Calculate worst-day cigarette equivalents** - Diwali/winter peaks
4. **Write the actual blog post** - With all visualizations
5. **Package notebooks for open-source release**

---

## Key Sources

- [Berkeley Earth - Cigarette Equivalence](https://berkeleyearth.org/air-pollution-and-cigarette-equivalence/)
- [UrbanEmissions - India PM2.5 1998-2022](https://urbanemissions.info/india-air-quality/india-satpm25/)
- [Science Advances 2024 - NCAP Assessment](https://www.science.org/doi/10.1126/sciadv.adq1071)
- [Nature Sustainability 2024 - Weather vs Policy](https://www.nature.com/articles/s41893-024-01366-y)
- [MDPI Review - Delhi AQ 1990-2022](https://www.mdpi.com/2071-1050/15/5/4209)

---

## Git Branch
`claude/document-skills-XrK54`

## To Continue
```bash
cd /home/user/short_projects/india_air_quality
git pull origin claude/document-skills-XrK54

# Run visualizations
python notebooks/02_data_visualization.py
python notebooks/03_tier_analysis.py

# View charts
ls charts/
```
