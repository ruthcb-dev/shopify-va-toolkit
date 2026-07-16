from shopify.product_fetcher import get_products


class AppController:
    """
    Coordinates the application's business logic.

    The controller acts as the bridge between the GUI and the
    Shopify modules.
    """

    def __init__(self):

        self.products = []

    def fetch_products(self):
        """
        Fetch products from Shopify.

        Returns:
            list: Shopify products.
        """

        self.products = get_products()

        return self.products

    def get_products(self):
        """
        Returns the products currently loaded in memory.
        """

        return self.products