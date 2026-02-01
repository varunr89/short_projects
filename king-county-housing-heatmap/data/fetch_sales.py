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
    if "PropertyType" in df.columns:
        residential_types = df["PropertyType"].value_counts()
        print(f"\nAll PropertyType values in filtered data:\n{residential_types}")

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
