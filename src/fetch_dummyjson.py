import json
from pathlib import Path
import requests

SNAPSHOT_DIR = Path("data/snapshots")
SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

def fetch_products(limit=50):
    url = f"https://dummyjson.com/products?limit={limit}"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()

def fetch_carts(limit=20):
    url = f"https://dummyjson.com/carts?limit={limit}"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()

def save_json(data, file_name):
    output_path = SNAPSHOT_DIR / file_name
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def main():
    products_data = fetch_products(limit=50)
    carts_data = fetch_carts(limit=20)

    save_json(products_data, "dummy_products.json")
    save_json(carts_data, "dummy_carts.json")

    print("Saved product and cart snapshots successfully.")
    print(f"Products count: {len(products_data.get('products', []))}")
    print(f"Carts count: {len(carts_data.get('carts', []))}")

if __name__ == "__main__":
    main()