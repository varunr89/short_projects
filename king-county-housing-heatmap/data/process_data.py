#!/usr/bin/env python3
"""Join sales data with parcel coordinates and building data, output sales_data.json.

Merges King County and Snohomish County sales into a single dataset.
"""

import json
import os
import time

import numpy as np
import pandas as pd
import requests

RAW_DIR = os.path.join(os.path.dirname(__file__), "raw")

# King County files
KC_SALES_CSV = os.path.join(RAW_DIR, "filtered_sales.csv")
KC_COORDS_CSV = os.path.join(RAW_DIR, "parcel_coords.csv")
KC_BLDG_CSV = os.path.join(RAW_DIR, "EXTR_ResBldg.csv")

# Snohomish County files
SN_SALES_CSV = os.path.join(RAW_DIR, "filtered_sales_snohomish.csv")
SN_COORDS_CSV = os.path.join(RAW_DIR, "parcel_coords_snohomish.csv")

OUTPUT_JSON = os.path.join(
    os.path.dirname(__file__), "..", "frontend", "public", "sales_data.json"
)

# Points of interest for drive time computation (must match frontend/src/data/pois.js)
CLIMBING_GYMS = [
    {"name": "Edgeworks Bellevue", "lat": 47.6195, "lng": -122.1302},
    {"name": "Edgeworks Seattle", "lat": 47.6680, "lng": -122.3953},
    {"name": "Vertical World Seattle", "lat": 47.6610, "lng": -122.3865},
    {"name": "Vertical World North", "lat": 47.8688, "lng": -122.2981},
    {"name": "Uplift Shoreline", "lat": 47.7548, "lng": -122.3143},
    {"name": "Momentum SODO", "lat": 47.5781, "lng": -122.3348},
    {"name": "SBP Poplar", "lat": 47.5936, "lng": -122.3109},
    {"name": "SBP Fremont", "lat": 47.6502, "lng": -122.3418},
]
MICROSOFT_B43 = {"name": "Microsoft Building 43", "lat": 47.6395, "lng": -122.1344}

OSRM_TABLE_URL = "http://router.project-osrm.org/table/v1/driving"
DRIVE_BATCH_SIZE = 100
DRIVE_RATE_DELAY = 0.3


def compute_drive_times(merged):
    """Compute driving times from each sale to nearest gym and MS Building 43.

    Uses OSRM table API with sales as sources and POIs as destinations.
    Adds 'driveGym' and 'driveOffice' columns (minutes, rounded).
    """
    all_pois = CLIMBING_GYMS + [MICROSOFT_B43]
    gym_count = len(CLIMBING_GYMS)

    # Destination coords string (POIs): lng,lat;lng,lat;...
    dest_coords = [f"{p['lng']},{p['lat']}" for p in all_pois]
    dest_str = ";".join(dest_coords)
    dest_indices = ";".join(str(i) for i in range(len(all_pois)))

    lats = merged["lat"].values
    lngs = merged["lng"].values
    n = len(merged)

    drive_gym = np.full(n, np.nan)
    drive_office = np.full(n, np.nan)

    total_batches = (n + DRIVE_BATCH_SIZE - 1) // DRIVE_BATCH_SIZE
    print(f"\nComputing drive times ({total_batches} batches of {DRIVE_BATCH_SIZE})...")

    for batch_start in range(0, n, DRIVE_BATCH_SIZE):
        batch_end = min(batch_start + DRIVE_BATCH_SIZE, n)
        batch_num = batch_start // DRIVE_BATCH_SIZE + 1

        # Source coords for this batch
        src_coords = [f"{lngs[i]},{lats[i]}" for i in range(batch_start, batch_end)]
        src_count = len(src_coords)

        # Build coordinate string: sources first, then destinations
        all_coords = ";".join(src_coords + dest_coords)
        src_indices = ";".join(str(i) for i in range(src_count))
        dst_indices = ";".join(str(i) for i in range(src_count, src_count + len(all_pois)))

        url = f"{OSRM_TABLE_URL}/{all_coords}?sources={src_indices}&destinations={dst_indices}&annotations=duration"

        for attempt in range(3):
            try:
                resp = requests.get(url, timeout=30)
                resp.raise_for_status()
                data = resp.json()

                if data.get("code") != "Ok":
                    print(f"  Batch {batch_num}: OSRM error {data.get('code')}")
                    break

                durations = data["durations"]  # shape: [src_count x poi_count]
                for j, row in enumerate(durations):
                    idx = batch_start + j
                    # Nearest gym: min of first gym_count destinations
                    gym_times = [row[k] for k in range(gym_count) if row[k] is not None]
                    if gym_times:
                        drive_gym[idx] = round(min(gym_times) / 60)
                    # Office: last destination
                    if row[-1] is not None:
                        drive_office[idx] = round(row[-1] / 60)
                break

            except (requests.RequestException, json.JSONDecodeError) as e:
                wait = 2 ** (attempt + 1)
                print(f"  Batch {batch_num} retry {attempt + 1}/3 after {wait}s: {e}")
                time.sleep(wait)

        if batch_num % 20 == 0 or batch_num == 1:
            print(f"  Batch {batch_num}/{total_batches}")

        time.sleep(DRIVE_RATE_DELAY)

    merged["driveGym"] = drive_gym
    merged["driveOffice"] = drive_office

    valid_gym = np.isfinite(drive_gym).sum()
    valid_office = np.isfinite(drive_office).sum()
    print(f"  Drive times computed: gym {valid_gym}/{n}, office {valid_office}/{n}")
    print(f"  Gym range: {np.nanmin(drive_gym):.0f}-{np.nanmax(drive_gym):.0f} min")
    print(f"  Office range: {np.nanmin(drive_office):.0f}-{np.nanmax(drive_office):.0f} min")

    return merged


