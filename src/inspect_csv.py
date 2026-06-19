import pandas as pd

file_path = "data/raw/ecommerce_sales.csv"

df = pd.read_csv(file_path)

print("Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nDtypes:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nFirst 5 rows:")
print(df.head())


print("\nUnique values in 'Category':")
print(df['category'].unique())

print("\nValue counts for 'Category':")
print(df['category'].value_counts())

print("\nUnique values in 'returned':")
print(df['returned'].unique())

print("\nValue counts for 'returned':")
print(df['returned'].value_counts())

print("\nValue of the 'profit margin' \':")
print(df['profit_margin'].head())

print("\nValue of the 'order date' \':")
print(df['order_date'].head())
