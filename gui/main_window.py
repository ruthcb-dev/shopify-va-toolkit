import tkinter as tk
from tkinter import ttk
import threading

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

        # Root Grid

        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=0)
        self.root.grid_rowconfigure(3, weight=0)
        self.root.grid_columnconfigure(0, weight=1)

        self.selected_product = None

        self.controller = AppController()

        self.create_layout()

        self.status_bar.set_status("Application started")

        self.log_panel.write("Shopify VA Toolkit started.")
        self.log_panel.write("Ready.")

    def create_layout(self):

        # ==========================================================
        # Toolbar
        # ==========================================================

        self.toolbar_frame = ttk.Frame(self.root, padding=10)
        self.toolbar_frame.grid(row=0, column=0, sticky="ew")

        # ==========================================================
        # Main Content
        # ==========================================================

        self.content_frame = ttk.Frame(self.root, padding=10)
        self.content_frame.grid(row=1, column=0, sticky="nsew")

        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)

        self.left_panel = ttk.Frame(
            self.content_frame,
            relief="solid",
            borderwidth=1
        )

        self.left_panel.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 5)
        )

        self.right_panel = ttk.Frame(
            self.content_frame,
            relief="solid",
            borderwidth=1
        )

        self.right_panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5, 0)
        )

        # ==========================================================
        # Activity Log
        # ==========================================================

        self.log_frame = ttk.Frame(
            self.root,
            padding=10
        )

        self.log_frame.grid(
            row=2,
            column=0,
            sticky="ew"
        )

        # ==========================================================
        # Status Bar
        # ==========================================================

        self.status_frame = ttk.Frame(
            self.root,
            relief="sunken",
            padding=5
        )

        self.status_frame.grid(
            row=3,
            column=0,
            sticky="ew"
        )

        # ==========================================================
        # Components
        # ==========================================================

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
    # Fetch Products
    # ==========================================================

    def on_fetch_products(self):

        threading.Thread(
            target=self.fetch_products_worker,
            daemon=True
        ).start()

    def fetch_products_worker(self):

        self.root.after(0, lambda: self.toolbar.set_enabled(False))
        self.root.after(0, self.toolbar.start_progress)
        self.root.after(0, self.details_panel.clear)
        self.root.after(0, lambda: self.status_bar.set_status("Fetching products..."))
        self.root.after(0, lambda: self.log_panel.write("Connecting to Shopify..."))

        try:

            products = self.controller.fetch_products()

            self.root.after(
                0,
                lambda: self.product_panel.load_products(products)
            )

            self.root.after(
                0,
                lambda: self.log_panel.write(
                    f"Loaded {len(products)} products."
                )
            )

            self.root.after(
                0,
                lambda: self.status_bar.set_status(
                    f"{len(products)} products loaded"
                )
            )

        except Exception as e:

            self.root.after(
                0,
                lambda: self.log_panel.write(f"ERROR: {e}")
            )

            self.root.after(
                0,
                lambda: self.status_bar.set_status("Error")
            )

        finally:

            self.root.after(
                0,
                self.toolbar.stop_progress
            )

            self.root.after(
                0,
                lambda: self.toolbar.set_enabled(True)
            )

    # ==========================================================
    # Download Images
    # ==========================================================

    def on_download_images(self):

        threading.Thread(
            target=self.download_images_worker,
            daemon=True
        ).start()

    def download_images_worker(self):

        self.root.after(0, lambda: self.toolbar.set_enabled(False))
        self.root.after(0, self.toolbar.start_progress)
        self.root.after(0, lambda: self.status_bar.set_status("Downloading images..."))

        try:

            self.controller.download_product_images(
                logger=lambda msg:
                self.root.after(
                    0,
                    lambda m=msg: self.log_panel.write(m)
                )
            )

            self.root.after(
                0,
                lambda: self.status_bar.set_status("Ready")
            )

        except Exception as e:

            self.root.after(
                0,
                lambda: self.log_panel.write(f"ERROR: {e}")
            )

            self.root.after(
                0,
                lambda: self.status_bar.set_status("Error")
            )

        finally:

            self.root.after(
                0,
                self.toolbar.stop_progress
            )

            self.root.after(
                0,
                lambda: self.toolbar.set_enabled(True)
            )

    # ==========================================================
    # Generate CSV
    # ==========================================================

    def on_generate_csv(self):

        threading.Thread(
            target=self.generate_csv_worker,
            daemon=True
        ).start()

    def generate_csv_worker(self):

        self.root.after(0, lambda: self.toolbar.set_enabled(False))
        self.root.after(0, self.toolbar.start_progress)
        self.root.after(0, lambda: self.status_bar.set_status("Generating CSV..."))

        try:

            filename = self.controller.generate_csv(
                logger=lambda msg:
                self.root.after(
                    0,
                    lambda m=msg: self.log_panel.write(m)
                )
            )

            if filename:

                self.root.after(
                    0,
                    lambda: self.log_panel.write(
                        f"Saved to:\n{filename}"
                    )
                )

                self.root.after(
                    0,
                    lambda: self.status_bar.set_status(
                        "CSV generated"
                    )
                )

            else:

                self.root.after(
                    0,
                    lambda: self.status_bar.set_status("Ready")
                )

        except Exception as e:

            self.root.after(
                0,
                lambda: self.log_panel.write(f"ERROR: {e}")
            )

            self.root.after(
                0,
                lambda: self.status_bar.set_status("Error")
            )

        finally:

            self.root.after(
                0,
                self.toolbar.stop_progress
            )

            self.root.after(
                0,
                lambda: self.toolbar.set_enabled(True)
            )

    # ==========================================================
    # Validate CSV
    # ==========================================================

    def on_validate_csv(self):

        threading.Thread(
            target=self.validate_csv_worker,
            daemon=True
        ).start()

    def validate_csv_worker(self):

        self.root.after(
            0,
            lambda: self.toolbar.set_enabled(False)
        )

        self.root.after(
            0,
            self.toolbar.start_progress
        )

        self.root.after(
            0,
            lambda: self.status_bar.set_status("Validating CSV...")
        )

        try:

            success = self.controller.validate_csv(
                logger=lambda msg:
                self.root.after(
                    0,
                    lambda m=msg: self.log_panel.write(m)
                )
            )

            if success:

                self.root.after(
                    0,
                    lambda: self.status_bar.set_status(
                        "Validation completed"
                    )
                )

            else:

                self.root.after(
                    0,
                    lambda: self.status_bar.set_status(
                        "Ready"
                    )
                )

        except Exception as e:

            self.root.after(
                0,
                lambda: self.log_panel.write(
                    f"ERROR: {e}"
                )
            )

            self.root.after(
                0,
                lambda: self.status_bar.set_status(
                    "Validation failed"
                )
            )

        finally:

            self.root.after(
                0,
                self.toolbar.stop_progress
            )

            self.root.after(
                0,
                lambda: self.toolbar.set_enabled(True)
            )

    
    # ==========================================================
    # Export Selected
    # ==========================================================

    def on_export_selected(self):

        threading.Thread(
            target=self.export_selected_worker,
            daemon=True
        ).start()


    def export_selected_worker(self):

        self.root.after(
            0,
            lambda: self.toolbar.set_enabled(False)
        )

        self.root.after(
            0,
            self.toolbar.start_progress
        )

        self.root.after(
            0,
            lambda: self.status_bar.set_status(
                "Exporting selected products..."
            )
        )

        try:

            selected_products = self.product_panel.get_selected_products()

            if not selected_products:

                raise ValueError(
                    "Please select one or more products first."
                )

            filename = self.controller.export_selected_products(

                selected_products,

                logger=lambda msg:
                self.root.after(
                    0,
                    lambda m=msg: self.log_panel.write(m)
                )
            )

            if filename:

                self.root.after(
                    0,
                    lambda: self.log_panel.write(
                        f"Export completed.\n{filename}"
                    )
                )

                self.root.after(
                    0,
                    lambda: self.status_bar.set_status(
                        "Export completed"
                    )
                )

            else:

                self.root.after(
                    0,
                    lambda: self.status_bar.set_status(
                        "Ready"
                    )
                )

        except Exception as e:

            self.root.after(
                0,
                lambda: self.log_panel.write(
                    f"ERROR: {e}"
                )
            )

            self.root.after(
                0,
                lambda: self.status_bar.set_status(
                    "Export failed"
                )
            )

        finally:

            self.root.after(
                0,
                self.toolbar.stop_progress
            )

            self.root.after(
                0,
                lambda: self.toolbar.set_enabled(True)
            )

    # ==========================================================
    # Product Selection
    # ==========================================================

    def on_product_selected(self, product):

        self.selected_product = product

        self.log_panel.write(
            f"Selected: {product.get('title', '-')}"
        )

        self.status_bar.set_status(
            "Product selected"
        )

        self.details_panel.show_product(product)