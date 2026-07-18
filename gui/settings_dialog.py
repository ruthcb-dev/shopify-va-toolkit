import tkinter as tk
from tkinter import ttk, filedialog, messagebox


class SettingsDialog:
    """
    Modal dialog for editing application settings.

    Settings are returned to MainWindow through the on_save callback.
    Permanent storage will be added in Phase 7.4.
    """

    def __init__(
        self,
        parent,
        settings=None,
        on_save=None
    ):

        self.parent = parent
        self.on_save = on_save
        self.settings = settings or {}

        self.window = tk.Toplevel(parent)

        self.window.title("Settings")
        self.window.geometry("600x560")
        self.window.minsize(560, 520)
        self.window.resizable(True, True)

        self.window.transient(parent)
        self.window.grab_set()

        self.center_window()

        self.create_variables()
        self.create_layout()

        self.window.protocol(
            "WM_DELETE_WINDOW",
            self.close
        )

        self.window.focus_set()

    # ==========================================================
    # Window Position
    # ==========================================================

    def center_window(self):

        self.window.update_idletasks()

        width = self.window.winfo_width()
        height = self.window.winfo_height()

        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()

        x_position = (
            parent_x
            + (parent_width // 2)
            - (width // 2)
        )

        y_position = (
            parent_y
            + (parent_height // 2)
            - (height // 2)
        )

        self.window.geometry(
            f"+{x_position}+{y_position}"
        )

    # ==========================================================
    # Variables
    # ==========================================================

    def create_variables(self):

        self.store_url_var = tk.StringVar(
            value=self.settings.get(
                "store_url",
                ""
            )
        )

        self.output_folder_var = tk.StringVar(
            value=self.settings.get(
                "output_folder",
                "output"
            )
        )

        self.image_folder_var = tk.StringVar(
            value=self.settings.get(
                "image_folder",
                "images"
            )
        )

        self.csv_encoding_var = tk.StringVar(
            value=self.settings.get(
                "csv_encoding",
                "utf-8-sig"
            )
        )

        self.open_output_var = tk.BooleanVar(
            value=self.settings.get(
                "open_output_after_export",
                False
            )
        )

        self.confirm_exit_var = tk.BooleanVar(
            value=self.settings.get(
                "confirm_exit",
                True
            )
        )

    # ==========================================================
    # Layout
    # ==========================================================

    def create_layout(self):

        self.window.grid_rowconfigure(
            0,
            weight=1
        )

        self.window.grid_columnconfigure(
            0,
            weight=1
        )

        main_frame = ttk.Frame(
            self.window,
            padding=20
        )

        main_frame.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        main_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.create_store_section(main_frame)
        self.create_folder_section(main_frame)
        self.create_export_section(main_frame)
        self.create_application_section(main_frame)
        self.create_buttons(main_frame)

    # ==========================================================
    # Shopify Store Section
    # ==========================================================

    def create_store_section(self, parent):

        store_frame = ttk.LabelFrame(
            parent,
            text="Shopify Store",
            padding=12
        )

        store_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            pady=(0, 12)
        )

        store_frame.grid_columnconfigure(
            1,
            weight=1
        )

        ttk.Label(
            store_frame,
            text="Store URL:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 10)
        )

        ttk.Entry(
            store_frame,
            textvariable=self.store_url_var
        ).grid(
            row=0,
            column=1,
            sticky="ew"
        )

        ttk.Label(
            store_frame,
            text="Example: https://example-store.com",
            foreground="gray"
        ).grid(
            row=1,
            column=1,
            sticky="w",
            pady=(5, 0)
        )

    # ==========================================================
    # Folder Section
    # ==========================================================

    def create_folder_section(self, parent):

        folder_frame = ttk.LabelFrame(
            parent,
            text="Folders",
            padding=12
        )

        folder_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            pady=(0, 12)
        )

        folder_frame.grid_columnconfigure(
            1,
            weight=1
        )

        ttk.Label(
            folder_frame,
            text="CSV output:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 10),
            pady=(0, 8)
        )

        ttk.Entry(
            folder_frame,
            textvariable=self.output_folder_var
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            pady=(0, 8)
        )

        ttk.Button(
            folder_frame,
            text="Browse...",
            command=self.browse_output_folder
        ).grid(
            row=0,
            column=2,
            padx=(8, 0),
            pady=(0, 8)
        )

        ttk.Label(
            folder_frame,
            text="Product images:"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=(0, 10)
        )

        ttk.Entry(
            folder_frame,
            textvariable=self.image_folder_var
        ).grid(
            row=1,
            column=1,
            sticky="ew"
        )

        ttk.Button(
            folder_frame,
            text="Browse...",
            command=self.browse_image_folder
        ).grid(
            row=1,
            column=2,
            padx=(8, 0)
        )

    # ==========================================================
    # Export Section
    # ==========================================================

    def create_export_section(self, parent):

        export_frame = ttk.LabelFrame(
            parent,
            text="CSV Export",
            padding=12
        )

        export_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(0, 12)
        )

        export_frame.grid_columnconfigure(
            1,
            weight=1
        )

        ttk.Label(
            export_frame,
            text="Encoding:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 10)
        )

        encoding_box = ttk.Combobox(
            export_frame,
            textvariable=self.csv_encoding_var,
            state="readonly",
            values=(
                "utf-8-sig",
                "utf-8",
                "cp1252"
            )
        )

        encoding_box.grid(
            row=0,
            column=1,
            sticky="ew"
        )

        ttk.Checkbutton(
            export_frame,
            text="Open output folder after exporting",
            variable=self.open_output_var
        ).grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(10, 0)
        )

    # ==========================================================
    # Application Section
    # ==========================================================

    def create_application_section(self, parent):

        application_frame = ttk.LabelFrame(
            parent,
            text="Application",
            padding=12
        )

        application_frame.grid(
            row=3,
            column=0,
            sticky="ew",
            pady=(0, 16)
        )

        ttk.Checkbutton(
            application_frame,
            text="Ask for confirmation before exiting",
            variable=self.confirm_exit_var
        ).grid(
            row=0,
            column=0,
            sticky="w"
        )

    # ==========================================================
    # Buttons
    # ==========================================================

    def create_buttons(self, parent):

        button_frame = ttk.Frame(parent)

        button_frame.grid(
            row=4,
            column=0,
            sticky="e"
        )

        ttk.Button(
            button_frame,
            text="Cancel",
            command=self.close
        ).grid(
            row=0,
            column=0,
            padx=(0, 8)
        )

        ttk.Button(
            button_frame,
            text="Save Settings",
            command=self.save
        ).grid(
            row=0,
            column=1
        )

    # ==========================================================
    # Folder Browsers
    # ==========================================================

    def browse_output_folder(self):

        folder = filedialog.askdirectory(
            parent=self.window,
            title="Select CSV Output Folder",
            initialdir=self.output_folder_var.get() or "."
        )

        if folder:

            self.output_folder_var.set(folder)

    def browse_image_folder(self):

        folder = filedialog.askdirectory(
            parent=self.window,
            title="Select Product Image Folder",
            initialdir=self.image_folder_var.get() or "."
        )

        if folder:

            self.image_folder_var.set(folder)

    # ==========================================================
    # Validation
    # ==========================================================

    def validate_settings(self):

        store_url = self.store_url_var.get().strip()

        if store_url and not store_url.startswith(
            ("http://", "https://")
        ):

            messagebox.showwarning(
                title="Invalid Store URL",
                message=(
                    "The Shopify store URL must begin with "
                    "http:// or https://."
                ),
                parent=self.window
            )

            return False

        if not self.output_folder_var.get().strip():

            messagebox.showwarning(
                title="Missing Output Folder",
                message="Please select a CSV output folder.",
                parent=self.window
            )

            return False

        if not self.image_folder_var.get().strip():

            messagebox.showwarning(
                title="Missing Image Folder",
                message="Please select a product image folder.",
                parent=self.window
            )

            return False

        return True

    # ==========================================================
    # Save
    # ==========================================================

    def save(self):

        if not self.validate_settings():

            return

        updated_settings = {
            "store_url": self.store_url_var.get().strip(),
            "output_folder": self.output_folder_var.get().strip(),
            "image_folder": self.image_folder_var.get().strip(),
            "csv_encoding": self.csv_encoding_var.get(),
            "open_output_after_export": self.open_output_var.get(),
            "confirm_exit": self.confirm_exit_var.get()
        }

        if self.on_save:

            self.on_save(updated_settings)

        self.close()

    # ==========================================================
    # Close
    # ==========================================================

    def close(self):

        self.window.grab_release()
        self.window.destroy()