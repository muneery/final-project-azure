import pandas as pd
import os

def load_data():
    try:
        BASE_DIR = "/home/site/wwwroot"

        households = pd.read_csv(os.path.join(BASE_DIR, "400_households.csv"))
        transactions = pd.read_csv(os.path.join(BASE_DIR, "400_transactions.csv"))
        products = pd.read_csv(os.path.join(BASE_DIR, "400_products.csv"))

        households.columns = households.columns.str.lower()
        transactions.columns = transactions.columns.str.lower()
        products.columns = products.columns.str.lower()

        df = transactions.merge(products, on="product_num", how="left")
        df = df.merge(households, on="hshd_num", how="left")

        return df

    except Exception as e:
        print("ERROR:", e)
        return None
