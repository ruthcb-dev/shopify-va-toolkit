import os
import subprocess
import sys
import threading
import tkinter as tk

from pathlib import Path
from tkinter import messagebox, ttk

from app_config.config_manager import ConfigManager
from controllers.app_controller import AppController

from gui.details_panel import DetailsPanel
from gui.log_panel import LogPanel
from gui.menu_bar import MenuBar
from gui.product_panel import ProductPanel
from gui.settings_dialog import SettingsDialog
from gui.status_bar import StatusBar
from gui.toolbar import Toolbar


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

        self.root.grid_rowconfigure(
            0,
            weight=0
        )

        self.root.grid_rowconfigure(
            1,
            weight=1
        )

        self.root.grid_rowconfigure(
            2,
            weight=0
        )

        self.root.grid_rowconfigure(
            3,
            weight=0
        )

        self.root.grid_columnconfigure(
            0,
            weight=1
        )

        self.selected_product = None

        # ==========================================================
        # Configuration
        # ==========================================================

        self.config_manager = ConfigManager()

        self.settings = (
            self.config_manager.load_settings()
        )

        self.ensure_settings_folders()

        # ==========================================================
        # Controller
        # ==========================================================

        self.controller = AppController()

        # ==========================================================
        # Interface
        # ==========================================================

        self.create_layout()
        self.create_menu_bar()

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.on_exit
        )

        self.status_bar.set_status(
            "Application started"
        )

        self.log_panel.write(
            "Shopify VA Toolkit started."
        )

        self.log_panel.write(
            "Settings loaded."
        )

        self.log_panel.write(
            "Ready."
        )

    # ==========================================================
    # Layout
    # ==========================================================

    def create_layout(self):

        # ==========================================================
        # Toolbar
        # ==========================================================

        self.toolbar_frame = ttk.Frame(
            self.root,
            padding=10
        )

        self.toolbar_frame.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        # ==========================================================
        # Main Content
        # ==========================================================

        self.content_frame = ttk.Frame(
            self.root,
            padding=10
        )

        self.content_frame.grid(
            row=1,
            column=0,
            sticky="nsew"
        )

        self.content_frame.grid_rowconfigure(
            0,
            weight=1
        )

        self.content_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.content_frame.grid_columnconfigure(
            1,
            weight=1
        )

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

    # ==========================================================
    # Menu Bar
    # ==========================================================

    def create_menu_bar(self):

        self.menu_bar = MenuBar(
            root=self.root,
            on_fetch=self.on_fetch_products,
            on_download=self.on_download_images,
            on_generate_csv=self.on_generate_csv,
            on_validate=self.on_validate_csv,
            on_export=self.on_export_selected,
            on_settings=self.show_settings,
            on_about=self.show_about,
            on_exit=self.on_exit
        )

    # ==========================================================
    # Application
    # ==========================================================

    def run(self):

        self.root.mainloop()

    # ==========================================================
    # Settings
    # ==========================================================

    def show_settings(self):

        SettingsDialog(
            parent=self.root,
            settings=self.settings.copy(),
            on_save=self.apply_settings
        )

    def apply_settings(self, updated_settings):

        try:

            self.settings = (
                self.config_manager.update_settings(
                    updated_settings
                )
            )

            self.ensure_settings_folders()

            self.log_panel.write(
                "Application settings saved."
            )

            self.status_bar.set_status(
                "Settings saved"
            )

        except OSError as error:

            messagebox.showerror(
                title="Settings Error",
                message=(
                    "The settings could not be saved.\n\n"
                    f"{error}"
                ),
                parent=self.root
            )

            self.log_panel.write(
                f"ERROR: Settings could not be saved: {error}"
            )

            self.status_bar.set_status(
                "Settings error"
            )

    def ensure_settings_folders(self):

        folder_keys = (
            "output_folder",
            "image_folder"
        )

        for key in folder_keys:

            folder_value = self.settings.get(
                key,
                ""
            )

            if not folder_value:

                continue

            try:

                Path(folder_value).expanduser().mkdir(
                    parents=True,
                    exist_ok=True
                )

            except OSError:

                # Folder errors are handled later when the folder is used.
                pass

    # ==========================================================
    # Open Folder
    # ==========================================================

    def open_folder(self, folder_path):

        folder = Path(
            folder_path
        ).expanduser()

        if not folder.exists():

            folder.mkdir(
                parents=True,
                exist_ok=True
            )

        if sys.platform.startswith("win"):

            os.startfile(
                str(folder.resolve())
            )

        elif sys.platform == "darwin":

            subprocess.Popen(
                [
                    "open",
                    str(folder.resolve())
                ]
            )

        else:

            subprocess.Popen(
                [
                    "xdg-open",
                    str(folder.resolve())
                ]
            )

    def open_export_location(self, filename):

        if not self.settings.get(
            "open_output_after_export",
            False
        ):

            return

        if filename:

            export_folder = (
                Path(filename)
                .expanduser()
                .resolve()
                .parent
            )

        else:

            export_folder = self.settings.get(
                "output_folder",
                "output"
            )

        try:

            self.open_folder(
                export_folder
            )

            self.log_panel.write(
                f"Opened output folder: {export_folder}"
            )

        except (
            OSError,
            subprocess.SubprocessError
        ) as error:

            self.log_panel.write(
                f"ERROR: Could not open output folder: {error}"
            )

            self.status_bar.set_status(
                "Could not open output folder"
            )

    # ==========================================================
    # Exit Application
    # ==========================================================

    def on_exit(self):

        confirm_exit = self.settings.get(
            "confirm_exit",
            True
        )

        if confirm_exit:

            should_exit = messagebox.askyesno(
                title="Exit Application",
                message=(
                    "Are you sure you want to exit "
                    "Shopify VA Toolkit?"
                ),
                parent=self.root
            )

            if not should_exit:

                return

        self.root.destroy()

    # ==========================================================
    # About Dialog
    # ==========================================================

    def show_about(self):

        messagebox.showinfo(
            title="About Shopify VA Toolkit",
            message=(
                "Shopify VA Toolkit v2.0\n\n"
                "A desktop productivity tool for "
                "Shopify virtual assistants.\n\n"
                "Features:\n"
                "• Fetch Shopify products\n"
                "• Download product images\n"
                "• Generate Shopify-compatible CSV files\n"
                "• Validate CSV files\n"
                "• Export selected products\n"
                "• Persistent application settings\n\n"
                "Built with Python and Tkinter."
            ),
            parent=self.root
        )

    # ==========================================================
    # Fetch Products
    # ==========================================================

    def on_fetch_products(self):

        threading.Thread(
            target=self.fetch_products_worker,
            daemon=True
        ).start()

    def fetch_products_worker(self):

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
            self.details_panel.clear
        )

        self.root.after(
            0,
            lambda: self.status_bar.set_status(
                "Fetching products..."
            )
        )

        self.root.after(
            0,
            lambda: self.log_panel.write(
                "Connecting to Shopify..."
            )
        )

        try:

            products = (
                self.controller.fetch_products()
            )

            self.root.after(
                0,
                lambda: self.product_panel.load_products(
                    products
                )
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

        except Exception as error:

            error_message = str(error)

            self.root.after(
                0,
                lambda message=error_message:
                self.log_panel.write(
                    f"ERROR: {message}"
                )
            )

            self.root.after(
                0,
                lambda: self.status_bar.set_status(
                    "Error"
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
    # Download Images
    # ==========================================================

    def on_download_images(self):

        threading.Thread(
            target=self.download_images_worker,
            daemon=True
        ).start()

    def download_images_worker(self):

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
                "Downloading images..."
            )
        )

        self.root.after(
            0,
            lambda: self.log_panel.write(
                "Starting image download..."
            )
        )

        try:

            image_folder = self.settings.get(
                "image_folder",
                "images"
            )

            downloaded_count = (
                self.controller.download_images(
                    output_folder=image_folder,
                    logger=lambda message:
                    self.root.after(
                        0,
                        lambda log_message=message:
                        self.log_panel.write(
                            log_message
                        )
                    )
                )
            )

            self.root.after(
                0,
                lambda: self.log_panel.write(
                    f"Downloaded {downloaded_count} images."
                )
            )

            self.root.after(
                0,
                lambda: self.status_bar.set_status(
                    f"{downloaded_count} images downloaded"
                )
            )

        except Exception as error:

            error_message = str(error)

            self.root.after(
                0,
                lambda message=error_message:
                self.log_panel.write(
                    f"ERROR: {message}"
                )
            )

            self.root.after(
                0,
                lambda: self.status_bar.set_status(
                    "Image download failed"
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
    # Generate CSV
    # ==========================================================

    def on_generate_csv(self):

        threading.Thread(
            target=self.generate_csv_worker,
            daemon=True
        ).start()

    def generate_csv_worker(self):

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
                "Generating CSV..."
            )
        )

        self.root.after(
            0,
            lambda: self.log_panel.write(
                "Generating Shopify CSV..."
            )
        )

        try:

            output_folder = self.settings.get(
                "output_folder",
                "output"
            )

            csv_encoding = self.settings.get(
                "csv_encoding",
                "utf-8-sig"
            )

            filename = (
                self.controller.generate_csv(
                    output_folder=output_folder,
                    encoding=csv_encoding,
                    logger=lambda message:
                    self.root.after(
                        0,
                        lambda log_message=message:
                        self.log_panel.write(
                            log_message
                        )
                    )
                )
            )

            if filename:

                self.root.after(
                    0,
                    lambda: self.log_panel.write(
                        f"CSV generation completed.\n{filename}"
                    )
                )

                self.root.after(
                    0,
                    lambda: self.status_bar.set_status(
                        "CSV generated"
                    )
                )

                self.root.after(
                    0,
                    lambda export_file=filename:
                    self.open_export_location(
                        export_file
                    )
                )

            else:

                self.root.after(
                    0,
                    lambda: self.status_bar.set_status(
                        "Ready"
                    )
                )

        except Exception as error:

            error_message = str(error)

            self.root.after(
                0,
                lambda message=error_message:
                self.log_panel.write(
                    f"ERROR: {message}"
                )
            )

            self.root.after(
                0,
                lambda: self.status_bar.set_status(
                    "CSV generation failed"
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
            lambda: self.status_bar.set_status(
                "Validating CSV..."
            )
        )

        self.root.after(
            0,
            lambda: self.log_panel.write(
                "Validating Shopify CSV..."
            )
        )

        try:

            validation_result = (
                self.controller.validate_csv(
                    logger=lambda message:
                    self.root.after(
                        0,
                        lambda log_message=message:
                        self.log_panel.write(
                            log_message
                        )
                    )
                )
            )

            if validation_result:

                self.root.after(
                    0,
                    lambda: self.status_bar.set_status(
                        "CSV validation completed"
                    )
                )

            else:

                self.root.after(
                    0,
                    lambda: self.status_bar.set_status(
                        "Ready"
                    )
                )

        except Exception as error:

            error_message = str(error)

            self.root.after(
                0,
                lambda message=error_message:
                self.log_panel.write(
                    f"ERROR: {message}"
                )
            )

            self.root.after(
                0,
                lambda: self.status_bar.set_status(
                    "CSV validation failed"
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
    # Export Selected Products
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

        self.root.after(
            0,
            lambda: self.log_panel.write(
                "Preparing selected products for export..."
            )
        )

        try:

            selected_products = (
                self.product_panel.get_selected_products()
            )

            if not selected_products:

                raise ValueError(
                    "Please select one or more products first."
                )

            output_folder = self.settings.get(
                "output_folder",
                "output"
            )

            csv_encoding = self.settings.get(
                "csv_encoding",
                "utf-8-sig"
            )

            filename = (
                self.controller.export_selected_products(
                    selected_products=selected_products,
                    output_folder=output_folder,
                    encoding=csv_encoding,
                    logger=lambda message:
                    self.root.after(
                        0,
                        lambda log_message=message:
                        self.log_panel.write(
                            log_message
                        )
                    )
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
                        "Selected products exported"
                    )
                )

                self.root.after(
                    0,
                    lambda export_file=filename:
                    self.open_export_location(
                        export_file
                    )
                )

            else:

                self.root.after(
                    0,
                    lambda: self.status_bar.set_status(
                        "Ready"
                    )
                )

        except Exception as error:

            error_message = str(error)

            self.root.after(
                0,
                lambda message=error_message:
                self.log_panel.write(
                    f"ERROR: {message}"
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

        product_title = product.get(
            "title",
            "Untitled Product"
        )

        self.log_panel.write(
            f"Selected product: {product_title}"
        )

        self.status_bar.set_status(
            "Product selected"
        )

        self.details_panel.show_product(
            product
        )