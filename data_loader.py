import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_data():
    try:
        households = pd.read_csv(
            os.path.join(BASE_DIR, "400_households.csv"),
            skipinitialspace=True
        )

        transactions = pd.read_csv(
            os.path.join(BASE_DIR, "400_transactions.csv"),
            skipinitialspace=True
        )

        products = pd.read_csv(
            os.path.join(BASE_DIR, "400_products.csv"),
            skipinitialspace=True
        )

        # Clean column names
        households.columns = households.columns.str.strip().str.lower().str.replace(" ", "_")
        transactions.columns = transactions.columns.str.strip().str.lower().str.replace(" ", "_")
        products.columns = products.columns.str.strip().str.lower().str.replace(" ", "_")

        # Merge data
        df = transactions.merge(products, on="product_num", how="left")
        df = df.merge(households, on="hshd_num", how="left")

        return df

    except Exception as e:
        return f"ERROR: {str(e)}"
