from shopify.product_fetcher import get_products
from shopify.image_downloader import download_images
from shopify.csv_generator import generate_csv
from shopify.csv_validator import validate_csv


class AppController:
    """
    Coordinates communication between the GUI and
    the Shopify service layer.
    """

    def __init__(self):

        self.products = []

    # ==========================================================
    # Product Retrieval
    # ==========================================================

    def fetch_products(self):

        self.products = get_products()

        return self.products

    # ==========================================================
    # Product Search
    # ==========================================================

    def search_products(self, search_text):

        search_text = search_text.strip().lower()

        if not search_text:
            return self.products

        filtered = []

        for product in self.products:

            variants = product.get("variants", [])
            variant = variants[0] if variants else {}

            searchable = " ".join([
                str(product.get("title", "")),
                str(product.get("vendor", "")),
                str(product.get("product_type", "")),
                str(variant.get("sku", "")),
                " ".join(product.get("tags", []))
            ]).lower()

            if search_text in searchable:
                filtered.append(product)

        return filtered

    # ==========================================================
    # Image Download
    # ==========================================================

    def download_product_images(
        self,
        logger=None,
        products=None
    ):

        if products is None:
            products = self.products

        return download_images(
            products,
            logger=logger
        )

    # ==========================================================
    # CSV Generator
    # ==========================================================

    def generate_csv(
        self,
        logger=None,
        products=None
    ):

        if products is None:
            products = self.products

        return generate_csv(
            products,
            logger=logger
        )

    # ==========================================================
    # CSV Validation
    # ==========================================================

    def validate_csv(
        self,
        logger=None
    ):

        return validate_csv(
            logger=logger
        )