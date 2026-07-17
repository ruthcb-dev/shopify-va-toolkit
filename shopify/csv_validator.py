import pandas as pd
from tkinter import filedialog


def validate_csv(logger=None):
    """
    Validates a Shopify CSV file.

    Returns:
        True if validation completed,
        False if cancelled.
    """

    filename = filedialog.askopenfilename(
        title="Select Shopify CSV",
        filetypes=[
            ("CSV Files", "*.csv")
        ]
    )

    if not filename:
        return False

    if logger:
        logger(f"Opening CSV:\n{filename}")

    df = pd.read_csv(filename)

    if logger:
        logger("")
        logger("========== CSV Validation ==========")
        logger(f"Rows: {len(df)}")

    required_columns = [
        "Handle",
        "Title",
        "Vendor",
        "Variant SKU",
        "Variant Price",
        "Image Src"
    ]

    missing_columns = []

    for column in required_columns:

        if column not in df.columns:
            missing_columns.append(column)

    if missing_columns:

        if logger:
            logger("")
            logger("Missing Columns:")

            for column in missing_columns:
                logger(f"   • {column}")

        raise ValueError("CSV is missing required columns.")

    duplicate_handles = df["Handle"].duplicated().sum()

    duplicate_skus = (
        df["Variant SKU"]
        .fillna("")
        .replace("", pd.NA)
        .dropna()
        .duplicated()
        .sum()
    )

    missing_titles = (
        df["Title"]
        .fillna("")
        .eq("")
        .sum()
    )

    missing_prices = (
        df["Variant Price"]
        .fillna("")
        .eq("")
        .sum()
    )

    missing_vendor = (
        df["Vendor"]
        .fillna("")
        .eq("")
        .sum()
    )

    missing_images = (
        df["Image Src"]
        .fillna("")
        .eq("")
        .sum()
    )

    if logger:

        logger("")
        logger("Duplicate Handles : {}".format(duplicate_handles))
        logger("Duplicate SKUs    : {}".format(duplicate_skus))
        logger("Missing Titles    : {}".format(missing_titles))
        logger("Missing Vendors   : {}".format(missing_vendor))
        logger("Missing Prices    : {}".format(missing_prices))
        logger("Missing Images    : {}".format(missing_images))
        logger("")
        logger("Validation completed successfully.")

    return True