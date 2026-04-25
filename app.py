from flask import Flask
import pandas as pd

app = Flask(__name__)

# Load data safely
def load_data():
    try:
        transactions = pd.read_csv("400_transactions.csv")
        products = pd.read_csv("400_products.csv")
        households = pd.read_csv("400_households.csv")
        return transactions, products, households
    except Exception as e:
        return None, None, str(e)

@app.route("/")
def home():
    transactions, products, households = load_data()

    if transactions is None:
        return f"Error loading data: {households}"

    return f"""
    <h1>Retail Dashboard</h1>
    <p>Transactions rows: {len(transactions)}</p>
    <p>Products rows: {len(products)}</p>
    <p>Households rows: {len(households)}</p>
    """

if __name__ == "__main__":
    app.run()
