# King County Housing Cost Heatmap - Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a React web app that visualizes King County residential housing sale prices on an interactive Leaflet map, colored by price percentile.

**Architecture:** Python data pipeline downloads RPSALE sales data and parcel centroids from King County, joins them, and outputs a static JSON file. React/Vite frontend loads the JSON and renders colored circle markers on a Leaflet map with filtering and tooltips.

**Tech Stack:** Python 3 (pandas, requests, shapely), React 18, Vite, Leaflet, React-Leaflet

---

## Task 1: Project Scaffolding

**Files:**
- Create: `king-county-housing-heatmap/data/requirements.txt`
- Create: `king-county-housing-heatmap/data/.gitkeep`
- Create: `king-county-housing-heatmap/.gitignore`

**Step 1: Create project directories**

```bash
mkdir -p king-county-housing-heatmap/data/raw
mkdir -p king-county-housing-heatmap/frontend
```

**Step 2: Create .gitignore**

```
# Data
king-county-housing-heatmap/data/raw/
__pycache__/
*.pyc

# Node
node_modules/
dist/

# Environment
.env
*.log
```

**Step 3: Create Python requirements.txt**

```
pandas>=2.0
requests>=2.31
shapely>=2.0
```

**Step 4: Install Python dependencies**

```bash
cd king-county-housing-heatmap/data
pip3 install -r requirements.txt
```

**Step 5: Commit**

```bash
git add .
git commit -m "feat: scaffold project structure with data and frontend dirs"
```

---

## Task 2: Fetch Sales Data Script

**Files:**
- Create: `king-county-housing-heatmap/data/fetch_sales.py`

**Context:** The King County Assessor provides a ZIP file containing EXTR_RPSale.csv at:
`https://aqua.kingcounty.gov/extranet/assessor/Real%20Property%20Sales.zip`

The CSV has these columns (not all are needed):
- `ExciseTaxNbr` - unique sale identifier
- `Major` - first 6 chars of parcel ID (string, may have leading zeros)
- `Minor` - last 4 chars of parcel ID (string, may have leading zeros)
- `DocumentDate` - sale date (MM/DD/YYYY format)
- `SalePrice` - integer sale price
- `PropertyType` - numeric code (need to discover residential codes)
- `PrincipalUse` - principal use code
- `SaleInstrument` - type of sale instrument
- `SaleReason` - reason code (0 = none specified)
- `PropertyClass` - property class code

**Step 1: Write fetch_sales.py**

