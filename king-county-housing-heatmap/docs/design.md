# King County Housing Cost Heatmap - Design

## Overview

A React web application that visualizes residential housing sale prices across King County, WA on an interactive map. Each sale is plotted at its parcel location and colored by price on a continuous scale. Future iteration will add adaptive choropleth aggregation.

## Data Sources

### RPSALE.csv - King County Assessor
- Source: https://info.kingcounty.gov/assessor/datadownload/default.aspx
- Contains all historical real property sales records
- Fields used: ExciseTaxNum, Major, Minor, SaleDate, SalePrice, PropertyType
- Updated regularly by county assessor

### Parcel Centroids - King County ArcGIS REST API
- Source: https://gisdata.kingcounty.gov/arcgis/rest/services/OpenDataPortal/property__parcel_area/MapServer
- Provides geographic centroid (lat/lng) for each parcel
- Queried by parcel ID (Major+Minor)
- Max 4000 records per API request

## Data Architecture

### Filtering Pipeline
```
RPSALE.csv (all historical sales)
        |
Filter: SaleDate >= 1 year ago
        |
Filter: Residential property types only
        |
Filter: Valid sales (exclude $0, family transfers, non-market sales)
        |
~15-25K sales (estimated for 1 year window)
```

### Processing Steps

1. **fetch_sales.py** - Download RPSALE.csv from KC Assessor (likely ZIP containing CSV). Parse and filter to: last 12 months, residential PropertyType, SalePrice > $0.

2. **fetch_parcels.py** - Query ArcGIS REST API with `returnCentroid=true` in batches of ~4000. Only fetch parcels that appear in filtered sales data.

3. **process_data.py** - Join sales to parcel centroids on Major+Minor. Drop unmatched. Calculate summary stats. Output sales_data.json.

### Output Format
```json
{
  "generated": "2025-01-31",
  "stats": { "median": 725000, "min": 150000, "max": 4500000, "count": 18432 },
  "sales": [
    { "lat": 47.61, "lng": -122.33, "price": 850000, "date": "2024-06-15" }
  ]
}
```

### Error Handling
- Log parcels that fail to geocode
- Report % of sales successfully matched (target >95%)

## Frontend Architecture

### Tech Stack
- React (Vite)
- Leaflet + React-Leaflet
- No backend - static JSON served alongside the app

### Component Structure
```
App
+-- MapContainer (Leaflet map, full viewport)
|   +-- TileLayer (CartoDB Positron basemap)
|   +-- SalesLayer (renders circles or choropleth)
+-- ColorLegend (price scale reference)
+-- FilterPanel (date range, price range sliders)
+-- InfoPanel (stats, hover/click details)
```

### Visualization

**Phase 1 - Colored Circles:**
- Each sale rendered as a circle marker at parcel centroid
- Color scale based on price percentiles (not absolute values)
- Scheme: dark green (0-20th) -> light green (20-40th) -> yellow (40-60th) -> orange (60-80th) -> red (80-100th)
- Legend displays actual dollar values at each breakpoint
- `preferCanvas: true` for performance with 15-25K markers

**Phase 2 - Adaptive Choropleth (future iteration):**
- Experiment with aggregation once data density is understood
- Options: H3 hexagonal grid, fixed grid, Voronoi tessellation
- Rule: minimum 10 sales per region for statistical validity
- Regions with <10 sales expand or merge with neighbors
- Color each region by median sale price

### Map Defaults
- Center: ~47.5, -122.2 (King County center)
- Zoom: 10 (shows full county)
- Basemap: CartoDB Positron (light, minimal)

### Interactions
- Hover: tooltip with sale price and date
- Click: info panel with full details
- Zoom: reduce opacity or cluster at low zoom if overlapping
- Filter panel: sliders for price range and date range

### Performance
- 15-25K circle markers render fine with canvas renderer
- If sluggish, add clustering at low zoom levels

## Project Structure
```
king-county-housing-heatmap/
+-- data/
|   +-- fetch_sales.py
|   +-- fetch_parcels.py
|   +-- process_data.py
|   +-- requirements.txt
|   +-- raw/                   (gitignored)
|
+-- frontend/
|   +-- public/
|   |   +-- sales_data.json   (processed data)
|   +-- src/
|   |   +-- App.jsx
|   |   +-- components/
|   |   |   +-- Map.jsx
|   |   |   +-- SalesLayer.jsx
|   |   |   +-- Legend.jsx
|   |   |   +-- InfoPanel.jsx
|   |   +-- utils/
|   |   |   +-- colorScale.js
|   |   +-- main.jsx
|   +-- package.json
|   +-- vite.config.js
|
+-- README.md
```

## Deployment
- Static hosting (Vercel, Netlify, or GitHub Pages)
- Just the built frontend + sales_data.json
- No server needed

## Workflow
1. Run Python scripts in data/ to generate sales_data.json
2. Copy JSON to frontend/public/
3. npm run dev to develop, npm run build to deploy
