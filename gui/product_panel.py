import tkinter as tk
from tkinter import ttk


class ProductPanel:
    """
    Displays the Shopify product list.
    """

    def __init__(
        self,
        parent,
        on_product_selected=None
    ):

        self.frame = ttk.Frame(parent)

        self.frame.pack(
            fill="both",
            expand=True
        )

        self.products = []

        self.selection_callback = on_product_selected

        self.create_widgets()

    def create_widgets(self):

        # ==========================================================
        # Header
        # ==========================================================

        header_frame = ttk.Frame(self.frame)

        header_frame.pack(
            fill="x",
            padx=10,
            pady=(10, 5)
        )

        ttk.Label(
            header_frame,
            text="Products",
            font=("Segoe UI", 11, "bold")
        ).pack(side="left")

        # ==========================================================
        # Search
        # ==========================================================

        search_frame = ttk.Frame(self.frame)

        search_frame.pack(
            fill="x",
            padx=10,
            pady=(0, 10)
        )

        ttk.Label(
            search_frame,
            text="Search:"
        ).pack(side="left")

        self.search_var = tk.StringVar()

        self.search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            width=35
        )

        self.search_entry.pack(
            side="left",
            padx=5
        )

        self.search_button = ttk.Button(
            search_frame,
            text="Search"
        )

        self.search_button.pack(side="left")

        # ==========================================================
        # Product Table
        # ==========================================================

        columns = (
            "Title",
            "Vendor",
            "Type",
            "Price",
            "SKU"
        )

        self.tree = ttk.Treeview(
            self.frame,
            columns=columns,
            show="headings",
            selectmode="extended"
        )

        for column in columns:

            self.tree.heading(
                column,
                text=column
            )

        self.tree.column("Title", width=280)
        self.tree.column("Vendor", width=120)
        self.tree.column("Type", width=120)
        self.tree.column("Price", width=80, anchor="center")
        self.tree.column("SKU", width=120)

        scrollbar = ttk.Scrollbar(
            self.frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 0),
            pady=(0, 10)
        )

        scrollbar.pack(
            side="right",
            fill="y",
            padx=(0, 10),
            pady=(0, 10)
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.on_select
        )

    def on_select(self, event):

        selection = self.tree.selection()

        if not selection:
            return

        first = self.tree.index(selection[0])

        if first < len(self.products):

            if self.selection_callback:

                self.selection_callback(
                    self.products[first]
                )

    def get_selected_products(self):
        """
        Returns all selected products.
        """

        selected = []

        for item in self.tree.selection():

            index = self.tree.index(item)

            if index < len(self.products):

                selected.append(
                    self.products[index]
                )

        return selected

    def clear(self):

        for item in self.tree.get_children():

            self.tree.delete(item)

    def load_products(self, products):

        self.products = products

        self.clear()

        for product in products:

            variants = product.get("variants", [])

            variant = variants[0] if variants else {}

            self.tree.insert(
                "",
                "end",
                values=(
                    product.get("title", ""),
                    product.get("vendor", ""),
                    product.get("product_type", ""),
                    variant.get("price", ""),
                    variant.get("sku", "")
                )
            )