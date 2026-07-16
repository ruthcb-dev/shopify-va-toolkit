from shopify.product_fetcher import get_products
from shopify.image_downloader import download_images


class AppController:
    """
    Coordinates communication between the GUI and
    the Shopify service layer.
    """

    def __init__(self):

        # Complete product list fetched from Shopify
        self.products = []

    # ==========================================================
    # Product Retrieval
    # ==========================================================

    def fetch_products(self):
        """
        Retrieves all products from Shopify and stores
        them in memory.
        """

        self.products = get_products()

        return self.products

    # ==========================================================
    # Search
    # ==========================================================

    def search_products(self, search_text):
        """
        Searches products by:
        - Title
        - Vendor
        - Product Type
        - SKU
        - Tags
        """

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
    # Images
    # ==========================================================

    def download_product_images(self, products=None):
        """
        Downloads images for the supplied products.

        If no product list is supplied, downloads images
        for every loaded product.
        """

        if products is None:
            products = self.products

        download_images(products)

        return len(products)