```python
#!/usr/bin/env python3
"""Download and filter King County real property sales data."""

import io
import os
import zipfile
from datetime import datetime, timedelta

import pandas as pd
import requests

SALES_URL = "https://aqua.kingcounty.gov/extranet/assessor/Real%20Property%20Sales.zip"
RAW_DIR = os.path.join(os.path.dirname(__file__), "raw")
OUTPUT_CSV = os.path.join(RAW_DIR, "filtered_sales.csv")


def download_sales_zip():
    """Download and extract RPSALE CSV from King County Assessor."""
    os.makedirs(RAW_DIR, exist_ok=True)
    zip_path = os.path.join(RAW_DIR, "Real_Property_Sales.zip")

    if os.path.exists(zip_path):
        print(f"Using cached ZIP: {zip_path}")
    else:
        print(f"Downloading sales data from {SALES_URL}...")
        resp = requests.get(SALES_URL, timeout=120)
        resp.raise_for_status()
        with open(zip_path, "wb") as f:
            f.write(resp.content)
        print(f"Downloaded {len(resp.content) / 1024 / 1024:.1f} MB")

    with zipfile.ZipFile(zip_path) as zf:
        csv_names = [n for n in zf.namelist() if n.endswith(".csv")]
        print(f"Files in ZIP: {csv_names}")
        # Find the RPSale CSV (name may vary)
        sale_csv = next(
            (n for n in csv_names if "rpsale" in n.lower() or "sale" in n.lower()),
            csv_names[0],
        )
        print(f"Extracting: {sale_csv}")
        with zf.open(sale_csv) as f:
            df = pd.read_csv(f, dtype={"Major": str, "Minor": str})
    return df


def filter_sales(df):
    """Filter to recent residential sales with valid prices."""
    print(f"Total records: {len(df)}")

    # Print column names for debugging
    print(f"Columns: {list(df.columns)}")

    # Print unique PropertyType values to understand the codes
    if "PropertyType" in df.columns:
        print(f"\nPropertyType value counts:\n{df['PropertyType'].value_counts().head(20)}")

    # Parse sale date - try multiple column name variants
    date_col = None
    for col in ["DocumentDate", "SaleDate", "DocumentDt"]:
        if col in df.columns:
            date_col = col
            break
    if date_col is None:
        raise ValueError(f"No date column found. Columns: {list(df.columns)}")

    df["sale_date"] = pd.to_datetime(df[date_col], format="mixed", errors="coerce")

    # Filter: last 12 months
    one_year_ago = datetime.now() - timedelta(days=365)
    df = df[df["sale_date"] >= one_year_ago]
    print(f"After date filter (>= {one_year_ago.date()}): {len(df)}")

    # Filter: sale price > 0 (exclude non-arm's-length transfers)
    price_col = "SalePrice"
    df = df[df[price_col] > 0]
    print(f"After price > $0 filter: {len(df)}")

    # Filter: reasonable residential prices ($50K - $10M)
    df = df[(df[price_col] >= 50000) & (df[price_col] <= 10000000)]
    print(f"After price range filter ($50K-$10M): {len(df)}")

    # Filter: residential property types
    # PropertyType codes for residential vary - common ones:
    # 2=Res-Improved, 3=Res-Vacant, 10=Condo, 11=Townhouse
    # We'll be flexible: include all and let user inspect.
    # For now, filter on PropertyType if available, otherwise use PrincipalUse
    if "PropertyType" in df.columns:
        # Include common residential types - adjust after inspecting data
        # For safety, start broad and log what we're including
        residential_types = df["PropertyType"].value_counts()
        print(f"\nAll PropertyType values in filtered data:\n{residential_types}")
        # Common residential: 2, 3, 10, 11 - but verify from actual data
        # We'll keep all types for now and filter in process_data.py after inspection

    # Pad Major/Minor to standard widths (6 and 4 chars)
    df["Major"] = df["Major"].str.strip().str.zfill(6)
    df["Minor"] = df["Minor"].str.strip().str.zfill(4)
    df["PIN"] = df["Major"] + df["Minor"]

    # Select output columns
    output = df[["PIN", "Major", "Minor", "sale_date", price_col]].copy()
    output.columns = ["PIN", "Major", "Minor", "date", "price"]
    output["date"] = output["date"].dt.strftime("%Y-%m-%d")

    return output


def main():
    df = download_sales_zip()
    filtered = filter_sales(df)
    filtered.to_csv(OUTPUT_CSV, index=False)
    print(f"\nSaved {len(filtered)} filtered sales to {OUTPUT_CSV}")
    print(f"Price range: ${filtered['price'].min():,.0f} - ${filtered['price'].max():,.0f}")
    print(f"Median price: ${filtered['price'].median():,.0f}")
    print(f"Unique parcels: {filtered['PIN'].nunique()}")


if __name__ == "__main__":
    main()
```

**Step 2: Run the script and inspect output**

```bash
cd king-county-housing-heatmap/data
python3 fetch_sales.py
```

Expected: Downloads ZIP, extracts CSV, prints column names and PropertyType values, filters to ~15-25K recent sales, saves filtered_sales.csv.

**Important:** Check the printed PropertyType values and column names. If column names differ from expected, adjust the script. If PropertyType codes need residential filtering, add appropriate codes to the filter.

