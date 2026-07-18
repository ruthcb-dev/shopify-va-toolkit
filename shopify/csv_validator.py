from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "Handle",
    "Title",
    "Vendor",
    "Variant SKU",
    "Variant Price",
    "Image Src"
]


def validate_csv(
    filename,
    encoding="utf-8-sig",
    logger=None
):
    """
    Validates a Shopify CSV file.

    Parameters
    ----------
    filename : str or Path
        Full path of the CSV file to validate.

    encoding : str, optional
        Encoding used to read the CSV file.

    logger : callable, optional
        Function used for activity logging.

    Returns
    -------
    dict
        Validation summary containing row counts,
        missing columns, duplicates, and missing values.
    """

    if not filename:
        raise ValueError(
            "No CSV filename supplied."
        )

    csv_file = Path(
        filename
    ).expanduser()

    if not csv_file.exists():

        raise FileNotFoundError(
            f"CSV file not found: {csv_file}"
        )

    if not csv_file.is_file():

        raise ValueError(
            f"The selected path is not a file: {csv_file}"
        )

    if csv_file.suffix.lower() != ".csv":

        raise ValueError(
            "The selected file must be a CSV file."
        )

    if logger:

        logger(
            f"Opening CSV:\n{csv_file}"
        )

    try:

        dataframe = pd.read_csv(
            csv_file,
            encoding=encoding
        )

    except UnicodeDecodeError:

        if encoding == "utf-8-sig":

            dataframe = pd.read_csv(
                csv_file,
                encoding="utf-8"
            )

        else:

            raise

    except pd.errors.EmptyDataError as error:

        raise ValueError(
            "The selected CSV file is empty."
        ) from error

    except pd.errors.ParserError as error:

        raise ValueError(
            "The selected CSV file could not be parsed."
        ) from error

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in dataframe.columns
    ]

    if logger:

        logger("")
        logger("========== CSV Validation ==========")
        logger(
            f"Rows: {len(dataframe)}"
        )

    if missing_columns:

        if logger:

            logger("")
            logger("Missing Columns:")

            for column in missing_columns:

                logger(
                    f"   • {column}"
                )

        raise ValueError(
            "CSV is missing required columns: "
            + ", ".join(missing_columns)
        )

    duplicate_handles = (
        dataframe["Handle"]
        .fillna("")
        .replace("", pd.NA)
        .dropna()
        .duplicated()
        .sum()
    )

    duplicate_skus = (
        dataframe["Variant SKU"]
        .fillna("")
        .replace("", pd.NA)
        .dropna()
        .duplicated()
        .sum()
    )

    missing_titles = (
        dataframe["Title"]
        .fillna("")
        .astype(str)
        .str.strip()
        .eq("")
        .sum()
    )

    missing_vendors = (
        dataframe["Vendor"]
        .fillna("")
        .astype(str)
        .str.strip()
        .eq("")
        .sum()
    )

    missing_prices = (
        dataframe["Variant Price"]
        .fillna("")
        .astype(str)
        .str.strip()
        .eq("")
        .sum()
    )

    missing_images = (
        dataframe["Image Src"]
        .fillna("")
        .astype(str)
        .str.strip()
        .eq("")
        .sum()
    )

    validation_result = {
        "filename": str(
            csv_file.resolve()
        ),
        "rows": int(
            len(dataframe)
        ),
        "missing_columns": missing_columns,
        "duplicate_handles": int(
            duplicate_handles
        ),
        "duplicate_skus": int(
            duplicate_skus
        ),
        "missing_titles": int(
            missing_titles
        ),
        "missing_vendors": int(
            missing_vendors
        ),
        "missing_prices": int(
            missing_prices
        ),
        "missing_images": int(
            missing_images
        )
    }

    if logger:

        logger("")
        logger(
            f"Duplicate Handles : {duplicate_handles}"
        )
        logger(
            f"Duplicate SKUs    : {duplicate_skus}"
        )
        logger(
            f"Missing Titles    : {missing_titles}"
        )
        logger(
            f"Missing Vendors   : {missing_vendors}"
        )
        logger(
            f"Missing Prices    : {missing_prices}"
        )
        logger(
            f"Missing Images    : {missing_images}"
        )
        logger("")
        logger(
            "Validation completed successfully."
        )

    return validation_result