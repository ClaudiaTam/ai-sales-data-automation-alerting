# src/main.py
import logging
import sys
from transform import load_sales_data, transform_sales_data, save_outputs
from fetch_dummyjson import fetch_products, fetch_carts, save_json
from prepare_api_data import load_json, prepare_products, prepare_cart_items, save_outputs as save_api_outputs

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/pipeline.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def main():
    try:
        logging.info("Pipeline started")

        file_path = "data/raw/ecommerce_sales.csv"
        df = load_sales_data(file_path)
        logging.info(f"Loaded raw data: {df.shape[0]} rows, {df.shape[1]} columns")

        cleaned_df, overall_summary, category_summary, flagged_products = transform_sales_data(df)
        logging.info("Transformation completed")

        save_outputs(cleaned_df, overall_summary, category_summary, flagged_products)
        logging.info("Output files saved successfully")

        logging.info(f"Low margin rows: {flagged_products.shape[0]}")

        products_data = fetch_products(limit=50)
        carts_data = fetch_carts(limit=20)

        save_json(products_data, "dummy_products.json")
        save_json(carts_data, "dummy_carts.json")
        logging.info("DummyJSON snapshots saved successfully")
        logging.info("Pipeline finished successfully")

    except Exception as e:
        logging.exception(f"Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    main()