**Step 3: Commit**

```bash
git add king-county-housing-heatmap/data/fetch_sales.py
git commit -m "feat: add sales data fetch script with date and price filtering"
```

---

## Task 3: Fetch Parcel Coordinates Script

**Files:**
- Create: `king-county-housing-heatmap/data/fetch_parcels.py`

**Context:** The King County ArcGIS REST API provides parcel polygons. We query the parcel_area FeatureServer, request geometry in WGS84 (EPSG:4326), and compute centroids. The API has a max of 4000 records per request, so we batch.

The endpoint: `https://gisdata.kingcounty.gov/arcgis/rest/services/OpenDataPortal/property__parcel_area/FeatureServer/0/query`

Key parameters:
- `where`: SQL filter on PIN field
- `outFields`: PIN,MAJOR,MINOR
- `outSR`: 4326 (WGS84 lat/lng)
- `returnGeometry`: true
- `f`: json
- `resultRecordCount`: 4000 max per request

**Note:** `returnCentroid=true` is NOT supported on this service. We must request polygon geometry and compute centroids using Shapely.

**Step 1: Write fetch_parcels.py**

```python
#!/usr/bin/env python3
"""Fetch parcel centroid coordinates from King County ArcGIS REST API."""

import json
import os
import time

import pandas as pd
import requests
from shapely.geometry import shape

PARCEL_API = (
    "https://gisdata.kingcounty.gov/arcgis/rest/services/"
    "OpenDataPortal/property__parcel_area/FeatureServer/0/query"
)
RAW_DIR = os.path.join(os.path.dirname(__file__), "raw")
SALES_CSV = os.path.join(RAW_DIR, "filtered_sales.csv")
OUTPUT_CSV = os.path.join(RAW_DIR, "parcel_coords.csv")
BATCH_SIZE = 100  # PINs per API request (conservative to avoid URL length limits)
RATE_LIMIT_DELAY = 0.5  # seconds between requests


def load_unique_pins():
    """Load unique PINs from filtered sales data."""
    df = pd.read_csv(SALES_CSV, dtype={"PIN": str, "Major": str, "Minor": str})
    pins = df["PIN"].unique().tolist()
    print(f"Unique parcels to geocode: {len(pins)}")
    return pins


def query_parcel_batch(pins):
    """Query ArcGIS API for a batch of PINs, return list of (PIN, lat, lng)."""
    # Build WHERE clause: PIN IN ('0123456789', '0123456790', ...)
    pin_list = ",".join(f"'{p}'" for p in pins)
    where_clause = f"PIN IN ({pin_list})"

    params = {
        "where": where_clause,
        "outFields": "PIN",
        "outSR": 4326,
        "returnGeometry": "true",
        "f": "json",
    }

    for attempt in range(4):
        try:
            resp = requests.get(PARCEL_API, params=params, timeout=60)
            resp.raise_for_status()
            data = resp.json()

            if "error" in data:
                print(f"API error: {data['error']}")
                return []

            results = []
            for feature in data.get("features", []):
                pin = feature["attributes"]["PIN"]
                geom = feature.get("geometry")
                if geom and "rings" in geom:
                    # Build a polygon and compute centroid
                    poly = shape({"type": "Polygon", "coordinates": geom["rings"]})
                    centroid = poly.centroid
                    results.append((pin, centroid.y, centroid.x))
            return results

        except (requests.RequestException, json.JSONDecodeError) as e:
            wait = 2 ** (attempt + 1)
            print(f"  Retry {attempt + 1}/4 after {wait}s: {e}")
            time.sleep(wait)

    return []


def main():
    pins = load_unique_pins()
    all_coords = []
    failed_pins = []

    total_batches = (len(pins) + BATCH_SIZE - 1) // BATCH_SIZE
    print(f"Fetching coordinates in {total_batches} batches of {BATCH_SIZE}...")

    for i in range(0, len(pins), BATCH_SIZE):
        batch = pins[i : i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1

        if batch_num % 10 == 0 or batch_num == 1:
            print(f"Batch {batch_num}/{total_batches} ({len(all_coords)} coords so far)")

        results = query_parcel_batch(batch)
        found_pins = {r[0] for r in results}
        all_coords.extend(results)

        for pin in batch:
            if pin not in found_pins:
                failed_pins.append(pin)

        time.sleep(RATE_LIMIT_DELAY)

    # Save results
    df = pd.DataFrame(all_coords, columns=["PIN", "lat", "lng"])
    df.to_csv(OUTPUT_CSV, index=False)

    match_rate = len(all_coords) / len(pins) * 100
    print(f"\nResults:")
    print(f"  Matched: {len(all_coords)} / {len(pins)} ({match_rate:.1f}%)")
    print(f"  Failed: {len(failed_pins)}")
    print(f"  Saved to: {OUTPUT_CSV}")

    if failed_pins:
        failed_path = os.path.join(RAW_DIR, "failed_pins.txt")
        with open(failed_path, "w") as f:
            f.write("\n".join(failed_pins))
        print(f"  Failed PINs saved to: {failed_path}")


if __name__ == "__main__":
    main()
```

