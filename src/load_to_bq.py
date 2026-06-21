# src/load_to_bq.py
import os
import logging
from pathlib import Path
import pandas as pd
import pandas_gbq


def _load_dotenv_from_file(dotenv_path: str = ".env"):
    path = Path(dotenv_path)
    if not path.exists():
        return

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")

            if key and key not in os.environ:
                os.environ[key] = value


_load_dotenv_from_file()

PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
DATASET = os.environ.get("BQ_DATASET")

if not PROJECT_ID or not DATASET:
    raise ValueError("GCP_PROJECT_ID and BQ_DATASET environment variables must be set")

def load_dataframes_to_bq(tables: dict[str, pd.DataFrame]):
    """
    tables: {"table_name": dataframe, ...}
    Replaces the table on each run (v1).
    Credentials: set GOOGLE_APPLICATION_CREDENTIALS env var to service account JSON path.
    """
    for table_name, df in tables.items():
        if df is None or df.empty:
            logging.warning(f"Skipping empty DataFrame for table: {table_name}")
            continue
        destination = f"{DATASET}.{table_name}"
        pandas_gbq.to_gbq(
            df,
            destination_table=destination,
            project_id=PROJECT_ID,
            if_exists="replace",
            progress_bar=False
        )
        logging.info(f"Loaded {len(df)} rows into BigQuery: {destination}")