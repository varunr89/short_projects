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
    sales = pd.read_csv(SALES_CSV, dtype={"PIN": str})
    coords = pd.read_csv(COORDS_CSV, dtype={"PIN": str})

    print(f"Sales records: {len(sales)}")
    print(f"Parcel coordinates: {len(coords)}")

    merged = sales.merge(coords, on="PIN", how="inner")
    print(f"Matched sales: {len(merged)} ({len(merged)/len(sales)*100:.1f}%)")

    merged = merged.sort_values("date", ascending=False)

    merged = merged[
        (merged["lat"] >= 47.0)
        & (merged["lat"] <= 47.8)
        & (merged["lng"] >= -122.6)
        & (merged["lng"] <= -121.5)
    ]
    print(f"After geo bounds filter: {len(merged)}")

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

    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)

    with open(OUTPUT_JSON, "w") as f:
        json.dump(output, f)

    file_size = os.path.getsize(OUTPUT_JSON) / 1024 / 1024
    print(f"\nOutput: {OUTPUT_JSON}")
    print(f"File size: {file_size:.1f} MB")
    print(f"Stats: {json.dumps(stats, indent=2)}")


if __name__ == "__main__":
    main()
