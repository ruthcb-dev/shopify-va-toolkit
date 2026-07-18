import re
import pandas as pd
from tkinter import filedialog


def create_handle(title):
    """
    Convert product title into a Shopify handle.
    """

    handle = title.lower()
    handle = re.sub(r"[^a-z0-9]+", "-", handle)

    return handle.strip("-")


def get_option_value(variant, index):

    return variant.get(f"option{index}", "")


def generate_csv(products, logger=None):
    """
    Generates a Shopify-compatible CSV.
    """

    if not products:
        raise ValueError("No products supplied.")

    filename = filedialog.asksaveasfilename(
        title="Save Shopify CSV",
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")],
        initialfile="shopify_export.csv"
    )

    if not filename:
        return None

    if logger:
        logger(f"Generating CSV for {len(products)} products...")

    rows = []

    for product in products:

        handle = create_handle(product["title"])

        variants = product.get("variants", [])
        images = product.get("images", [])
        options = product.get("options", [])

        option_names = ["", "", ""]

        for i, option in enumerate(options):

            if i < 3:
                option_names[i] = option["name"]

        first_variant = True

        for variant in variants:

            rows.append({

                "Handle": handle,

                "Title": product["title"] if first_variant else "",

                "Body (HTML)": product["body_html"] if first_variant else "",

                "Vendor": product["vendor"] if first_variant else "",

                "Product Category": "",

                "Type": product["product_type"] if first_variant else "",

                "Tags": product["tags"] if first_variant else "",

                "Published": "TRUE",

                "Option1 Name": option_names[0],
                "Option1 Value": get_option_value(variant, 1),

                "Option2 Name": option_names[1],
                "Option2 Value": get_option_value(variant, 2),

                "Option3 Name": option_names[2],
                "Option3 Value": get_option_value(variant, 3),

                "Variant SKU": variant.get("sku", ""),

                "Variant Grams": variant.get("grams", ""),

                "Variant Inventory Tracker": "shopify",

                "Variant Inventory Qty": variant.get(
                    "inventory_quantity",
                    0
                ),

                "Variant Inventory Policy": "deny",

                "Variant Fulfillment Service": "manual",

                "Variant Price": variant.get("price", ""),

                "Variant Compare At Price": variant.get(
                    "compare_at_price",
                    ""
                ),

                "Variant Requires Shipping": "TRUE",

                "Variant Taxable": "TRUE",

                "Variant Barcode": variant.get("barcode", ""),

                "Image Src": (
                    images[0]["src"]
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

            })

            first_variant = False

        if len(images) > 1:

            for position, image in enumerate(images[1:], start=2):

                rows.append({

                    "Handle": handle,

                    "Image Src": image["src"],

                    "Image Position": position

                })

    df = pd.DataFrame(rows)

    df.to_csv(
        filename,
        index=False,
        encoding="utf-8-sig"
    )

    if logger:
        logger("CSV generation completed.")
        logger(filename)

    return filename