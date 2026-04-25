from flask import Flask
from data_loader import load_data

app = Flask(__name__)

@app.route("/")
def home():
    df = load_data()

    if isinstance(df, str):
        return df

    sample = df.head(20).to_html()

    return f"""
    <h1>Retail Dashboard</h1>
    <p>Total rows: {len(df)}</p>
    <h2>Sample Data</h2>
    {sample}
    """

if __name__ == "__main__":
    app.run()
