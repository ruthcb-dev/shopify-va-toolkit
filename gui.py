from shopify.app_state import AppState

import tkinter as tk
from tkinter import ttk, messagebox
import threading

from shopify.product_fetcher import get_products
from shopify.image_downloader import download_images
from shopify.csv_generator import generate_csv
from shopify.validator import validate_csv


# -----------------------------
# Global Variables
# -----------------------------
state = AppState()
# -----------------------------
# Logging
# -----------------------------

def log(message):
    log_box.insert(tk.END, message + "\n")
    log_box.see(tk.END)
    root.update_idletasks()


# -----------------------------
# Fetch Products
# -----------------------------

def fetch_products():

    def run():

        global products

        try:

            progress["value"] = 0

            log("Connecting to Shopify...")

            state.products = get_products()

            progress["value"] = 20

            log(f"✓ Found {len(state.products)} products")

            for row in product_table.get_children():
                product_table.delete(row)

            for product in state.products:
                price = ""

                if product.get("variants"):
                    price = product["variants"][0].get("price", "")

                product_table.insert(
                    "",
                    "end",
                    values=(
                        product["id"],
                        product["title"],
                        f"£{price}"
                    )
                )

            download_button.config(state="normal")
            export_button.config(state="normal")

        except Exception as e:

            messagebox.showerror("Error", str(e))

    threading.Thread(target=run).start()


# -----------------------------
# Download Images
# -----------------------------

def download_product_images():

    def run():

        try:

            log("Downloading images...")

            download_images(state.products)

            progress["value"] = 55

            log("✓ Images downloaded")

            csv_button.config(state="normal")

        except Exception as e:

            messagebox.showerror("Error", str(e))

    threading.Thread(target=run).start()


# -----------------------------
# Generate CSV
# -----------------------------

def generate_shopify_csv():

    def run():

        try:

            log("Generating Shopify CSV...")

            generate_csv(state.products)

            progress["value"] = 80

            log("✓ CSV generated")

            validate_button.config(state="normal")

        except Exception as e:

            messagebox.showerror("Error", str(e))

    threading.Thread(target=run).start()

def export_selected_products():

    selected_items = product_table.selection()

    if not selected_items:
        messagebox.showwarning(
            "No Selection",
            "Please select one or more products."
        )
        return

    selected_products = []

    for item in selected_items:

        product_id = product_table.item(item)["values"][0]

        for product in state.products:

            if product["id"] == product_id:
                selected_products.append(product)
                break

    generate_csv(selected_products)

    messagebox.showinfo(
        "Finished",
        f"Exported {len(selected_products)} selected products."
    )

# -----------------------------
# Validate CSV
# -----------------------------

def validate_shopify_csv():

    def run():

        try:

            log("Validating CSV...")

            validate_csv("output/shopify_import.csv")

            progress["value"] = 100

            log("✓ Validation complete")

            messagebox.showinfo(
                "Finished",
                "Shopify VA Toolkit completed successfully!"
            )

        except Exception as e:

            messagebox.showerror("Error", str(e))

    threading.Thread(target=run).start()


# -----------------------------
# Main Window
# -----------------------------

root = tk.Tk()

root.title("Shopify VA Toolkit")

root.geometry("900x650")


title = ttk.Label(
    root,
    text="Shopify VA Toolkit",
    font=("Segoe UI", 18, "bold")
)

title.pack(pady=10)


progress = ttk.Progressbar(
    root,
    length=600,
    mode="determinate"
)

progress.pack(pady=10)


# -----------------------------
# Buttons
# -----------------------------

button_frame = ttk.Frame(root)

button_frame.pack(pady=10)


fetch_button = ttk.Button(
    button_frame,
    text="1. Fetch Products",
    command=fetch_products
)

fetch_button.grid(row=0, column=0, padx=5)


download_button = ttk.Button(
    button_frame,
    text="2. Download Images",
    command=download_product_images,
    state="disabled"
)

download_button.grid(row=0, column=1, padx=5)


csv_button = ttk.Button(
    button_frame,
    text="3. Generate CSV",
    command=generate_shopify_csv,
    state="disabled"
)

csv_button.grid(row=0, column=2, padx=5)


validate_button = ttk.Button(
    button_frame,
    text="4. Validate CSV",
    command=validate_shopify_csv,
    state="disabled"
)

validate_button.grid(row=0, column=3, padx=5)

export_button = ttk.Button(
    button_frame,
    text="5. Export Selected",
    command=export_selected_products,
    state="disabled"
)

export_button.grid(row=0, column=4, padx=5)

# -----------------------------
# Product Preview
# -----------------------------

preview_label = ttk.Label(
    root,
    text="Product Preview",
    font=("Segoe UI", 11, "bold")
)

preview_label.pack(pady=(15, 5))


columns = ("ID", "Product", "Price")

product_table = ttk.Treeview(
    root,
    columns=columns,
    show="headings",
    height=10,
    selectmode="extended"
)

product_table.heading("ID", text="ID")
product_table.heading("Product", text="Product")
product_table.heading("Price", text="Price")

# Hidden Product ID
product_table.column("ID", width=0, stretch=False)

product_table.column("Product", width=560)

product_table.column("Price", width=100, anchor="center")

product_table.pack(pady=5)


# -----------------------------
# Activity Log
# -----------------------------

log_label = ttk.Label(
    root,
    text="Activity Log",
    font=("Segoe UI", 11, "bold")
)

log_label.pack(pady=(15, 5))


log_box = tk.Text(
    root,
    width=100,
    height=10
)

log_box.pack(pady=5)


root.mainloop()