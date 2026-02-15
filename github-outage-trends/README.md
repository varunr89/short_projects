# github-outage-trends

Analyzing trends in GitHub outages from 2013 to 2026 using data scraped from the GitHub Status page. Tests the hypothesis that rising outage frequency correlates with platform growth and AI feature expansion, not the Azure migration.

## Data Source

- [GitHub Status History](https://www.githubstatus.com/history) -- all publicly reported incidents, scraped via Playwright

## Methodology

1. Scrape all incident history pages using a headless browser to capture JS-rendered data (`data/scrape_incidents.py`)
2. Parse and clean dates, durations, impact levels, and categorize affected components (`data/clean_incidents.py`)
3. Analyze trends in frequency, severity, component breakdown, and duration (`notebooks/01_trend_analysis.py`)

## Key Findings

- **1,234 incidents** scraped from Sept 2013 to Feb 2026
- Incidents were stable at 40-90/year from 2013-2021, then jumped to 136 (2022), 165 (2023), and 207 (2025)
- The inflection point aligns with AI-era feature growth (Actions, Copilot, Codespaces), not the Azure migration timeline
- Actions alone accounts for 233 incidents (19% of all), with Copilot adding 71 (6%) since its 2022 launch
- Major/critical incidents also increased from ~5/year (2015-2020) to 26-36/year (2024-2025)
- Duration data only reliable from 2019+; median duration has stayed around 50-90 minutes

## Limitations

- Pre-2019 incidents lack resolution timestamps (start == end), so duration analysis is only valid from 2019 onward
- Component categorization is based on keyword matching from titles/bodies, which may misclassify some incidents
- The status page may not capture all incidents uniformly across all years