**Step 2: Run the script**

```bash
cd king-county-housing-heatmap/data
python3 fetch_parcels.py
```

Expected: Fetches parcel coordinates in batches. This will take a while (~15-20K parcels at 100/batch = 150-200 requests). Prints progress. Target: >95% match rate. Saves parcel_coords.csv.

**Troubleshooting:**
- If the FeatureServer endpoint 403s, try the MapServer variant: change `FeatureServer/0/query` to `MapServer/0/query`
- If PIN field name differs, check the API response and adjust `outFields`
- If URL is too long with 100 PINs, reduce BATCH_SIZE to 50
- If rate limited, increase RATE_LIMIT_DELAY to 1.0 or 2.0

**Step 3: Commit**

```bash
git add king-county-housing-heatmap/data/fetch_parcels.py
git commit -m "feat: add parcel coordinate fetcher via ArcGIS REST API"
```

---

## Task 4: Join and Process Data Script

**Files:**
- Create: `king-county-housing-heatmap/data/process_data.py`

**Step 1: Write process_data.py**

```python
#!/usr/bin/env python3
"""Join sales data with parcel coordinates and output sales_data.json."""

import json
import os

import numpy as np
import pandas as pd

RAW_DIR = os.path.join(os.path.dirname(__file__), "raw")
SALES_CSV = os.path.join(RAW_DIR, "filtered_sales.csv")
COORDS_CSV = os.path.join(RAW_DIR, "parcel_coords.csv")
OUTPUT_JSON = os.path.join(
    os.path.dirname(__file__), "..", "frontend", "public", "sales_data.json"
)


def main():
    # Load data
    sales = pd.read_csv(SALES_CSV, dtype={"PIN": str})
    coords = pd.read_csv(COORDS_CSV, dtype={"PIN": str})

    print(f"Sales records: {len(sales)}")
    print(f"Parcel coordinates: {len(coords)}")

    # Join on PIN
    merged = sales.merge(coords, on="PIN", how="inner")
    print(f"Matched sales: {len(merged)} ({len(merged)/len(sales)*100:.1f}%)")

    # Drop duplicates (same parcel sold multiple times - keep most recent)
    merged = merged.sort_values("date", ascending=False)
    # Keep all sales (user may want to see historical), don't dedup

    # Filter out obvious outliers in lat/lng (King County bounds)
    merged = merged[
        (merged["lat"] >= 47.0)
        & (merged["lat"] <= 47.8)
        & (merged["lng"] >= -122.6)
        & (merged["lng"] <= -121.5)
    ]
    print(f"After geo bounds filter: {len(merged)}")

    # Calculate percentile breakpoints for color scale
    percentiles = [0, 20, 40, 60, 80, 100]
    breakpoints = np.percentile(merged["price"], percentiles).tolist()

    stats = {
        "count": len(merged),
        "min": int(merged["price"].min()),
        "max": int(merged["price"].max()),
        "median": int(merged["price"].median()),
        "mean": int(merged["price"].mean()),
        "percentiles": {str(p): int(v) for p, v in zip(percentiles, breakpoints)},
    }

    # Build output
    sales_list = []
    for _, row in merged.iterrows():
        sales_list.append(
            {
                "lat": round(row["lat"], 6),
                "lng": round(row["lng"], 6),
                "price": int(row["price"]),
                "date": row["date"],
            }
        )

    output = {
        "generated": pd.Timestamp.now().strftime("%Y-%m-%d"),
        "stats": stats,
        "sales": sales_list,
    }

    # Ensure output directory exists
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)

    with open(OUTPUT_JSON, "w") as f:
        json.dump(output, f)

    file_size = os.path.getsize(OUTPUT_JSON) / 1024 / 1024
    print(f"\nOutput: {OUTPUT_JSON}")
    print(f"File size: {file_size:.1f} MB")
    print(f"Stats: {json.dumps(stats, indent=2)}")


if __name__ == "__main__":
    main()
```

