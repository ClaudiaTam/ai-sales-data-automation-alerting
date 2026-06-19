import json
from pathlib import Path
import pandas as pd

SNAPSHOT_DIR = Path("data/snapshots")
PROCESSED_DIR = Path("data/processed")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def load_json(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def prepare_products(products_json: dict) -> pd.DataFrame:
    products = products_json.get("products", [])

    product_rows = []
    for p in products:
        product_rows.append({
            "api_product_id": p.get("id"),
            "product_title": p.get("title"),
            "category": p.get("category"),
            "brand": p.get("brand"),
            "api_price": p.get("price"),
            "discount_percentage": p.get("discountPercentage"),
            "rating": p.get("rating"),
            "stock": p.get("stock"),
            "availability_status": p.get("availabilityStatus"),
            "shipping_information": p.get("shippingInformation"),
            "return_policy": p.get("returnPolicy"),
            "minimum_order_quantity": p.get("minimumOrderQuantity"),
            "source": "dummyjson_products"
        })

    return pd.DataFrame(product_rows)


def prepare_cart_items(carts_json: dict) -> pd.DataFrame:
    carts = carts_json.get("carts", [])

    cart_item_rows = []
    for cart in carts:
        cart_id = cart.get("id")
        user_id = cart.get("userId")
        cart_total = cart.get("total")
        cart_discounted_total = cart.get("discountedTotal")
        total_products = cart.get("totalProducts")
        total_quantity = cart.get("totalQuantity")

        for item in cart.get("products", []):
            cart_item_rows.append({
                "cart_id": cart_id,
                "user_id": user_id,
                "cart_total": cart_total,
                "cart_discounted_total": cart_discounted_total,
                "cart_total_products": total_products,
                "cart_total_quantity": total_quantity,
                "api_product_id": item.get("id"),
                "product_title": item.get("title"),
                "api_price": item.get("price"),
                "quantity": item.get("quantity"),
                "line_total": item.get("total"),
                "discount_percentage": item.get("discountPercentage"),
                "discounted_total": item.get("discountedTotal"),
                "thumbnail": item.get("thumbnail"),
                "source": "dummyjson_carts"
            })

    return pd.DataFrame(cart_item_rows)


def save_outputs(products_df: pd.DataFrame, cart_items_df: pd.DataFrame):
    products_output = PROCESSED_DIR / "api_products.csv"
    cart_items_output = PROCESSED_DIR / "api_cart_items.csv"

    products_df.to_csv(products_output, index=False)
    cart_items_df.to_csv(cart_items_output, index=False)

    return products_output, cart_items_output


def main():
    products_file = SNAPSHOT_DIR / "dummy_products.json"
    carts_file = SNAPSHOT_DIR / "dummy_carts.json"

    products_json = load_json(products_file)
    carts_json = load_json(carts_file)

    products_df = prepare_products(products_json)
    cart_items_df = prepare_cart_items(carts_json)

    products_output, cart_items_output = save_outputs(products_df, cart_items_df)

    print("API preparation completed.")
    print(f"api_products rows: {len(products_df)}")
    print(f"api_cart_items rows: {len(cart_items_df)}")
    print(f"Saved: {products_output}")
    print(f"Saved: {cart_items_output}")

    print("\nSample api_products:")
    print(products_df.head())

    print("\nSample api_cart_items:")
    print(cart_items_df.head())


if __name__ == "__main__":
    main()