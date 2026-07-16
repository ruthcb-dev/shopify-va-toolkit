from shopify.product_fetcher import get_products


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

        # Empty search returns all products
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