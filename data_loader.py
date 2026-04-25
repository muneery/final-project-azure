import pandas as pd

def load_data():
    households = pd.read_csv("400_households.csv")
    transactions = pd.read_csv("400_transactions.csv")
    products = pd.read_csv("400_products.csv")

    # merge tables
    df = transactions.merge(households, on="Hshd_num")
    df = df.merge(products, on="Product_num")

    return df
