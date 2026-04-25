from flask import Flask, render_template, request
from data_loader import load_data

app = Flask(__name__)

df = load_data()

@app.route("/")
def home():
    return "Retail Dashboard Running"

@app.route("/search", methods=["GET", "POST"])
def search():
    results = None

    if request.method == "POST":
        hshd = request.form.get("hshd")
        results = df[df["Hshd_num"] == int(hshd)].sort_values(
            by=["Hshd_num", "Basket_num", "Date", "Product_num"]
        )

        results = results.head(50).to_html()

    return f"""
    <h1>Search Household</h1>
    <form method="POST">
        <input name="hshd" placeholder="Enter Hshd_num">
        <button type="submit">Search</button>
    </form>
    <div>{results if results else ""}</div>
    """

if __name__ == "__main__":
    app.run()