**Step 2: Run the script**

```bash
cd king-county-housing-heatmap/data
python3 process_data.py
```

Expected: Joins sales + coordinates, outputs `frontend/public/sales_data.json` (~2-3 MB). Prints stats including percentile breakpoints.

**Step 3: Commit**

```bash
git add king-county-housing-heatmap/data/process_data.py
git commit -m "feat: add data join script producing sales_data.json"
```

---

## Task 5: React App Scaffolding

**Files:**
- Create: `king-county-housing-heatmap/frontend/` (via Vite)

**Step 1: Create Vite React app**

```bash
cd king-county-housing-heatmap
npm create vite@latest frontend -- --template react
cd frontend
npm install
```

**Step 2: Install map dependencies**

```bash
cd king-county-housing-heatmap/frontend
npm install leaflet react-leaflet
```

**Step 3: Verify dev server starts**

```bash
cd king-county-housing-heatmap/frontend
npm run dev -- --host 0.0.0.0 &
# Check it starts without errors, then kill it
kill %1
```

**Step 4: Commit**

```bash
git add king-county-housing-heatmap/frontend/
git commit -m "feat: scaffold React frontend with Vite and Leaflet deps"
```

---

## Task 6: Color Scale Utility

**Files:**
- Create: `king-county-housing-heatmap/frontend/src/utils/colorScale.js`

**Step 1: Write colorScale.js**

This utility maps a sale price to a color based on percentile breakpoints from the data stats.

```javascript
/**
 * Map a price to a color based on percentile breakpoints.
 * Colors: dark green (cheap) -> light green -> yellow -> orange -> red (expensive)
 */

const COLORS = [
  [27, 120, 55],    // dark green (0-20th percentile)
  [102, 189, 99],   // light green (20-40th)
  [254, 224, 76],   // yellow (40-60th)
  [253, 141, 60],   // orange (60-80th)
  [215, 48, 39],    // red (80-100th)
];

function interpolateColor(color1, color2, t) {
  return color1.map((c, i) => Math.round(c + (color2[i] - c) * t));
}

export function createColorScale(percentiles) {
  const breaks = [
    percentiles["0"],
    percentiles["20"],
    percentiles["40"],
    percentiles["60"],
    percentiles["80"],
    percentiles["100"],
  ];

  return function getColor(price) {
    for (let i = 0; i < breaks.length - 1; i++) {
      if (price <= breaks[i + 1]) {
        const t = (price - breaks[i]) / (breaks[i + 1] - breaks[i] || 1);
        const color = i < COLORS.length - 1
          ? interpolateColor(COLORS[i], COLORS[i + 1], t)
          : COLORS[COLORS.length - 1];
        return `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
      }
    }
    return `rgb(${COLORS[COLORS.length - 1].join(", ")})`;
  };
}

