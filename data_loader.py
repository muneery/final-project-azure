import pandas as pd
import os

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

        # CLEAN column names HARD
        households.columns = households.columns.str.strip().str.lower().str.replace(" ", "_")
        transactions.columns = transactions.columns.str.strip().str.lower().str.replace(" ", "_")
        products.columns = products.columns.str.strip().str.lower().str.replace(" ", "_")

        # PRINT TO DEBUG (important)
        print("Transactions:", transactions.columns.tolist())
        print("Products:", products.columns.tolist())
        print("Households:", households.columns.tolist())

        # FIX known bad names manually
        transactions.rename(columns={
            'product_num': 'product_num',
            'hshd_num': 'hshd_num'
        }, inplace=True)

        # MERGE
        df = transactions.merge(products, on="product_num", how="left")
        df = df.merge(households, on="hshd_num", how="left")

        return df

    except Exception as e:
        print("ERROR:", str(e))
        return None
