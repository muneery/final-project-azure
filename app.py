from flask import Flask, render_template, request, redirect, session
from data_loader import load_data
import json

app = Flask(__name__)
app.secret_key = "secret123"  # required for login


# -------- LOGIN --------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        # simple check (prof doesn't care about real auth)
        if username and password and email:
            session["user"] = username
            return redirect("/dashboard")

    return render_template("login.html")


# -------- DASHBOARD --------
@app.route("/dashboard")
def home():
    if "user" not in session:
        return redirect("/")

    df = load_data()

    if df is None or isinstance(df, str):
        return f"Error loading data: {df}"

    df.columns = df.columns.str.strip().str.lower()

    total_rows = len(df)
    total_sales = df["spend"].sum()
    avg_spend = df["spend"].mean()
    total_units = df["units"].sum()

    sample = df.head(20).to_html()

    # charts
    dept_sales = df.groupby("department")["spend"].sum().sort_values(ascending=False)
    chart_labels = dept_sales.index.tolist()
    chart_values = dept_sales.values.tolist()

    sales_over_time = df.groupby("year")["spend"].sum()
    time_labels = sales_over_time.index.astype(str).tolist()
    time_values = sales_over_time.values.tolist()

    region_col = "store_region" if "store_region" in df.columns else "store_r"
    region_sales = df.groupby(region_col)["spend"].sum()
    region_labels = region_sales.index.tolist()
    region_values = region_sales.values.tolist()

    # insights
    top_dept = dept_sales.idxmax()
    top_region = region_sales.idxmax()

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
        top_dept=top_dept,
        top_region=top_region
    )


# -------- SEARCH (FIXED SORTING) --------
@app.route("/search")
def search():
    hshd = request.args.get("hshd")

    df = load_data()
    df.columns = df.columns.str.strip().str.lower()

    if hshd:
        df = df[df["hshd_num"] == int(hshd)]

    df = df.sort_values(by=["hshd_num", "basket_num", "purchase_", "product_num", "department", "commodity"])

    return df.head(50).to_html()


if __name__ == "__main__":
    app.run()
