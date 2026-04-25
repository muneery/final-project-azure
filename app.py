from flask import Flask
from data_loader import load_data

app = Flask(__name__)

@app.route("/")
def home():
    df = load_data()

    if df is None:
        return "Error loading data"

    return f"""
    <h1>Retail Dashboard</h1>
    <p>Total rows: {len(df)}</p>
    """

if __name__ == "__main__":
    app.run()