def load_building_data():
    """Load and deduplicate residential building data (King County only)."""
    if not os.path.exists(KC_BLDG_CSV):
        print(f"No building data found at {KC_BLDG_CSV}, skipping enrichment")
        return None

    bldg = pd.read_csv(
        KC_BLDG_CSV, dtype={"Major": str, "Minor": str}, encoding="latin-1",
        low_memory=False,
    )
    print(f"Building records loaded: {len(bldg)}")

    bldg["Major"] = bldg["Major"].str.strip().str.zfill(6)
    bldg["Minor"] = bldg["Minor"].str.strip().str.zfill(4)
    bldg["PIN"] = bldg["Major"] + bldg["Minor"]

    # Compute bathroom count
    for col in ["BathFullCount", "Bath3qtrCount", "BathHalfCount"]:
        if col not in bldg.columns:
            bldg[col] = 0
    bldg["baths"] = (
        bldg["BathFullCount"]
        + bldg["Bath3qtrCount"] * 0.75
        + bldg["BathHalfCount"] * 0.5
    )

    # Select columns we need
    keep_cols = ["PIN", "Bedrooms", "baths", "SqFtTotLiving", "YrBuilt"]
    available = [c for c in keep_cols if c in bldg.columns]
    bldg = bldg[available].copy()

    # Deduplicate: keep the record with the largest living area per PIN
    bldg = bldg.sort_values("SqFtTotLiving", ascending=False).drop_duplicates(
        subset="PIN", keep="first"
    )
    print(f"Unique building PINs: {len(bldg)}")

    # Rename to output field names
    bldg = bldg.rename(
        columns={
            "Bedrooms": "beds",
            "SqFtTotLiving": "sqft",
            "YrBuilt": "yrBuilt",
        }
    )

    # Replace zeros with NaN (0 means unknown in assessor data)
    for col in ["beds", "baths", "sqft", "yrBuilt"]:
        if col in bldg.columns:
            bldg[col] = bldg[col].replace(0, np.nan)

    return bldg


def load_king_county(bldg):
    """Load and merge King County sales with coords and building data."""
    if not os.path.exists(KC_SALES_CSV) or not os.path.exists(KC_COORDS_CSV):
        print("King County data not found, skipping")
        return pd.DataFrame()

    sales = pd.read_csv(KC_SALES_CSV, dtype={"PIN": str})
    coords = pd.read_csv(KC_COORDS_CSV, dtype={"PIN": str})

    print(f"\n--- King County ---")
    print(f"Sales records: {len(sales)}")
    print(f"Parcel coordinates: {len(coords)}")

    merged = sales.merge(coords, on="PIN", how="inner")
    print(f"Matched sales: {len(merged)} ({len(merged)/len(sales)*100:.1f}%)")

    if bldg is not None:
        before = len(merged)
        merged = merged.merge(bldg, on="PIN", how="left")
        matched = merged[["beds", "baths", "sqft", "yrBuilt"]].notna().any(axis=1).sum()
        print(f"Sales with building data: {matched} ({matched/before*100:.1f}%)")

    merged["county"] = "King"
    return merged


