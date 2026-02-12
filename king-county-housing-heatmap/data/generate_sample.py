#!/usr/bin/env python3
"""Generate sample sales_data.json for frontend development."""

import json
import os
import random

import h3

random.seed(42)

# King County bounds
KC_LAT_MIN, KC_LAT_MAX = 47.2, 47.8
KC_LNG_MIN, KC_LNG_MAX = -122.5, -121.8

# Snohomish County bounds
SN_LAT_MIN, SN_LAT_MAX = 47.8, 48.3
SN_LNG_MIN, SN_LNG_MAX = -122.4, -121.7

sales = []

# King County samples (~400)
for _ in range(400):
    lat = random.uniform(KC_LAT_MIN, KC_LAT_MAX)
    lng = random.uniform(KC_LNG_MIN, KC_LNG_MAX)
    dist = ((lat - 47.6) ** 2 + (lng + 122.3) ** 2) ** 0.5
    base = max(200000, 900000 - dist * 3000000)
    price = int(base * random.uniform(0.7, 1.5))
    month = random.randint(1, 12)
    day = random.randint(1, 28)

    sale = {
        "lat": round(lat, 6),
        "lng": round(lng, 6),
        "price": price,
        "date": f"2024-{month:02d}-{day:02d}",
        "county": "King",
        "h3": h3.latlng_to_cell(lat, lng, 8),
    }

    if random.random() < 0.9:
        beds = random.choice([1, 2, 2, 3, 3, 3, 4, 4, 5, 6])
        sale["beds"] = beds
        sale["baths"] = random.choice([1, 1.5, 2, 2, 2.5, 2.5, 3, 3.5])
        sale["sqft"] = random.randint(600, 5000)
        sale["yrBuilt"] = random.randint(1900, 2024)

    # Fake drive times based on distance to POIs
    sale["driveGym"] = random.randint(5, 40)
    sale["driveOffice"] = random.randint(10, 60)

    sales.append(sale)

# Snohomish County samples (~100)
for _ in range(100):
    lat = random.uniform(SN_LAT_MIN, SN_LAT_MAX)
    lng = random.uniform(SN_LNG_MIN, SN_LNG_MAX)
    dist = ((lat - 48.0) ** 2 + (lng + 122.2) ** 2) ** 0.5
    base = max(180000, 700000 - dist * 2500000)
    price = int(base * random.uniform(0.7, 1.5))
    month = random.randint(1, 12)
    day = random.randint(1, 28)

    sale = {
        "lat": round(lat, 6),
        "lng": round(lng, 6),
        "price": price,
        "date": f"2024-{month:02d}-{day:02d}",
        "county": "Snohomish",
        "h3": h3.latlng_to_cell(lat, lng, 8),
    }

    if random.random() < 0.9:
        beds = random.choice([1, 2, 2, 3, 3, 3, 4, 4, 5, 6])
        sale["beds"] = beds
        sale["baths"] = random.choice([1, 1.5, 2, 2, 2.5, 2.5, 3, 3.5])
        sale["sqft"] = random.randint(600, 5000)
        sale["yrBuilt"] = random.randint(1900, 2024)

    # Fake drive times based on distance to POIs
    sale["driveGym"] = random.randint(5, 40)
    sale["driveOffice"] = random.randint(10, 60)

    sales.append(sale)

prices = [s["price"] for s in sales]
prices.sort()
n = len(prices)

# Compute filter ranges from sales that have building data
sqft_vals = [s["sqft"] for s in sales if "sqft" in s]
yr_vals = [s["yrBuilt"] for s in sales if "yrBuilt" in s]
bed_vals = [s["beds"] for s in sales if "beds" in s]

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
        "filterRanges": {
            "price": {"min": min(prices), "max": max(prices)},
            "sqft": {"min": min(sqft_vals), "max": max(sqft_vals)},
            "yrBuilt": {"min": min(yr_vals), "max": max(yr_vals)},
            "beds": {"max": max(bed_vals)},
            "driveGym": {"max": max(s["driveGym"] for s in sales)},
            "driveOffice": {"max": max(s["driveOffice"] for s in sales)},
        },
    },
    "sales": sales,
}

output_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "public", "sales_data.json")
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"Generated {len(sales)} sample sales")
kc_count = sum(1 for s in sales if s["county"] == "King")
sn_count = sum(1 for s in sales if s["county"] == "Snohomish")
print(f"  King County: {kc_count}")
print(f"  Snohomish County: {sn_count}")
with_bldg = sum(1 for s in sales if "beds" in s)
print(f"  With building data: {with_bldg} ({with_bldg/len(sales)*100:.0f}%)")
print(f"  Filter ranges: sqft {min(sqft_vals)}-{max(sqft_vals)}, yr {min(yr_vals)}-{max(yr_vals)}, beds max {max(bed_vals)}")