export function formatPrice(price) {
  if (price >= 1000000) return `$${(price / 1000000).toFixed(1)}M`;
  if (price >= 1000) return `$${(price / 1000).toFixed(0)}K`;
  return `$${price}`;
}
```

**Step 2: Commit**

```bash
git add king-county-housing-heatmap/frontend/src/utils/colorScale.js
git commit -m "feat: add price-to-color scale utility"
```

---

## Task 7: Map Component

**Files:**
- Create: `king-county-housing-heatmap/frontend/src/components/Map.jsx`
- Create: `king-county-housing-heatmap/frontend/src/components/SalesLayer.jsx`

**Step 1: Write Map.jsx**

```jsx
import { MapContainer, TileLayer } from "react-leaflet";
import SalesLayer from "./SalesLayer";
import "leaflet/dist/leaflet.css";

const KC_CENTER = [47.5, -122.2];
const DEFAULT_ZOOM = 10;

export default function Map({ sales, getColor }) {
  return (
    <MapContainer
      center={KC_CENTER}
      zoom={DEFAULT_ZOOM}
      style={{ width: "100%", height: "100vh" }}
      preferCanvas={true}
    >
      <TileLayer
        attribution='&copy; <a href="https://carto.com/">CARTO</a>'
        url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
      />
      {sales && <SalesLayer sales={sales} getColor={getColor} />}
    </MapContainer>
  );
}
```

**Step 2: Write SalesLayer.jsx**

```jsx
import { CircleMarker, Tooltip } from "react-leaflet";
import { formatPrice } from "../utils/colorScale";

export default function SalesLayer({ sales, getColor }) {
  return (
    <>
      {sales.map((sale, i) => (
        <CircleMarker
          key={i}
          center={[sale.lat, sale.lng]}
          radius={5}
          pathOptions={{
            fillColor: getColor(sale.price),
            fillOpacity: 0.7,
            color: "#333",
            weight: 0.5,
          }}
        >
          <Tooltip>
            <div>
              <strong>{formatPrice(sale.price)}</strong>
              <br />
              {sale.date}
            </div>
          </Tooltip>
        </CircleMarker>
      ))}
    </>
  );
}
```

**Step 3: Commit**

```bash
git add king-county-housing-heatmap/frontend/src/components/
git commit -m "feat: add Map and SalesLayer components with canvas rendering"
```

---

## Task 8: Legend Component

**Files:**
- Create: `king-county-housing-heatmap/frontend/src/components/Legend.jsx`

**Step 1: Write Legend.jsx**

```jsx
import { formatPrice } from "../utils/colorScale";

const COLORS = [
  "rgb(27, 120, 55)",
  "rgb(102, 189, 99)",
  "rgb(254, 224, 76)",
  "rgb(253, 141, 60)",
  "rgb(215, 48, 39)",
];

const LABELS = ["0-20th", "20-40th", "40-60th", "60-80th", "80-100th"];

