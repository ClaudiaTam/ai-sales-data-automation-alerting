# src/transform.py
import pandas as pd

def load_sales_data(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df = df.rename(columns=lambda x: x.strip().lower().replace(' ', '_'))
    df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce')

    cols_to_numeric = [
        'price', 'discount', 'quantity', 'delivery_time_days',
        'total_amount', 'shipping_cost', 'profit_margin', 'customer_age'
    ]
    for col in cols_to_numeric:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df

def transform_sales_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df = df.copy()

    df['revenue'] = df['total_amount']
    df['gross_margin'] = df['profit_margin']
    df['estimated_cost'] = df['revenue'] * (1 - df['gross_margin'] / 100)
    df['gross_profit'] = df['revenue'] - df['estimated_cost']
    df['low_margin_flag'] = df['gross_margin'] < 10
    df['source'] = 'csv_kaggle'

    overall_summary = pd.DataFrame({
        'total_orders': [df['order_id'].nunique()],
        'total_revenue': [df['revenue'].sum()],
        'total_gross_profit': [df['gross_profit'].sum()],
        'avg_gross_margin': [df['gross_margin'].mean()],
        'low_margin_orders': [df['low_margin_flag'].sum()],
        'returned_orders': [(df['returned'] == 'Yes').sum()]
    })

    category_summary = df.groupby('category', as_index=False).agg(
        total_orders=('order_id', 'count'),
        total_revenue=('revenue', 'sum'),
        total_gross_profit=('gross_profit', 'sum'),
        avg_gross_margin=('gross_margin', 'mean'),
        low_margin_orders=('low_margin_flag', 'sum')
    )

    flagged_products = df[df['low_margin_flag']].copy()

    return df, overall_summary, category_summary, flagged_products

def save_outputs(
    cleaned_df: pd.DataFrame,
    overall_summary: pd.DataFrame,
    category_summary: pd.DataFrame,
    flagged_products: pd.DataFrame
) -> None:
    cleaned_df.to_csv("data/processed/cleaned_sales.csv", index=False)
    overall_summary.to_csv("data/processed/metrics_summary_overall.csv", index=False)
    category_summary.to_csv("data/processed/metrics_summary_by_category.csv", index=False)
    flagged_products.to_csv("data/processed/flagged_products.csv", index=False)