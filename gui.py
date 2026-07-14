import tkinter as tk
from tkinter import ttk, messagebox
import threading

from shopify.product_fetcher import get_products
from shopify.image_downloader import download_images
from shopify.csv_generator import generate_csv
from shopify.validator import validate_csv


def log(message):
    log_box.insert(tk.END, message + "\n")
    log_box.see(tk.END)
    root.update_idletasks()


def start_toolkit():

    def run():

        try:

            progress["value"] = 0

            log("Connecting to Shopify...")

            products = get_products()

            progress["value"] = 15

            log(f"✓ Found {len(products)} products")

            log("Downloading images...")

            download_images(products)

            progress["value"] = 55

            log("✓ Images downloaded")

            log("Generating Shopify CSV...")

            generate_csv(products)

            progress["value"] = 80

            log("✓ CSV generated")

            log("Validating CSV...")

            validate_csv("output/shopify_import.csv")

            progress["value"] = 100

            log("✓ Validation complete")

            messagebox.showinfo(
                "Finished",
                "Toolkit completed successfully!"
            )

        except Exception as e:

            messagebox.showerror("Error", str(e))

    threading.Thread(target=run).start()


root = tk.Tk()

root.title("Shopify VA Toolkit")

root.geometry("700x500")

title = ttk.Label(
    root,
    text="Shopify VA Toolkit",
    font=("Segoe UI", 18, "bold")
)

title.pack(pady=15)

progress = ttk.Progressbar(
    root,
    length=500,
    mode="determinate"
)

progress.pack(pady=10)

start_button = ttk.Button(
    root,
    text="Start Toolkit",
    command=start_toolkit
)

start_button.pack(pady=10)

log_box = tk.Text(
    root,
    height=18,
    width=80
)

log_box.pack(pady=10)

root.mainloop()