export default function Legend({ percentiles }) {
  if (!percentiles) return null;

  const breaks = ["0", "20", "40", "60", "80", "100"];

  return (
    <div
      style={{
        position: "absolute",
        bottom: 30,
        right: 10,
        background: "white",
        padding: "12px 16px",
        borderRadius: 8,
        boxShadow: "0 2px 8px rgba(0,0,0,0.2)",
        zIndex: 1000,
        fontSize: 13,
      }}
    >
      <div style={{ fontWeight: "bold", marginBottom: 8 }}>Sale Price</div>
      {COLORS.map((color, i) => (
        <div key={i} style={{ display: "flex", alignItems: "center", marginBottom: 4 }}>
          <div
            style={{
              width: 20,
              height: 14,
              backgroundColor: color,
              marginRight: 8,
              borderRadius: 2,
            }}
          />
          <span>
            {formatPrice(percentiles[breaks[i]])} - {formatPrice(percentiles[breaks[i + 1]])}
          </span>
        </div>
      ))}
    </div>
  );
}
```

**Step 2: Commit**

```bash
git add king-county-housing-heatmap/frontend/src/components/Legend.jsx
git commit -m "feat: add color legend component with percentile price ranges"
```

---

## Task 9: App.jsx - Wire Everything Together

**Files:**
- Modify: `king-county-housing-heatmap/frontend/src/App.jsx`
- Modify: `king-county-housing-heatmap/frontend/src/App.css` (replace)
- Modify: `king-county-housing-heatmap/frontend/src/index.css` (replace)

**Step 1: Write App.jsx**

```jsx
import { useEffect, useState } from "react";
import Map from "./components/Map";
import Legend from "./components/Legend";
import { createColorScale } from "./utils/colorScale";

export default function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("/sales_data.json")
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      })
      .then((json) => {
        setData(json);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100vh" }}>
        Loading sales data...
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ display: "flex", justifyContent: "center", alignItems: "center", height: "100vh", color: "red" }}>
        Error loading data: {error}
      </div>
    );
  }

  const getColor = createColorScale(data.stats.percentiles);

  return (
    <div style={{ position: "relative" }}>
      <div
        style={{
          position: "absolute",
          top: 10,
          left: 60,
          zIndex: 1000,
          background: "white",
          padding: "8px 16px",
          borderRadius: 8,
          boxShadow: "0 2px 8px rgba(0,0,0,0.2)",
          fontSize: 14,
        }}
      >
        <strong>King County Housing Sales</strong>
        <span style={{ marginLeft: 12, color: "#666" }}>
          {data.stats.count.toLocaleString()} sales | Generated {data.generated}
        </span>
      </div>
      <Map sales={data.sales} getColor={getColor} />
      <Legend percentiles={data.stats.percentiles} />
    </div>
  );
}
```

**Step 2: Replace App.css with minimal reset**

```css
/* Empty - all styles inline for simplicity */
```

**Step 3: Replace index.css with minimal reset**

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
```

**Step 4: Commit**

```bash
git add king-county-housing-heatmap/frontend/src/
git commit -m "feat: wire up App with data loading, map, and legend"
```

---

## Task 10: Create Sample Data for Development

**Files:**
- Create: `king-county-housing-heatmap/frontend/public/sales_data.json` (sample)

**Context:** While the real data pipeline runs, create a small sample JSON so frontend development can proceed independently.

**Step 1: Write a script to generate sample data**

```python
#!/usr/bin/env python3
"""Generate sample sales_data.json for frontend development."""

import json
import random

random.seed(42)

# King County approximate bounds
LAT_MIN, LAT_MAX = 47.2, 47.8
LNG_MIN, LNG_MAX = -122.5, -121.8

sales = []
for _ in range(500):
    lat = random.uniform(LAT_MIN, LAT_MAX)
    lng = random.uniform(LNG_MIN, LNG_MAX)
    # Higher prices near Seattle center (47.6, -122.3)
    dist = ((lat - 47.6) ** 2 + (lng + 122.3) ** 2) ** 0.5
    base = max(200000, 900000 - dist * 3000000)
    price = int(base * random.uniform(0.7, 1.5))
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    sales.append({
        "lat": round(lat, 6),
        "lng": round(lng, 6),
        "price": price,
        "date": f"2024-{month:02d}-{day:02d}",
    })

prices = [s["price"] for s in sales]
prices.sort()
n = len(prices)

output = {
    "generated": "2025-01-31",
    "stats": {
        "count": len(sales),
        "min": min(prices),
        "max": max(prices),
        "median": prices[n // 2],
        "mean": sum(prices) // n,
        "percentiles": {
            "0": prices[0],
            "20": prices[int(n * 0.2)],
            "40": prices[int(n * 0.4)],
            "60": prices[int(n * 0.6)],
            "80": prices[int(n * 0.8)],
            "100": prices[-1],
        },
    },
    "sales": sales,
}

with open("king-county-housing-heatmap/frontend/public/sales_data.json", "w") as f:
    json.dump(output, f, indent=2)

print(f"Generated {len(sales)} sample sales")
```

