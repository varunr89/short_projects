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

- 22,603 geocoded home sales in the last 12 months, with a median price of $950,000
- The Lake Washington waterfront corridor (Medina, Mercer Island, Bellevue) forms a visible band of $2M+ sales
- South King County (Federal Way, Auburn, Kent) is where sub-$600K sales concentrate
- The 20th-to-80th percentile spread is over $1M ($634K to $1.675M)

## Running

```bash
# Data pipeline
cd king-county-housing-heatmap
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python data/fetch_sales.py
python data/fetch_parcels.py   # ~5 min (API rate limited)
python data/process_data.py

# Frontend
cd frontend && npm install && npm run dev
```
