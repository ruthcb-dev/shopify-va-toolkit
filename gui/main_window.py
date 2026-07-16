import tkinter as tk
from tkinter import ttk

from controllers.app_controller import AppController

from gui.toolbar import Toolbar
from gui.product_panel import ProductPanel
from gui.details_panel import DetailsPanel
from gui.log_panel import LogPanel
from gui.status_bar import StatusBar


class MainWindow:
    """
    Main application window.
    """

    def __init__(self):

        self.root = tk.Tk()

        self.root.title("Shopify VA Toolkit v2.0")

        self.root.geometry("1200x750")

        self.root.minsize(1000, 650)

        # ===== Application State =====

        self.selected_product = None

        self.controller = AppController()

        self.create_layout()

        self.status_bar.set_status("Application started")

        self.log_panel.write("Shopify VA Toolkit started.")

        self.log_panel.write("Ready.")

    def create_layout(self):

        # ===== Toolbar =====

        self.toolbar_frame = ttk.Frame(
            self.root,
            padding=10
        )

        self.toolbar_frame.pack(
            fill="x"
        )

        # ===== Main Content =====

        self.content_frame = ttk.Frame(
            self.root,
            padding=10
        )

        self.content_frame.pack(
            fill="both",
            expand=True
        )

        # ===== Left Panel =====

        self.left_panel = ttk.Frame(
            self.content_frame,
            relief="solid",
            borderwidth=1
        )

        self.left_panel.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 5)
        )

        # ===== Right Panel =====

        self.right_panel = ttk.Frame(
            self.content_frame,
            relief="solid",
            borderwidth=1
        )

        self.right_panel.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(5, 0)
        )

        # ===== Activity Log =====

        self.log_frame = ttk.Frame(
            self.root,
            padding=10
        )

        self.log_frame.pack(
            fill="both"
        )

        # ===== Status Bar =====

        self.status_frame = ttk.Frame(
            self.root,
            relief="sunken",
            padding=5
        )

        self.status_frame.pack(
            fill="x"
        )

        # ===== Components =====

        self.toolbar = Toolbar(
            parent=self.toolbar_frame,
            on_fetch=self.on_fetch_products,
            on_download=self.on_download_images,
            on_csv=self.on_generate_csv,
            on_validate=self.on_validate_csv,
            on_export=self.on_export_selected
        )

        self.product_panel = ProductPanel(
            parent=self.left_panel,
            on_product_selected=self.on_product_selected
        )

        self.details_panel = DetailsPanel(
            self.right_panel
        )

        self.log_panel = LogPanel(
            self.log_frame
        )

        self.status_bar = StatusBar(
            self.status_frame
        )

    def run(self):

        self.root.mainloop()

    # ==========================================================
    # Toolbar Callbacks
    # ==========================================================

    def on_fetch_products(self):

        self.status_bar.set_status(
            "Fetching products..."
        )

        self.log_panel.write(
            "Connecting to Shopify..."
        )

        self.details_panel.clear()

        try:

            products = self.controller.fetch_products()

            self.product_panel.load_products(
                products
            )

            self.log_panel.write(
                f"Loaded {len(products)} products."
            )

            self.status_bar.set_status(
                f"{len(products)} products loaded"
            )

        except Exception as e:

            self.log_panel.write(
                f"ERROR: {e}"
            )

            self.status_bar.set_status(
                "Error"
            )

    def on_download_images(self):

        self.log_panel.write(
            "Download Images clicked."
        )

        self.status_bar.set_status(
            "Downloading images..."
        )

    def on_generate_csv(self):

        self.log_panel.write(
            "Generate CSV clicked."
        )

        self.status_bar.set_status(
            "Generating CSV..."
        )

    def on_validate_csv(self):

        self.log_panel.write(
            "Validate CSV clicked."
        )

        self.status_bar.set_status(
            "Validating CSV..."
        )

    def on_export_selected(self):

        self.log_panel.write(
            "Export Selected clicked."
        )

        self.status_bar.set_status(
            "Exporting selected products..."
        )

    # ==========================================================
    # Product Callbacks
    # ==========================================================

    def on_product_selected(self, product):

        self.selected_product = product

        self.log_panel.write(
            f"Selected: {product.get('title', '-')}"
        )

        self.status_bar.set_status(
            "Product selected"
        )

        self.details_panel.show_product(
            product
        )