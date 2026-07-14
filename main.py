from shopify.product_fetcher import get_products
from shopify.image_downloader import download_images
from shopify.csv_generator import generate_csv
from shopify.validator import validate_csv

products = get_products()

print(f"Found {len(products)} products.")

download_images(products)

generate_csv(products)

validate_csv("output/shopify_import.csv")

print("\nEverything completed successfully!")