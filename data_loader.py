import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_data():
    households = pd.read_csv(os.path.join(BASE_DIR, "400_households.csv"))
    transactions = pd.read_csv(os.path.join(BASE_DIR, "400_transactions.csv"))
    products = pd.read_csv(os.path.join(BASE_DIR, "400_products.csv"))

    # normalize columns
    households.columns = households.columns.str.lower()
    transactions.columns = transactions.columns.str.lower()
    products.columns = products.columns.str.lower()

    # merge
    df = transactions.merge(products, on="product_num", how="left")
    df = df.merge(households, on="hshd_num", how="left")

    return df
