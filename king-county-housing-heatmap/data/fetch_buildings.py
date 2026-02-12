#!/usr/bin/env python3
"""Download and extract King County residential building data."""

import os
import zipfile

import requests

BUILDINGS_URL = "https://aqua.kingcounty.gov/extranet/assessor/Residential%20Building.zip"
RAW_DIR = os.path.join(os.path.dirname(__file__), "raw")


def download_buildings_zip():
    """Download and extract EXTR_ResBldg CSV from King County Assessor."""
    os.makedirs(RAW_DIR, exist_ok=True)
    zip_path = os.path.join(RAW_DIR, "Residential_Building.zip")

    if os.path.exists(zip_path):
        print(f"Using cached ZIP: {zip_path}")
    else:
        print(f"Downloading building data from {BUILDINGS_URL}...")
        resp = requests.get(BUILDINGS_URL, timeout=120)
        resp.raise_for_status()
        with open(zip_path, "wb") as f:
            f.write(resp.content)
        print(f"Downloaded {len(resp.content) / 1024 / 1024:.1f} MB")

    with zipfile.ZipFile(zip_path) as zf:
        csv_names = [n for n in zf.namelist() if n.endswith(".csv")]
        print(f"Files in ZIP: {csv_names}")
        bldg_csv = next(
            (n for n in csv_names if "resbldg" in n.lower() or "bldg" in n.lower()),
            csv_names[0],
        )
        print(f"Extracting: {bldg_csv}")
        zf.extract(bldg_csv, RAW_DIR)
        extracted_path = os.path.join(RAW_DIR, bldg_csv)
        print(f"Extracted to: {extracted_path}")
        return extracted_path


def main():
    path = download_buildings_zip()
    size_mb = os.path.getsize(path) / 1024 / 1024
    print(f"\nBuilding data ready: {path} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
