import os
import requests
from urllib.parse import urlparse
from config import HEADERS


def clean_filename(name):
    """Remove characters that Windows doesn't allow in file names."""
    return "".join(c for c in name if c.isalnum() or c in (" ", "-", "_")).strip()


def download_images(products):
    os.makedirs("images", exist_ok=True)

    for product in products:

        product_name = clean_filename(product["title"])

        product_folder = os.path.join("images", product_name)

        os.makedirs(product_folder, exist_ok=True)

        print(f"\nDownloading images for: {product_name}")

        for image in product["images"]:

            image_url = image["src"]

            filename = os.path.basename(urlparse(image_url).path)

            filepath = os.path.join(product_folder, filename)

            # Skip if already downloaded
            if os.path.exists(filepath):
                print(f"   ✓ Already exists: {filename}")
                continue

            response = requests.get(image_url, headers=HEADERS)

            with open(filepath, "wb") as f:
                f.write(response.content)

            print(f"   ✓ Downloaded: {filename}")