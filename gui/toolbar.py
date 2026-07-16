from tkinter import ttk


class Toolbar:
    """
    Top toolbar containing the main workflow buttons.
    """

    def __init__(
        self,
        parent,
        on_fetch=None,
        on_download=None,
        on_csv=None,
        on_validate=None,
        on_export=None
    ):

        self.frame = ttk.Frame(parent)

        self.frame.pack(fill="x")

        self.create_widgets(
            on_fetch,
            on_download,
            on_csv,
            on_validate,
            on_export
        )

    def create_widgets(
        self,
        on_fetch,
        on_download,
        on_csv,
        on_validate,
        on_export
    ):

        self.fetch_button = ttk.Button(
            self.frame,
            text="Fetch Products",
            command=on_fetch
        )

        self.fetch_button.pack(
            side="left",
            padx=5,
            pady=5
        )

        self.download_button = ttk.Button(
            self.frame,
            text="Download Images",
            command=on_download
        )

        self.download_button.pack(
            side="left",
            padx=5,
            pady=5
        )

        self.csv_button = ttk.Button(
            self.frame,
            text="Generate CSV",
            command=on_csv
        )

        self.csv_button.pack(
            side="left",
            padx=5,
            pady=5
        )

        self.validate_button = ttk.Button(
            self.frame,
            text="Validate CSV",
            command=on_validate
        )

        self.validate_button.pack(
            side="left",
            padx=5,
            pady=5
        )

        self.export_button = ttk.Button(
            self.frame,
            text="Export Selected",
            command=on_export
        )

        self.export_button.pack(
            side="left",
            padx=5,
            pady=5
        )