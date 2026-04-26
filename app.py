from flask import Flask, render_template, request
from data_loader import load_data
import json

app = Flask(__name__)

@app.route("/")
def home():
    df = load_data()

    if df is None:
        return "Error loading data"

    df.columns = df.columns.str.strip().str.lower()

    # 🔥 REQUIRED SORTING
    df = df.sort_values(by=[
        "hshd_num",
        "basket_num",
        "purchase_",
        "product_num",
        "department",
        "commodity"
    ])

    # KPIs
    total_rows = len(df)
    total_sales = df["spend"].sum()
    avg_spend = df["spend"].mean()
    total_units = df["units"].sum()

    sample = df.head(20).to_html()

    # CHART 1
    dept_sales = df.groupby("department")["spend"].sum().sort_values(ascending=False)
    chart_labels = dept_sales.index.tolist()
    chart_values = dept_sales.values.tolist()

    # CHART 2
    sales_over_time = df.groupby("year")["spend"].sum()
    time_labels = sales_over_time.index.astype(str).tolist()
    time_values = sales_over_time.values.tolist()

    # CHART 3
    region_col = "store_region" if "store_region" in df.columns else "store_r"
    region_sales = df.groupby(region_col)["spend"].sum()
    region_labels = region_sales.index.tolist()
    region_values = region_sales.values.tolist()

    # 🔥 INSIGHTS (BIG POINT BOOST)
    top_department = df.groupby("department")["spend"].sum().idxmax()
    top_region = df.groupby(region_col)["spend"].sum().idxmax()

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
        region_values=json.dumps(region_values),

        top_dept=top_department,
        top_region=top_region
    )


@app.route("/search")
def search():
    hshd = request.args.get("hshd")

    df = load_data()

    if df is None:
        return "Error loading data"

    df.columns = df.columns.str.strip().str.lower()

    if hshd:
        df = df[df["hshd_num"] == int(hshd)]

    # 🔥 REQUIRED SORT
    df = df.sort_values(by=[
        "hshd_num",
        "basket_num",
        "purchase_",
        "product_num",
        "department",
        "commodity"
    ])

    table = df.head(100).to_html()

    return render_template(
        "index.html",
        total=len(df),
        sales=round(df["spend"].sum(), 2),
        avg=round(df["spend"].mean(), 2),
        units=int(df["units"].sum()),
        table=table,

        labels="[]",
        values="[]",
        time_labels="[]",
        time_values="[]",
        region_labels="[]",
        region_values="[]",

        top_dept="N/A",
        top_region="N/A"
    )


if __name__ == "__main__":
    app.run()
