#!/usr/bin/env python3
"""Generate sample sales_data.json for frontend development."""

import json
import os
import random

random.seed(42)

LAT_MIN, LAT_MAX = 47.2, 47.8
LNG_MIN, LNG_MAX = -122.5, -121.8

sales = []
for _ in range(500):
    lat = random.uniform(LAT_MIN, LAT_MAX)
    lng = random.uniform(LNG_MIN, LNG_MAX)
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

output_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "public", "sales_data.json")
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"Generated {len(sales)} sample sales")
