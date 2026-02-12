#!/usr/bin/env python3
"""Fetch parcel centroid coordinates from Snohomish County ArcGIS REST API.

Same pattern as fetch_parcels.py (King County), adapted for the Snohomish
County parcel service which uses PARCEL_ID as the key field.
"""

import json
import os
import time

import pandas as pd
import requests
from shapely.geometry import shape

PARCEL_API = (
    "https://gis.snoco.org/sas/rest/services/"
    "SAS_Services/SAS_Parcels/MapServer/0/query"
)
RAW_DIR = os.path.join(os.path.dirname(__file__), "raw")
SALES_CSV = os.path.join(RAW_DIR, "filtered_sales_snohomish.csv")
OUTPUT_CSV = os.path.join(RAW_DIR, "parcel_coords_snohomish.csv")
BATCH_SIZE = 50  # Smaller batches -- Snohomish IDs are longer (14 chars)
RATE_LIMIT_DELAY = 0.5


def load_unique_parcel_ids():
    """Load unique PARCEL_IDs from filtered Snohomish sales data."""
    df = pd.read_csv(SALES_CSV, dtype={"PARCEL_ID": str})
    ids = df["PARCEL_ID"].unique().tolist()
    print(f"Unique parcels to geocode: {len(ids)}")
    return ids


def query_parcel_batch(parcel_ids):
    """Query Snohomish ArcGIS API for a batch of PARCEL_IDs."""
    id_list = ",".join(f"'{pid}'" for pid in parcel_ids)
    where_clause = f"PARCEL_ID IN ({id_list})"

    params = {
        "where": where_clause,
        "outFields": "PARCEL_ID",
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
                pid = feature["attributes"]["PARCEL_ID"]
                geom = feature.get("geometry")
                if geom and "rings" in geom:
                    poly = shape({"type": "Polygon", "coordinates": geom["rings"]})
                    centroid = poly.centroid
                    results.append((pid, centroid.y, centroid.x))
            return results

        except (requests.RequestException, json.JSONDecodeError) as e:
            wait = 2 ** (attempt + 1)
            print(f"  Retry {attempt + 1}/4 after {wait}s: {e}")
            time.sleep(wait)

    return []


def main():
    parcel_ids = load_unique_parcel_ids()
    all_coords = []
    failed_ids = []

    total_batches = (len(parcel_ids) + BATCH_SIZE - 1) // BATCH_SIZE
    print(f"Fetching coordinates in {total_batches} batches of {BATCH_SIZE}...")

    for i in range(0, len(parcel_ids), BATCH_SIZE):
        batch = parcel_ids[i : i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1

        if batch_num % 10 == 0 or batch_num == 1:
            print(f"Batch {batch_num}/{total_batches} ({len(all_coords)} coords so far)")

        results = query_parcel_batch(batch)
        found_ids = {r[0] for r in results}
        all_coords.extend(results)

        for pid in batch:
            if pid not in found_ids:
                failed_ids.append(pid)

        time.sleep(RATE_LIMIT_DELAY)

    df = pd.DataFrame(all_coords, columns=["PARCEL_ID", "lat", "lng"])
    df.to_csv(OUTPUT_CSV, index=False)

    match_rate = len(all_coords) / len(parcel_ids) * 100 if parcel_ids else 0
    print(f"\nResults:")
    print(f"  Matched: {len(all_coords)} / {len(parcel_ids)} ({match_rate:.1f}%)")
    print(f"  Failed: {len(failed_ids)}")
    print(f"  Saved to: {OUTPUT_CSV}")

    if failed_ids:
        failed_path = os.path.join(RAW_DIR, "failed_parcel_ids_snohomish.txt")
        with open(failed_path, "w") as f:
            f.write("\n".join(failed_ids))
        print(f"  Failed IDs saved to: {failed_path}")


if __name__ == "__main__":
    main()
