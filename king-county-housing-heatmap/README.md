# king-county-housing-heatmap

Interactive React web app visualizing residential housing sale prices across King County, WA on a Leaflet map. Each sale is plotted at its parcel centroid and colored by price on a continuous scale.

## Data Sources

- **RPSALE.csv** -- King County Assessor historical sales records ([download](https://info.kingcounty.gov/assessor/datadownload/default.aspx))
- **Parcel Centroids** -- King County ArcGIS REST API for geographic coordinates

## Methodology

1. Fetch and filter sales data: last 12 months, residential only, valid prices (`data/fetch_sales.py`)
2. Fetch parcel centroids via ArcGIS API (`data/fetch_parcels.py`)
3. Join sales to coordinates and output `sales_data.json` (`data/process_data.py`)
4. Render on an interactive Leaflet map with price-based color scale (`frontend/`)

## Key Findings

_To be written._

## Running

```bash
# Data pipeline
cd data && pip install -r ../requirements.txt && python fetch_sales.py && python fetch_parcels.py && python process_data.py

# Frontend
cd frontend && npm install && npm run dev
```
