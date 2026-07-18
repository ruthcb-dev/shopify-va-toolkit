from pathlib import Path
from urllib.parse import unquote, urlparse

import requests

from config import HEADERS


def clean_filename(name):
    """
    Removes characters that Windows does not allow in filenames.

    Parameters
    ----------
    name : str
        Original filename or folder name.

    Returns
    -------
    str
        Windows-safe filename.
    """

    cleaned_name = "".join(
        character
        for character in str(name or "")
        if character.isalnum()
        or character in (" ", "-", "_", ".")
    ).strip()

    return cleaned_name or "Unknown Product"


def get_image_filename(image_url, image_index):
    """
    Extracts and cleans an image filename from its URL.

    A fallback filename is generated when the URL does not contain one.
    """

    parsed_url = urlparse(image_url)

    original_filename = Path(
        unquote(parsed_url.path)
    ).name

    if not original_filename:

        return f"image_{image_index}.jpg"

    filename_path = Path(original_filename)

    safe_stem = clean_filename(
        filename_path.stem
    )

    safe_suffix = filename_path.suffix.lower()

    if not safe_suffix:

        safe_suffix = ".jpg"

    return f"{safe_stem}{safe_suffix}"


def create_unique_filepath(
    product_folder,
    filename
):
    """
    Creates a unique destination path when two images share a filename.
    """

    filepath = product_folder / filename

    if not filepath.exists():

        return filepath

    filename_path = Path(filename)

    stem = filename_path.stem
    suffix = filename_path.suffix

    counter = 2

    while True:

        candidate = product_folder / (
            f"{stem}_{counter}{suffix}"
        )

        if not candidate.exists():

            return candidate

        counter += 1


def download_images(
    products,
    output_folder="images",
    logger=None
):
    """
    Downloads Shopify product images.

    Parameters
    ----------
    products : list
        Shopify product records.

    output_folder : str or Path, optional
        Root folder where product-image folders are created.

    logger : callable, optional
        Function used for activity logging.

    Returns
    -------
    dict
        Download summary containing downloaded, skipped,
        failed, and product counts.
    """

    if not products:

        raise ValueError(
            "No products supplied."
        )

    if not output_folder:

        raise ValueError(
            "No image output folder supplied."
        )

    destination_folder = Path(
        output_folder
    ).expanduser()

    destination_folder.mkdir(
        parents=True,
        exist_ok=True
    )

    downloaded = 0
    skipped = 0
    failed = 0

    total_products = len(products)

    if logger:

        logger(
            f"Image folder: {destination_folder.resolve()}"
        )

        logger(
            f"Processing {total_products} products..."
        )

    with requests.Session() as session:

        session.headers.update(
            HEADERS
        )

        for product_index, product in enumerate(
            products,
            start=1
        ):

            product_name = clean_filename(
                product.get(
                    "title",
                    "Unknown Product"
                )
            )

            product_folder = (
                destination_folder
                / product_name
            )

            product_folder.mkdir(
                parents=True,
                exist_ok=True
            )

            if logger:

                logger(
                    f"[{product_index}/{total_products}] "
                    f"{product_name}"
                )

            images = product.get(
                "images",
                []
            )

            if not images:

                if logger:

                    logger(
                        "   No images found."
                    )

                continue

            for image_index, image in enumerate(
                images,
                start=1
            ):

                image_url = image.get(
                    "src",
                    ""
                )

                if not image_url:

                    skipped += 1

                    if logger:

                        logger(
                            "   Skipped image with no URL."
                        )

                    continue

                filename = get_image_filename(
                    image_url,
                    image_index
                )

                expected_filepath = (
                    product_folder
                    / filename
                )

                if expected_filepath.exists():

                    skipped += 1

                    if logger:

                        logger(
                            f"   Already exists: {filename}"
                        )

                    continue

                filepath = create_unique_filepath(
                    product_folder,
                    filename
                )

                try:

                    response = session.get(
                        image_url,
                        timeout=30
                    )

                    response.raise_for_status()

                    with filepath.open(
                        "wb"
                    ) as file:

                        file.write(
                            response.content
                        )

                    downloaded += 1

                    if logger:

                        logger(
                            f"   Downloaded: {filepath.name}"
                        )

                except requests.RequestException as error:

                    failed += 1

                    if logger:

                        logger(
                            f"   Failed: {filename} — {error}"
                        )

                except OSError as error:

                    failed += 1

                    if logger:

                        logger(
                            f"   Could not save {filename} — {error}"
                        )

    result = {
        "downloaded": downloaded,
        "skipped": skipped,
        "failed": failed,
        "products": total_products,
        "output_folder": str(
            destination_folder.resolve()
        )
    }

    if logger:

        logger("")
        logger("Image download completed.")
        logger(
            f"Downloaded : {downloaded}"
        )
        logger(
            f"Skipped    : {skipped}"
        )
        logger(
            f"Failed     : {failed}"
        )

    return result