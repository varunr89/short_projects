# Mapping Every Home Sale in King County

In the last twelve months, over 22,000 homes changed hands in King County, Washington. The median sale price was $950,000. I mapped every one of those sales to its exact parcel location and colored it by price, creating an interactive heatmap that reveals the geography of housing costs across the Seattle metro area.

## The data

King County publishes every real property sales record through its Assessor's office. The dataset goes back decades, but I filtered to the last twelve months (February 2025 through February 2026) and to sales priced between $50,000 and $10,000,000 to exclude non-market transfers and statistical outliers. That left 29,170 transactions.

To place each sale on a map, I needed geographic coordinates. The county's ArcGIS REST API provides polygon boundaries for every parcel. I queried it for each unique parcel in the sales data, computed the centroid of each polygon, and joined the results back to the sales records. About 78% of parcels matched successfully. The remainder were mostly condos and subdivided lots whose parcel IDs had changed in the county's GIS system. The final dataset contains 22,603 geocoded sales.

## What the map shows

The interactive map renders each sale as a small circle at its parcel location. Color encodes price using a five-band percentile scale: dark green for the bottom 20% of sales (under $634K), through light green, yellow, and orange, up to red for the top 20% (above $1.675M).

![King County housing sales heatmap](../charts/01_king_county_heatmap.png)

The spatial patterns are striking. The most expensive sales (red and orange) cluster along the Lake Washington waterfront, through Medina, Mercer Island, and the Bellevue-to-Kirkland corridor. Downtown Seattle and Capitol Hill show a mix of moderate and high prices. South King County, from Renton through Kent to Federal Way, is overwhelmingly green, with most sales below the county median.

East of the Cascades foothills, the map thins out rapidly. Enumclaw, Black Diamond, and the rural southeast corner of the county show scattered low-to-moderate sales with large gaps between them.

## The price distribution

The numbers tell the same story. The 20th percentile sits at $634,000, meaning one in five homes sold for less than that. The median is $950,000. The 80th percentile is $1,675,000. The mean ($1.28M) is pulled well above the median by a long right tail of multi-million dollar sales.

| Percentile | Price |
|-----------|-------|
| Minimum | $50,000 |
| 20th | $634,000 |
| 40th | $830,000 |
| 60th (median approx.) | $1,145,000 |
| 80th | $1,675,000 |
| Maximum | $10,000,000 |

The gap between the 20th and 80th percentile is just over $1 million. That spread, visible on the map as the transition from green to red, plays out over surprisingly short distances. In some neighborhoods, a ten-minute drive separates $500K starter homes from $2M properties.

## How it works

The project has two parts: a Python data pipeline and a React frontend.

The pipeline runs three scripts. First, `fetch_sales.py` downloads the county's sales ZIP file, extracts the CSV, and filters it by date and price. Second, `fetch_parcels.py` queries the ArcGIS API in batches of 100 PINs, computes polygon centroids using Shapely, and writes coordinates to a CSV. Third, `process_data.py` joins the two datasets, applies geographic bounds, calculates percentile breakpoints, and outputs a single `sales_data.json` file.

The frontend is a Vite-powered React app using Leaflet and React-Leaflet. It loads the JSON at startup, creates a color scale from the percentile breakpoints, and renders 22,000+ circle markers on a CartoDB Positron basemap. Hovering over any circle shows the sale price and date. The map uses Leaflet's canvas renderer (`preferCanvas: true`) for performance, drawing all markers to a single HTML5 Canvas element instead of creating individual DOM nodes.

The entire app is static. There is no backend server. The data pipeline produces a JSON file, and the built frontend serves it alongside the JavaScript bundle.

## What surprised me

Three things stood out.

First, the waterfront premium is visible from space. The band of red markers hugging Lake Washington's eastern shore is the single most obvious pattern on the map. Medina, Clyde Hill, and Yarrow Point form an almost unbroken line of $2M+ sales.

Second, South King County is a different market entirely. The area south of I-90 is dominated by green markers. Federal Way, Auburn, and Kent are where the sub-$600K sales concentrate. The dividing line is remarkably sharp.

Third, the data has gaps. The 22% of parcels that failed to geocode are disproportionately condos. King County's parcel system sometimes assigns condo units a PIN that does not correspond to a standalone polygon in the GIS database. A future version could address this by geocoding condos to their parent building parcel.

### Methodology

Sales data comes from King County Assessor's RPSALE.csv, filtered to the period February 2025 through February 2026, with prices between $50,000 and $10,000,000. Parcel coordinates were obtained from King County's ArcGIS REST API (OpenDataPortal/property__parcel_area, FeatureServer layer 439). Centroids were computed using Shapely. The color scale uses quintile breakpoints (20th, 40th, 60th, 80th percentiles) with linear RGB interpolation between five color stops. All property types are included (residential, commercial, land), though the $50K-$10M price filter excludes most non-residential transactions.

### Sources

- **Sales data:** King County Assessor - Real Property Sales (RPSALE.csv)
- **Parcel geometries:** King County GIS - ArcGIS REST API
- **Basemap tiles:** CartoDB Positron
- **Analysis code:** [github.com/varunr89/short_projects](https://github.com/varunr89/short_projects)
