import pandas as pd
import os

def load_data():
    try:
        households = pd.read_csv(os.path.join(BASE_DIR, "400_households.csv"))
        transactions = pd.read_csv(os.path.join(BASE_DIR, "400_transactions.csv"))
        products = pd.read_csv(os.path.join(BASE_DIR, "400_products.csv"))

        # CLEAN column names
        households.columns = households.columns.str.strip().str.lower()
        transactions.columns = transactions.columns.str.strip().str.lower()
        products.columns = products.columns.str.strip().str.lower()

        # DEBUG (you will see this in logs if needed)
        print("Transactions:", transactions.columns)
        print("Products:", products.columns)
        print("Households:", households.columns)

        # FIX BAD COLUMN NAMES (THIS IS IMPORTANT)
        transactions.rename(columns={
            'product_num': 'product_num',
            'hshd_num': 'hshd_num'
        }, inplace=True)

        products.rename(columns={
            'product_num': 'product_num'
        }, inplace=True)

        households.rename(columns={
            'hshd_num': 'hshd_num'
        }, inplace=True)

        # merge safely
        df = transactions.merge(products, on="product_num", how="left")
        df = df.merge(households, on="hshd_num", how="left")

        return df

    except Exception as e:
        print("ERROR:", str(e))
        return None
