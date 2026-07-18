import requests

from config import HEADERS, PRODUCT_LIMIT


def get_products(store_url):
    """
    Fetch products from a Shopify store.

    Parameters
    ----------
    store_url : str
        Shopify store URL, such as:
        https://example-store.com

    Returns
    -------
    list
        Shopify product records.
    """

    store_url = str(store_url or "").strip()

    if not store_url:
        raise ValueError(
            "No Shopify Store URL configured. "
            "Open File > Settings and enter a Store URL."
        )

    if not store_url.startswith(
        ("http://", "https://")
    ):
        raise ValueError(
            "Store URL must begin with http:// or https://."
        )

    store_url = store_url.rstrip("/")

    if store_url.endswith("/products.json"):
        products_url = store_url
    else:
        products_url = f"{store_url}/products.json"

    response = requests.get(
        products_url,
        headers=HEADERS,
        params={
            "limit": PRODUCT_LIMIT
        },
        timeout=30
    )

    try:
        response.raise_for_status()

    except requests.HTTPError as error:
        raise RuntimeError(
            f"Shopify request failed with status "
            f"{response.status_code}."
        ) from error

    try:
        response_data = response.json()

    except requests.JSONDecodeError as error:
        raise RuntimeError(
            "The Shopify store returned an invalid response."
        ) from error

    products = response_data.get(
        "products"
    )

    if products is None:
        raise RuntimeError(
            "The Shopify response does not contain a products list."
        )

    return products