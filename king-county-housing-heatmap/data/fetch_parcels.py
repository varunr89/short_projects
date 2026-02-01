#!/usr/bin/env python3
"""Fetch parcel centroid coordinates from King County ArcGIS REST API.

Troubleshooting:
- If the FeatureServer endpoint 403s, try the MapServer variant:
  change FeatureServer/0/query to MapServer/0/query
- If PIN field name differs, check the API response and adjust outFields
- If URL is too long with 100 PINs, reduce BATCH_SIZE to 50
- If rate limited, increase RATE_LIMIT_DELAY to 1.0 or 2.0
"""

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
