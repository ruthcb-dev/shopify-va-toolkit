import re
from pathlib import Path

import pandas as pd


def create_handle(title):
    """
    Converts a product title into a Shopify-compatible handle.
    """

    title = str(title or "").lower()
    handle = re.sub(r"[^a-z0-9]+", "-", title)

    return handle.strip("-")


def get_option_value(variant, index):
    """
    Returns a Shopify variant option value.
    """

    return variant.get(
        f"option{index}",
        ""
    )


def format_tags(tags):
    """
    Converts Shopify tags into a CSV-friendly string.
    """

    if isinstance(tags, list):
        return ", ".join(
            str(tag) for tag in tags
        )

    return str(tags or "")


def generate_csv(
    products,
    filename,
    encoding="utf-8-sig",
    logger=None
):
    """
    Generates a Shopify-compatible CSV file.

    Parameters
    ----------
    products : list
        Shopify product records.

    filename : str or Path
        Full destination path for the generated CSV.

    encoding : str, optional
        CSV file encoding.

    logger : callable, optional
        Function used for activity logging.

    Returns
    -------
    str
        Full path of the generated CSV file.
    """

    if not products:
        raise ValueError(
            "No products supplied."
        )

    if not filename:
        raise ValueError(
            "No output filename supplied."
        )

    output_file = Path(
        filename
    ).expanduser()

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    if logger:

        logger(
            f"Generating CSV for {len(products)} products..."
        )

        logger(
            f"Output file: {output_file}"
        )

    rows = []

    for product in products:

        product_title = product.get(
            "title",
            ""
        )

        handle = create_handle(
            product_title
        )

        variants = product.get(
            "variants",
            []
        )

        images = product.get(
            "images",
            []
        )

        options = product.get(
            "options",
            []
        )

        option_names = [
            "",
            "",
            ""
        ]

        for index, option in enumerate(options):

            if index >= 3:
                break

            option_names[index] = option.get(
                "name",
                ""
            )

        first_variant = True

        for variant in variants:

            rows.append(
                {
                    "Handle": handle,

                    "Title": (
                        product_title
                        if first_variant
                        else ""
                    ),

                    "Body (HTML)": (
                        product.get(
                            "body_html",
                            ""
                        )
                        if first_variant
                        else ""
                    ),

                    "Vendor": (
                        product.get(
                            "vendor",
                            ""
                        )
                        if first_variant
                        else ""
                    ),

                    "Product Category": "",

                    "Type": (
                        product.get(
                            "product_type",
                            ""
                        )
                        if first_variant
                        else ""
                    ),

                    "Tags": (
                        format_tags(
                            product.get(
                                "tags",
                                []
                            )
                        )
                        if first_variant
                        else ""
                    ),

                    "Published": "TRUE",

                    "Option1 Name": option_names[0],

                    "Option1 Value": get_option_value(
                        variant,
                        1
                    ),

                    "Option2 Name": option_names[1],

                    "Option2 Value": get_option_value(
                        variant,
                        2
                    ),

                    "Option3 Name": option_names[2],

                    "Option3 Value": get_option_value(
                        variant,
                        3
                    ),

                    "Variant SKU": variant.get(
                        "sku",
                        ""
                    ),

                    "Variant Grams": variant.get(
                        "grams",
                        ""
                    ),

                    "Variant Inventory Tracker": "shopify",

                    "Variant Inventory Qty": variant.get(
                        "inventory_quantity",
                        0
                    ),

                    "Variant Inventory Policy": "deny",

                    "Variant Fulfillment Service": "manual",

                    "Variant Price": variant.get(
                        "price",
                        ""
                    ),

                    "Variant Compare At Price": variant.get(
                        "compare_at_price",
                        ""
                    ),

                    "Variant Requires Shipping": "TRUE",

                    "Variant Taxable": "TRUE",

                    "Variant Barcode": variant.get(
                        "barcode",
                        ""
                    ),

                    "Image Src": (
                        images[0].get(
                            "src",
                            ""
                        )
                        if first_variant and images
                        else ""
                    ),

                    "Image Position": (
                        1
                        if first_variant and images
                        else ""
                    ),

                    "Gift Card": "FALSE",

                    "SEO Title": "",

                    "SEO Description": "",

                    "Google Shopping / Gender": "",

                    "Google Shopping / Age Group": "",

                    "Google Shopping / MPN": "",

                    "Google Shopping / Condition": "",

                    "Google Shopping / Custom Product": "",

                    "Google Shopping / Custom Label 0": "",

                    "Status": "draft"
                }
            )

            first_variant = False

        if len(images) > 1:

            for position, image in enumerate(
                images[1:],
                start=2
            ):

                rows.append(
                    {
                        "Handle": handle,

                        "Image Src": image.get(
                            "src",
                            ""
                        ),

                        "Image Position": position
                    }
                )

    if not rows:

        raise ValueError(
            "The selected products contain no exportable variants."
        )

    dataframe = pd.DataFrame(
        rows
    )

    dataframe.to_csv(
        output_file,
        index=False,
        encoding=encoding
    )

    if logger:

        logger(
            "CSV generation completed."
        )

        logger(
            str(output_file)
        )

    return str(
        output_file.resolve()
    )