# src/main.py
import logging
import sys
from transform import load_sales_data, transform_sales_data, save_outputs
from fetch_dummyjson import fetch_products, fetch_carts, save_json
from prepare_api_data import load_json, prepare_products, prepare_cart_items, save_outputs as save_api_outputs
from load_to_bq import load_dataframes_to_bq, _load_dotenv_from_file

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

        # --- Sales CSV pipeline ---
        file_path = "data/raw/ecommerce_sales.csv"
        df = load_sales_data(file_path)
        logging.info(f"Loaded raw sales data: {df.shape[0]} rows, {df.shape[1]} columns")

        cleaned_df, overall_summary, category_summary, flagged_products = transform_sales_data(df)
        logging.info("Sales transformation completed")
        logging.info(f"Cleaned rows: {cleaned_df.shape[0]}")
        logging.info(f"Low margin flagged rows: {flagged_products.shape[0]}")

        save_outputs(cleaned_df, overall_summary, category_summary, flagged_products)
        logging.info("Sales output files saved")

        # --- DummyJSON API pipeline ---
        logging.info("Fetching DummyJSON snapshots")
        products_data = fetch_products(limit=50)
        carts_data = fetch_carts(limit=20)

        save_json(products_data, "dummy_products.json")
        save_json(carts_data, "dummy_carts.json")
        logging.info("DummyJSON snapshots saved")

        SNAPSHOT_DIR = Path("data/snapshots")
        products_json = load_json(SNAPSHOT_DIR / "dummy_products.json")
        carts_json    = load_json(SNAPSHOT_DIR / "dummy_carts.json")

        products_df   = prepare_products(products_json)
        cart_items_df = prepare_cart_items(carts_json)
        logging.info(f"API products prepared: {len(products_df)} rows")
        logging.info(f"API cart items prepared: {len(cart_items_df)} rows")

        save_api_outputs(products_df, cart_items_df)
        logging.info("API processed CSVs saved")

        # --- Load to BigQuery ---
        logging.info("Loading processed data to BigQuery")
        _load_dotenv_from_file()
        load_dataframes_to_bq({"api_products": products_df,
                               "api_cart_items": cart_items_df,
                               "metrics_summary_overall": overall_summary,
                               "metrics_summary_by_category": category_summary})
        logging.info("All tables loaded to BigQuery")
        
    except Exception as e:
        logging.exception(f"Pipeline failed: {e}")
        raise

if __name__ == "__main__":
    main()
