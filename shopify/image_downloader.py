import os
from urllib.parse import urlparse

import requests

from config import HEADERS


def clean_filename(name):
    """
    Removes characters that Windows does not allow
    in filenames.
    """

    return "".join(
        c for c in name
        if c.isalnum() or c in (" ", "-", "_")
    ).strip()


def download_images(products, logger=None):
    """
    Downloads product images.

    Parameters
    ----------
    products : list
        Shopify product list.

    logger : callable, optional
        Function used for logging progress.

        Example:
            logger("Downloading image...")
    """

    os.makedirs("images", exist_ok=True)

    downloaded = 0
    skipped = 0

    total_products = len(products)

    for product_index, product in enumerate(products, start=1):

        product_name = clean_filename(
            product.get("title", "Unknown Product")
        )

        product_folder = os.path.join(
            "images",
            product_name
        )

        os.makedirs(
            product_folder,
            exist_ok=True
        )

        if logger:
            logger(
                f"[{product_index}/{total_products}] {product_name}"
            )

        for image in product.get("images", []):

            image_url = image.get("src")

            if not image_url:
                continue

            filename = os.path.basename(
                urlparse(image_url).path
            )

            filepath = os.path.join(
                product_folder,
                filename
            )

            if os.path.exists(filepath):

                skipped += 1

                if logger:
                    logger(
                        f"   ✓ Already exists: {filename}"
                    )

                continue

            response = requests.get(
                image_url,
                headers=HEADERS,
                timeout=30
            )

            response.raise_for_status()

            with open(filepath, "wb") as file:

                file.write(response.content)

            downloaded += 1

            if logger:
                logger(
                    f"   ✓ Downloaded: {filename}"
                )

    if logger:

        logger("")

        logger("Image download completed.")

        logger(
            f"Downloaded : {downloaded}"
        )

        logger(
            f"Skipped     : {skipped}"
        )

    return {
        "downloaded": downloaded,
        "skipped": skipped,
        "products": total_products
    }