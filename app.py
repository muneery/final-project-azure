from flask import Flask, render_template, request
from data_loader import load_data
import json

app = Flask(__name__)

@app.route("/")
def home():
    df = load_data()

    if df is None:
        return "Error loading data"

    # --- CLEAN COLUMN NAMES (IMPORTANT) ---
    df.columns = df.columns.str.strip().str.lower()

    # --- KPIs ---
    total_rows = len(df)
    total_sales = df["spend"].sum()
    avg_spend = df["spend"].mean()
    total_units = df["units"].sum()

    sample = df.head(20).to_html()

    # --- CHART 1: Sales by Department ---
    dept_sales = df.groupby("department")["spend"].sum().sort_values(ascending=False)
    chart_labels = dept_sales.index.tolist()
    chart_values = dept_sales.values.tolist()

    # --- CHART 2: Sales Over Time ---
    if "year" in df.columns:
        sales_over_time = df.groupby("year")["spend"].sum()
        time_labels = sales_over_time.index.astype(str).tolist()
        time_values = sales_over_time.values.tolist()
    else:
        time_labels = []
        time_values = []

    # --- CHART 3: Sales by Region (FIXED) ---
    region_col = "store_region" if "store_region" in df.columns else "store_r"

    if region_col in df.columns:
        region_sales = df.groupby(region_col)["spend"].sum()
        region_labels = region_sales.index.tolist()
        region_values = region_sales.values.tolist()
    else:
        region_labels = []
        region_values = []

    return render_template(
        "index.html",
        total=total_rows,
        sales=round(total_sales, 2),
        avg=round(avg_spend, 2),
        units=int(total_units),
        table=sample,
        labels=json.dumps(chart_labels),
        values=json.dumps(chart_values),

        time_labels=json.dumps(time_labels),
        time_values=json.dumps(time_values),

        region_labels=json.dumps(region_labels),
        region_values=json.dumps(region_values)
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