Save this as `king-county-housing-heatmap/data/generate_sample.py`, run it, then verify the frontend works with sample data.

**Step 2: Run sample generator and test frontend**

```bash
cd king-county-housing-heatmap/data
python3 generate_sample.py
cd ../frontend
npm run dev -- --host 0.0.0.0
```

Open the browser and verify: map loads, circles appear, colors vary, legend shows, tooltips work on hover.

**Step 3: Commit**

```bash
git add king-county-housing-heatmap/data/generate_sample.py
git commit -m "feat: add sample data generator for frontend development"
```

---

## Task 11: Run Full Data Pipeline

**Step 1: Run fetch_sales.py**

```bash
cd king-county-housing-heatmap/data
python3 fetch_sales.py
```

Inspect output. Check:
- Column names match expectations
- PropertyType values - identify which codes are residential
- Date range looks correct
- Price distribution is reasonable

**Step 2: Adjust filters if needed**

Based on PropertyType values seen, update fetch_sales.py to filter residential types only. Re-run.

**Step 3: Run fetch_parcels.py**

```bash
python3 fetch_parcels.py
```

This will take 10-30 minutes depending on batch size and rate limiting. Monitor progress output.

Check:
- Match rate >95%
- Coordinates look reasonable (lat ~47.x, lng ~-122.x)

**Step 4: Run process_data.py**

```bash
python3 process_data.py
```

Check:
- Output JSON is in frontend/public/sales_data.json
- Stats look reasonable
- File size is manageable (<5 MB)

**Step 5: Test frontend with real data**

```bash
cd ../frontend
npm run dev -- --host 0.0.0.0
```

Open browser. Verify real data renders correctly on the map.

**Step 6: Commit**

```bash
git add -A
git commit -m "feat: run full data pipeline with real King County sales data"
```

---

## Task 12: Final Polish and Build

**Step 1: Clean up Vite boilerplate**

Remove unused Vite template files:
- Delete `frontend/src/assets/react.svg`
- Delete `frontend/public/vite.svg`
- Update `frontend/index.html` title to "King County Housing Sales Heatmap"

**Step 2: Test production build**

```bash
cd king-county-housing-heatmap/frontend
npm run build
npx serve dist
```

Verify the production build works correctly.

**Step 3: Final commit and push**

```bash
git add -A
git commit -m "feat: finalize housing cost heatmap v1 with real data"
git push -u origin claude/housing-cost-heatmap-KvRis
```

---

## Summary of Tasks

| Task | Description | Dependencies |
|------|-------------|-------------|
| 1 | Project scaffolding | None |
| 2 | Fetch sales data script | Task 1 |
| 3 | Fetch parcel coordinates script | Task 1 |
| 4 | Join and process data script | Tasks 2, 3 |
| 5 | React app scaffolding | Task 1 |
| 6 | Color scale utility | Task 5 |
| 7 | Map + SalesLayer components | Tasks 5, 6 |
| 8 | Legend component | Tasks 5, 6 |
| 9 | App.jsx wiring | Tasks 7, 8 |
| 10 | Sample data for dev | Task 5 |
| 11 | Run full data pipeline | Tasks 2, 3, 4 |
| 12 | Final polish and build | All |

**Parallelizable:** Tasks 2+3 (data scripts), Tasks 6+7+8 (frontend components), Tasks 5+10 can run alongside Task 2+3.
