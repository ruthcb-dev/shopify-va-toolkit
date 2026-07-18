from shopify.csv_generator import generate_csv
from shopify.csv_validator import validate_csv
from shopify.image_downloader import download_images
from shopify.product_fetcher import get_products


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

        search_text = str(
            search_text or ""
        ).strip().lower()

        if not search_text:

            return self.products

        filtered_products = []

        for product in self.products:

            variants = product.get(
                "variants",
                []
            )

            variant_skus = " ".join(
                str(
                    variant.get(
                        "sku",
                        ""
                    )
                )
                for variant in variants
            )

            tags = product.get(
                "tags",
                []
            )

            if isinstance(tags, list):

                tags_text = " ".join(
                    str(tag)
                    for tag in tags
                )

            else:

                tags_text = str(
                    tags or ""
                )

            searchable_text = " ".join(
                [
                    str(
                        product.get(
                            "title",
                            ""
                        )
                    ),
                    str(
                        product.get(
                            "vendor",
                            ""
                        )
                    ),
                    str(
                        product.get(
                            "product_type",
                            ""
                        )
                    ),
                    variant_skus,
                    tags_text
                ]
            ).lower()

            if search_text in searchable_text:

                filtered_products.append(
                    product
                )

        return filtered_products

    # ==========================================================
    # Image Download
    # ==========================================================

    def download_product_images(
        self,
        output_folder="images",
        logger=None,
        products=None
    ):
        """
        Downloads product images.

        Parameters
        ----------
        output_folder : str
            Destination folder for downloaded images.

        logger : callable, optional
            Function used for progress logging.

        products : list, optional
            Products to download. Uses all loaded products
            when omitted.
        """

        selected_products = self._resolve_products(
            products
        )

        return download_images(
            selected_products,
            output_folder=output_folder,
            logger=logger
        )

    def download_images(
        self,
        output_folder="images",
        logger=None,
        products=None
    ):
        """
        Compatibility alias used by the current GUI.
        """

        return self.download_product_images(
            output_folder=output_folder,
            logger=logger,
            products=products
        )

    # ==========================================================
    # Generate CSV — All Products
    # ==========================================================

    def generate_csv(
        self,
        filename,
        encoding="utf-8-sig",
        logger=None,
        products=None
    ):
        """
        Generates a CSV from all loaded products unless a
        specific product list is supplied.
        """

        selected_products = self._resolve_products(
            products
        )

        return generate_csv(
            products=selected_products,
            filename=filename,
            encoding=encoding,
            logger=logger
        )

    # ==========================================================
    # Export Selected Products
    # ==========================================================

    def export_selected_products(
        self,
        selected_products,
        filename,
        encoding="utf-8-sig",
        logger=None
    ):
        """
        Exports only the selected products to a Shopify CSV.
        """

        if not selected_products:

            raise ValueError(
                "No products selected."
            )

        return generate_csv(
            products=selected_products,
            filename=filename,
            encoding=encoding,
            logger=logger
        )

    # ==========================================================
    # CSV Validation
    # ==========================================================

    def validate_csv(
        self,
        filename,
        encoding="utf-8-sig",
        logger=None
    ):
        """
        Validates the supplied Shopify CSV file.
        """

        return validate_csv(
            filename=filename,
            encoding=encoding,
            logger=logger
        )

    # ==========================================================
    # Internal Helpers
    # ==========================================================

    def _resolve_products(self, products=None):
        """
        Returns the supplied products or the controller's
        currently loaded product collection.
        """

        if products is None:

            products = self.products

        if not products:

            raise ValueError(
                "No products available. Fetch products first."
            )

        return products