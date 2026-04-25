from flask import Flask, render_template, request
from data_loader import load_data
import json

app = Flask(__name__)

@app.route("/")
def home():
    df = load_data()

    if df is None:
        return "Error loading data"

    # --- KPIs ---
    total_rows = len(df)
    total_sales = df["spend"].sum()
    avg_spend = df["spend"].mean()
    total_units = df["units"].sum()

    sample = df.head(20).to_html()

    # --- CHART DATA ---
    dept_sales = df.groupby("department")["spend"].sum().sort_values(ascending=False)

    chart_labels = dept_sales.index.tolist()
    chart_values = dept_sales.values.tolist()

    return render_template(
        "index.html",
        total=total_rows,
        sales=round(total_sales, 2),
        avg=round(avg_spend, 2),
        units=int(total_units),
        table=sample,
        labels=json.dumps(chart_labels),
        values=json.dumps(chart_values)
    )


@app.route("/search")
def search():
    hshd = request.args.get("hshd")

    df = load_data()

    if df is None:
        return "Error loading data"

    if hshd:
        df = df[df["hshd_num"] == int(hshd)]

    return df.head(50).to_html()


if __name__ == "__main__":
    app.run()