def load_snohomish_county():
    """Load and merge Snohomish County sales with coords.

    Building data comes from the sales CSV itself (no separate join needed).
    """
    if not os.path.exists(SN_SALES_CSV) or not os.path.exists(SN_COORDS_CSV):
        print("Snohomish County data not found, skipping")
        return pd.DataFrame()

    sales = pd.read_csv(SN_SALES_CSV, dtype={"PARCEL_ID": str})
    coords = pd.read_csv(SN_COORDS_CSV, dtype={"PARCEL_ID": str})

    print(f"\n--- Snohomish County ---")
    print(f"Sales records: {len(sales)}")
    print(f"Parcel coordinates: {len(coords)}")

    merged = sales.merge(coords, on="PARCEL_ID", how="inner")
    print(f"Matched sales: {len(merged)} ({len(merged)/len(sales)*100:.1f}%)")

    # Rename PARCEL_ID to PIN for consistency with King County
    merged = merged.rename(columns={"PARCEL_ID": "PIN"})
    merged["county"] = "Snohomish"
    return merged


def main():
    bldg = load_building_data()

    kc = load_king_county(bldg)
    sn = load_snohomish_county()

    # Ensure both DataFrames have the same building columns
    for col in ["beds", "baths", "sqft", "yrBuilt"]:
        if col not in kc.columns:
            kc[col] = np.nan
        if col not in sn.columns:
            sn[col] = np.nan

    merged = pd.concat([kc, sn], ignore_index=True)
    print(f"\n--- Combined ---")
    print(f"Total sales: {len(merged)}")
    for county in merged["county"].unique():
        count = (merged["county"] == county).sum()
        print(f"  {county}: {count}")

    merged = merged.sort_values("date", ascending=False)

    # Geo bounds filter -- widened to include Snohomish County
    merged = merged[
        (merged["lat"] >= 47.0)
        & (merged["lat"] <= 48.35)
        & (merged["lng"] >= -122.6)
        & (merged["lng"] <= -121.5)
    ]
    print(f"After geo bounds filter: {len(merged)}")

    # Compute driving times to POIs
    merged = compute_drive_times(merged)

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

    # Add filter ranges for the frontend
    has_bldg = merged["sqft"].notna()
    if has_bldg.any():
        stats["filterRanges"] = {
            "price": {"min": int(merged["price"].min()), "max": int(merged["price"].max())},
            "sqft": {
                "min": int(merged.loc[has_bldg, "sqft"].min()),
                "max": int(merged.loc[has_bldg, "sqft"].max()),
            },
            "yrBuilt": {
                "min": int(merged.loc[has_bldg, "yrBuilt"].min()),
                "max": int(merged.loc[has_bldg, "yrBuilt"].max()),
            },
            "beds": {"max": int(merged.loc[has_bldg, "beds"].max())},
            "driveGym": {"max": int(merged["driveGym"].max())},
            "driveOffice": {"max": int(merged["driveOffice"].max())},
        }

    sales_list = []
    for _, row in merged.iterrows():
        sale = {
            "lat": round(row["lat"], 6),
            "lng": round(row["lng"], 6),
            "price": int(row["price"]),
            "date": row["date"],
            "county": row["county"],
        }
        # Add building fields if available
        for field in ["beds", "baths", "sqft", "yrBuilt"]:
            if field in row.index and pd.notna(row[field]):
                val = row[field]
                sale[field] = round(val, 1) if field == "baths" else int(val)
        # Add drive times
        if pd.notna(row.get("driveGym")):
            sale["driveGym"] = int(row["driveGym"])
        if pd.notna(row.get("driveOffice")):
            sale["driveOffice"] = int(row["driveOffice"])
        sales_list.append(sale)

    output = {
        "generated": pd.Timestamp.now().strftime("%Y-%m-%d"),
        "stats": stats,
        "sales": sales_list,
    }

    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)

    with open(OUTPUT_JSON, "w") as f:
        json.dump(output, f)

    file_size = os.path.getsize(OUTPUT_JSON) / 1024 / 1024
    print(f"\nOutput: {OUTPUT_JSON}")
    print(f"File size: {file_size:.1f} MB")
    print(f"Stats: {json.dumps(stats, indent=2)}")


if __name__ == "__main__":
    main()
