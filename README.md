# Shopify VA Toolkit

A Python desktop application designed to streamline common Shopify Virtual Assistant tasks.

## Features

- Retrieve product data from a Shopify store (authorized stores only)
- Download product images
- Generate Shopify-compatible CSV files
- Validate Shopify import CSV files
- Desktop interface built with Tkinter

## Technologies

- Python
- Requests
- Pandas
- Tkinter

## Project Structure

```
Shopify VA Toolkit/

config.py
main.py
gui.py

shopify/
    product_fetcher.py
    image_downloader.py
    csv_generator.py
    validator.py

utils/

images/
output/
```

## How to Run

Install dependencies:

```bash
pip install pandas requests
```

Run:

```bash
python gui.py
```

## Current Version

Version 1.0 (In Progress)

## Roadmap

- Logging system
- Statistics dashboard
- Settings window
- Executable (.exe)
- Portfolio documentation

## Author

Ruth Bringas