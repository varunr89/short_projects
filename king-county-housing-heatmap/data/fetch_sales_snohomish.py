#!/usr/bin/env python3
"""Download and filter Snohomish County real property sales data.

Data source: Snohomish County Assessor 5-year sales Excel file.
The file has two sheets: "Disclaimer" (skip) and "AllSales" (the data).

Key columns in AllSales:
  Parcel_Id, Sale_Date, Sale_Price, Prop_Class, Bedrooms, Yr_Blt, Total_SqFt
"""

import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import requests

SALES_URL = "https://snohomishcountywa.gov/DocumentCenter/View/109438"
RAW_DIR = os.path.join(os.path.dirname(__file__), "raw")
EXCEL_PATH = os.path.join(RAW_DIR, "Snohomish_All_Sales.xlsx")
OUTPUT_CSV = os.path.join(RAW_DIR, "filtered_sales_snohomish.csv")


def download_excel():
    """Download the Snohomish County 5-year sales Excel file."""
    os.makedirs(RAW_DIR, exist_ok=True)

    if os.path.exists(EXCEL_PATH):
        print(f"Using cached Excel: {EXCEL_PATH}")
    else:
        print(f"Downloading sales data from {SALES_URL}...")
        resp = requests.get(SALES_URL, timeout=120)
        resp.raise_for_status()
        with open(EXCEL_PATH, "wb") as f:
            f.write(resp.content)
        print(f"Downloaded {len(resp.content) / 1024 / 1024:.1f} MB")

    df = pd.read_excel(
        EXCEL_PATH,
        sheet_name="AllSales",
        dtype={"Parcel_Id": str, "Prop_Class": str},
    )
    print(f"Columns: {list(df.columns)}")
    print(f"Total records: {len(df)}")
    return df


def filter_sales(df):
    """Filter to recent residential sales with valid prices."""
    print(f"Columns: {list(df.columns)}")

    # Parse sale date
    df["sale_date"] = pd.to_datetime(df["Sale_Date"], format="mixed", errors="coerce")

    # Parse sale price
    df["sale_price"] = pd.to_numeric(df["Sale_Price"], errors="coerce")

    # Filter: last 12 months
    one_year_ago = datetime.now() - timedelta(days=365)
    df = df[df["sale_date"] >= one_year_ago]
    print(f"After date filter (>= {one_year_ago.date()}): {len(df)}")

    # Filter: price range $50K - $10M
    df = df[df["sale_price"].notna()]
    df = df[(df["sale_price"] >= 50000) & (df["sale_price"] <= 10000000)]
    print(f"After price range filter ($50K-$10M): {len(df)}")

    # Filter: residential property classes (1xx codes = residential)
    if "Prop_Class" in df.columns:
        print(f"\nProp_Class value counts (top 20):\n{df['Prop_Class'].value_counts().head(20)}")
        prop_num = pd.to_numeric(df["Prop_Class"], errors="coerce")
        residential_mask = (prop_num >= 100) & (prop_num < 200)
        df = df[residential_mask]
        print(f"After residential filter (Prop_Class 1xx): {len(df)}")

    # Normalize PARCEL_ID (already string, just strip)
    df["PARCEL_ID"] = df["Parcel_Id"].str.strip()
    df = df[df["PARCEL_ID"].str.len() > 0]

    # Build output with building data from the same file
    output = pd.DataFrame()
    output["PARCEL_ID"] = df["PARCEL_ID"].values
    output["date"] = df["sale_date"].dt.strftime("%Y-%m-%d").values
    output["price"] = df["sale_price"].astype(int).values

    # Bedrooms
    if "Bedrooms" in df.columns:
        output["beds"] = pd.to_numeric(df["Bedrooms"].values, errors="coerce")

    # No dedicated baths column in this dataset

    # Square footage
    if "Total_SqFt" in df.columns:
        output["sqft"] = pd.to_numeric(df["Total_SqFt"].values, errors="coerce")

    # Year built
    if "Yr_Blt" in df.columns:
        output["yrBuilt"] = pd.to_numeric(df["Yr_Blt"].values, errors="coerce")

    # Replace zeros with NaN (0 means unknown in assessor data)
    for col in ["beds", "sqft", "yrBuilt"]:
        if col in output.columns:
            output[col] = output[col].replace(0, np.nan)

    return output


def main():
    df = download_excel()
    filtered = filter_sales(df)
    filtered.to_csv(OUTPUT_CSV, index=False)
    print(f"\nSaved {len(filtered)} filtered sales to {OUTPUT_CSV}")
    print(f"Price range: ${filtered['price'].min():,.0f} - ${filtered['price'].max():,.0f}")
    print(f"Median price: ${filtered['price'].median():,.0f}")
    print(f"Unique parcels: {filtered['PARCEL_ID'].nunique()}")

    for col in ["beds", "sqft", "yrBuilt"]:
        if col in filtered.columns:
            valid = filtered[col].notna().sum()
            print(f"  {col}: {valid} values ({valid/len(filtered)*100:.0f}%)")


if __name__ == "__main__":
    main()
