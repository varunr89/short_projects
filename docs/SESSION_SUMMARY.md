# King County Housing Cost Heatmap - Session Summary

## What We Built

A React web app that visualizes residential housing sale prices in King County, WA on an interactive Leaflet map. Each sale is plotted at its parcel location and colored by price percentile (green = cheap, red = expensive).

## Project Structure

```
king-county-housing-heatmap/
├── data/
│   ├── fetch_sales.py       # Downloads RPSALE from KC Assessor
│   ├── fetch_parcels.py     # Gets parcel coords from ArcGIS API
│   ├── process_data.py      # Joins data → sales_data.json
│   ├── generate_sample.py   # Creates sample data for dev
│   └── requirements.txt     # pandas, requests, shapely
│
└── frontend/
    ├── public/
    │   └── sales_data.json  # Sample data (500 points)
    └── src/
        ├── App.jsx
        ├── components/
        │   ├── Map.jsx
        │   ├── SalesLayer.jsx
        │   └── Legend.jsx
        └── utils/
            └── colorScale.js
```

## Design Decisions Made

1. **Data Source**: King County Assessor's RPSALE.csv + ArcGIS parcel centroids
2. **Time Window**: Last 12 months of sales
3. **Price Filter**: $50K - $10M (excludes outliers and non-arm's-length)
4. **Mapping Library**: Leaflet + React-Leaflet (free, no API key)
5. **Color Scale**: Percentile-based (not absolute) - green→yellow→orange→red
6. **Architecture**: Static JSON, no backend needed

## What's Complete

- ✅ Project scaffolding and dependencies
- ✅ `fetch_sales.py` - downloads and filters sales data
- ✅ `fetch_parcels.py` - batch queries ArcGIS for parcel coordinates
- ✅ `process_data.py` - joins data and outputs JSON
- ✅ `generate_sample.py` - creates dev sample data
- ✅ React frontend with Map, Legend, tooltips
- ✅ Production build works (351 KB JS bundle)
- ✅ All code committed and pushed

## What Needs to Run Outside Sandbox

The sandbox blocks external HTTP requests. Run these from your CLI:

```bash
cd king-county-housing-heatmap/data

# 1. Download and filter sales data (~30 seconds)
python3 fetch_sales.py
# Outputs: raw/filtered_sales.csv (~15-25K sales)

# 2. Fetch parcel coordinates (~15-30 minutes)
python3 fetch_parcels.py
# Outputs: raw/parcel_coords.csv
# Queries ArcGIS in batches of 100, rate-limited

# 3. Join data and create final JSON
python3 process_data.py
# Outputs: ../frontend/public/sales_data.json

# 4. Test the frontend
cd ../frontend
npm run dev
# Opens at http://localhost:5173
```

## Future Iteration: Adaptive Choropleth

We discussed but didn't implement an adaptive region sizing approach:
- Dense areas (Seattle core) → smaller grid cells
- Sparse areas (rural) → larger aggregated regions
- Minimum 10 sales per region for statistical validity
- Options to explore: H3 hexagons, quadtree, Voronoi

Start with the colored circles, then experiment with aggregation once you see the data density.

## Key Files to Know

| File | What It Does |
|------|--------------|
| `data/fetch_sales.py:107-133` | Downloads ZIP, extracts CSV |
| `data/fetch_sales.py:136-195` | Filters by date, price, formats output |
| `data/fetch_parcels.py:284-324` | Batch queries ArcGIS, computes centroids |
| `frontend/src/utils/colorScale.js` | Price → color mapping |
| `frontend/src/components/SalesLayer.jsx` | Renders circle markers |

## Git State

- Branch: `claude/housing-cost-heatmap-KvRis`
- Latest commit: `86f7f5d feat: finalize housing cost heatmap v1 with sample data`
- Status: Clean, pushed to origin

## To Continue Development

```bash
# Clone and checkout
git checkout claude/housing-cost-heatmap-KvRis

# Install Python deps
cd king-county-housing-heatmap/data
pip3 install -r requirements.txt

# Install Node deps
cd ../frontend
npm install

# Run with sample data
npm run dev

# Or fetch real data first (see above)
```

## Documents Created

- `docs/plans/2025-01-31-housing-cost-heatmap-design.md` - Full design doc
- `docs/plans/2025-01-31-housing-cost-heatmap-implementation.md` - 12-task implementation plan
