import requests
from config import STORE_URL, PRODUCT_LIMIT, HEADERS


def get_products():
    url = f"{STORE_URL}/products.json?limit={PRODUCT_LIMIT}"

    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}")

    return response.json()["products"]