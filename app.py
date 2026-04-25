from flask import Flask
from data_loader import load_data

app = Flask(__name__)

@app.route("/")
def home():
    df = load_data()

    total_sales = df["spend"].sum()
    total_transactions = len(df)

    return f"""
    <h1>Retail Dashboard</h1>
    <p>Total Sales: ${total_sales:,.2f}</p>
    <p>Total Transactions: {total_transactions}</p>
    """

if __name__ == "__main__":
    app.run()
