import pandas as pd


def validate_csv(csv_path):

    df = pd.read_csv(csv_path)

    print("\n==============================")
    print(" SHOPIFY CSV VALIDATION REPORT ")
    print("==============================")

    print(f"\nRows: {len(df)}")

    # Duplicate Handles
    duplicates = df[df["Handle"].duplicated()]

    print(f"Duplicate Handles: {len(duplicates)}")

    # Missing Titles
    missing_titles = df["Title"].fillna("").eq("").sum()

    print(f"Missing Titles: {missing_titles}")

    # Missing Prices
    missing_prices = df["Variant Price"].fillna("").eq("").sum()

    print(f"Missing Prices: {missing_prices}")

    # Missing Vendors
    missing_vendor = df["Vendor"].fillna("").eq("").sum()

    print(f"Missing Vendors: {missing_vendor}")

    # Missing Images
    missing_images = df["Image Src"].fillna("").eq("").sum()

    print(f"Missing Images: {missing_images}")

    print("\nValidation Finished.")