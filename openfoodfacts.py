import requests


BASE_URL = "https://world.openfoodfacts.org"


def clean_product_data(product, barcode=""):
    return {
        "name": product.get("product_name", "Unknown Product"),
        "brand": product.get("brands", "Unknown Brand"),
        "barcode": barcode or product.get("code", ""),
        "ingredients": product.get("ingredients_text", "No ingredients listed"),
        "categories": product.get("categories", ""),
        "image_url": product.get("image_url", ""),
        "source": "OpenFoodFacts"
    }


def fetch_product_by_barcode(barcode):
    url = f"{BASE_URL}/api/v2/product/{barcode}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()

        if data.get("status") != 1:
            return None

        product = data.get("product", {})
        return clean_product_data(product, barcode)

    except requests.RequestException:
        return None


def search_product_by_name(name):
    url = f"{BASE_URL}/cgi/search.pl"

    params = {
        "search_terms": name,
        "search_simple": 1,
        "action": "process",
        "json": 1,
        "page_size": 1
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        products = data.get("products", [])

        if not products:
            return None

        product = products[0]
        return clean_product_data(product, product.get("code", ""))

    except requests.RequestException:
        return None