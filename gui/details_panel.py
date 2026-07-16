from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO


class DetailsPanel:
    """
    Displays information about the selected Shopify product.
    """

    def __init__(self, parent):

        self.frame = ttk.Frame(parent)

        self.frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.current_image = None

        self.create_widgets()

    def create_widgets(self):

        ttk.Label(
            self.frame,
            text="Product Details",
            font=("Segoe UI", 11, "bold")
        ).pack(
            anchor="w",
            pady=(0, 10)
        )

        # ===== Product Image =====

        image_frame = ttk.Frame(self.frame)

        image_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        self.image_label = ttk.Label(
            image_frame,
            text="[ No Image ]",
            relief="solid",
            anchor="center",
            width=35
        )

        self.image_label.pack()

        # ===== Product Information =====

        fields = [
            "Title",
            "Vendor",
            "Product Type",
            "SKU",
            "Price",
            "Status",
            "Inventory",
            "Tags"
        ]

        self.labels = {}

        for field in fields:

            row = ttk.Frame(self.frame)

            row.pack(
                fill="x",
                pady=3
            )

            ttk.Label(
                row,
                text=f"{field}:",
                width=15,
                anchor="w"
            ).pack(
                side="left"
            )

            value = ttk.Label(
                row,
                text="-",
                wraplength=300,
                justify="left"
            )

            value.pack(
                side="left",
                fill="x",
                expand=True
            )

            self.labels[field] = value

    def clear(self):
        """
        Clears the Details Panel.
        """

        self.image_label.config(
            image="",
            text="[ No Image ]"
        )

        self.current_image = None

        for label in self.labels.values():

            label.config(text="-")

    def load_image(self, image_url):
        """
        Downloads and displays the product image.
        """

        if not image_url:

            self.image_label.config(
                image="",
                text="[ No Image ]"
            )

            self.current_image = None

            return

        try:

            response = requests.get(image_url, timeout=10)

            response.raise_for_status()

            image = Image.open(BytesIO(response.content))

            image.thumbnail((250, 250))

            self.current_image = ImageTk.PhotoImage(image)

            self.image_label.config(
                image=self.current_image,
                text=""
            )

        except Exception:

            self.image_label.config(
                image="",
                text="[ Image Error ]"
            )

            self.current_image = None

    def show_product(self, product):
        """
        Displays information about the selected product.
        """

        variants = product.get("variants", [])

        variant = variants[0] if variants else {}

        self.labels["Title"].config(
            text=product.get("title", "-")
        )

        self.labels["Vendor"].config(
            text=product.get("vendor", "-")
        )

        self.labels["Product Type"].config(
            text=product.get("product_type", "-")
        )

        self.labels["SKU"].config(
            text=variant.get("sku", "-")
        )

        self.labels["Price"].config(
            text=variant.get("price", "-")
        )

        self.labels["Status"].config(
            text="Published"
            if product.get("published_at")
            else "Draft"
        )

        self.labels["Inventory"].config(
            text=str(
                variant.get("inventory_quantity", "N/A")
            )
        )

        tags = product.get("tags", [])

        if isinstance(tags, list):

            tags = ", ".join(tags)

        self.labels["Tags"].config(
            text=tags or "-"
        )

        # ===== Load Product Image =====

        images = product.get("images", [])

        image_url = images[0].get("src") if images else None

        self.load_image(image_url)