#!/usr/bin/env python3
"""Fetch traffic-aware drive times from Google Maps Distance Matrix API.

Reads routing centroids (res-7 hex centers) and computes drive times to
Microsoft Building 43 and all climbing gyms. Results are cached so re-runs
skip already-computed hexes.

Requires GOOGLE_MAPS_API_KEY environment variable.
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta, timezone

import googlemaps

RAW_DIR = os.path.join(os.path.dirname(__file__), "raw")
CENTROIDS_PATH = os.path.join(RAW_DIR, "routing_centroids.json")
CACHE_PATH = os.path.join(RAW_DIR, "google_routes_cache.json")

# POIs (must match frontend/src/data/pois.js and process_data.py)
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

# All destinations: gyms first, then office
ALL_DESTINATIONS = [(g["lat"], g["lng"]) for g in CLIMBING_GYMS] + [
    (MICROSOFT_B43["lat"], MICROSOFT_B43["lng"])
]
GYM_COUNT = len(CLIMBING_GYMS)

BATCH_SIZE = 10  # max origins per request (10 * 9 destinations = 90 elements < 100 limit)


def next_tuesday_8am_pacific():
    """Return next Tuesday at 8 AM Pacific as a datetime for departure_time."""
    # Pacific time is UTC-8 (PST) or UTC-7 (PDT)
    # Use a fixed UTC offset for simplicity; Google handles DST internally
    pacific = timezone(timedelta(hours=-8))
    now = datetime.now(pacific)
    days_until_tuesday = (1 - now.weekday()) % 7
    if days_until_tuesday == 0:
        days_until_tuesday = 7  # next week if today is Tuesday
    next_tue = now + timedelta(days=days_until_tuesday)
    return next_tue.replace(hour=8, minute=0, second=0, microsecond=0)


def main():
    api_key = os.environ.get("GOOGLE_MAPS_API_KEY")
    if not api_key:
        print("ERROR: Set GOOGLE_MAPS_API_KEY environment variable")
        sys.exit(1)

    gmaps = googlemaps.Client(key=api_key)

    # Load centroids
    with open(CENTROIDS_PATH) as f:
        centroids = json.load(f)
    print(f"Routing centroids loaded: {len(centroids)}")

    # Load existing cache
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH) as f:
            cache = json.load(f)
        print(f"Existing cache entries: {len(cache)}")
    else:
        cache = {}

    # Filter to only hexes not yet cached
    to_process = {k: v for k, v in centroids.items() if k not in cache}
    print(f"Hexes to process: {len(to_process)} (skipping {len(centroids) - len(to_process)} cached)")

    if not to_process:
        print("Nothing to do, all hexes cached.")
        return

    departure = next_tuesday_8am_pacific()
    print(f"Departure time: {departure}")

    hex_ids = list(to_process.keys())
    total_batches = (len(hex_ids) + BATCH_SIZE - 1) // BATCH_SIZE
    total_elements = len(hex_ids) * len(ALL_DESTINATIONS)
    est_cost = total_elements / 1000 * 10  # $10 per 1000 elements (traffic-aware)
    print(f"Total API elements: {total_elements} (est. cost: ${est_cost:.2f})")
    print(f"Batches: {total_batches} of {BATCH_SIZE} origins each")
    print()

    processed = 0
    errors = 0

    for batch_start in range(0, len(hex_ids), BATCH_SIZE):
        batch_hex_ids = hex_ids[batch_start : batch_start + BATCH_SIZE]
        batch_num = batch_start // BATCH_SIZE + 1

        origins = [(to_process[h]["lat"], to_process[h]["lng"]) for h in batch_hex_ids]

        try:
            result = gmaps.distance_matrix(
                origins=origins,
                destinations=ALL_DESTINATIONS,
                mode="driving",
                departure_time=departure,
            )

            for i, hex_id in enumerate(batch_hex_ids):
                row = result["rows"][i]
                elements = row["elements"]

                # Find nearest gym (min duration among first GYM_COUNT destinations)
                best_gym_minutes = None
                best_gym_name = None
                for j in range(GYM_COUNT):
                    el = elements[j]
                    if el["status"] == "OK":
                        minutes = round(el["duration_in_traffic"]["value"] / 60)
                        if best_gym_minutes is None or minutes < best_gym_minutes:
                            best_gym_minutes = minutes
                            best_gym_name = CLIMBING_GYMS[j]["name"]

                # Office is the last destination
                office_el = elements[-1]
                office_minutes = None
                if office_el["status"] == "OK":
                    office_minutes = round(office_el["duration_in_traffic"]["value"] / 60)

                cache[hex_id] = {
                    "nearestGymMinutes": best_gym_minutes,
                    "nearestGymName": best_gym_name,
                    "officeMinutes": office_minutes,
                }
                processed += 1

        except Exception as e:
            print(f"  Batch {batch_num} ERROR: {e}")
            errors += 1
            time.sleep(2)
            continue

        # Save cache after each batch (incremental)
        with open(CACHE_PATH, "w") as f:
            json.dump(cache, f)

        if batch_num % 5 == 0 or batch_num == 1 or batch_num == total_batches:
            print(f"  Batch {batch_num}/{total_batches} -- {processed} hexes done")

        # Rate limit: ~10 requests/sec is safe, but be conservative
        time.sleep(0.5)

    print(f"\nDone! Processed: {processed}, Errors: {errors}")
    print(f"Total cache entries: {len(cache)}")

    # Sanity check: print a few results
    sample_keys = list(cache.keys())[:3]
    for k in sample_keys:
        entry = cache[k]
        print(f"  {k}: gym={entry['nearestGymMinutes']}min ({entry['nearestGymName']}), office={entry['officeMinutes']}min")


if __name__ == "__main__":
    main()
