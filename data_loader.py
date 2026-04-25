import pandas as pd

def load_data():
    households = pd.read_csv("400_households.csv")
    transactions = pd.read_csv("400_transactions.csv")
    products = pd.read_csv("400_products.csv")

    # Merge transactions with products
    df = transactions.merge(products, on="product_num", how="left")

    # Merge with households
    df = df.merge(households, on="hshd_num", how="left")

    return df
