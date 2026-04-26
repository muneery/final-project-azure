from flask import Flask, render_template, request, redirect, session
from data_loader import load_data
import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)
app.secret_key = "secret123"


# -------- LOGIN --------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

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

    # ---------------- KPIs ----------------
    total_rows = len(df)
    total_sales = df["spend"].sum()
    avg_spend = df["spend"].mean() if len(df) > 0 else 0
    total_units = df["units"].sum()

    sample = df.head(50).to_html()

    # ---------------- CHARTS ----------------
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

    # ---------------- INSIGHTS ----------------
    top_dept = dept_sales.idxmax()
    top_region = region_sales.idxmax()

    # ---------------- STEP 7: BASKET ANALYSIS ----------------
    basket_pairs = (
        df.groupby(["basket_num"])["product_num"]
        .apply(list)
        .tolist()
    )

    pair_counts = {}
    for basket in basket_pairs:
        for i in range(len(basket)):
            for j in range(i + 1, len(basket)):
                pair = tuple(sorted([basket[i], basket[j]]))
                pair_counts[pair] = pair_counts.get(pair, 0) + 1

    top_pairs = sorted(pair_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    # ---------------- STEP 7: SIMPLE ML ----------------
    # Predict high spender (simple classification)
    df["high_spend"] = df["spend"] > df["spend"].mean()

    X = df[["units"]]
    y = df["high_spend"]

    model = RandomForestClassifier()
    model.fit(X, y)

    ml_prediction = model.predict([[2]])[0]  # example prediction

    # ---------------- STEP 8: CHURN ----------------
    customer_spend = df.groupby("hshd_num")["spend"].sum()
    churn_threshold = customer_spend.mean()

    churn_customers = customer_spend[customer_spend < churn_threshold]
    churn_count = len(churn_customers)

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
        top_region=top_region,

        # NEW
        top_pairs=top_pairs,
        ml_prediction=ml_prediction,
        churn_count=churn_count
    )


# -------- LOGOUT --------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# -------- SEARCH --------
@app.route("/search")
def search():
    if "user" not in session:
        return redirect("/")

    hshd = request.args.get("hshd")
    
    if not hshd or not hshd.isdigit():
        return redirect("/dashboard")
    
    df = load_data()
    
    if df is None or isinstance(df, str):
    return f"Error loading data: {df}"
    
    df.columns = df.columns.str.strip().str.lower()

    if hshd:
        df = df[df["hshd_num"] == int(hshd)]

    # KPIs
    total_rows = len(df)
    total_sales = df["spend"].sum()
    avg_spend = df["spend"].mean() if len(df) > 0 else 0
    total_units = df["units"].sum()

    sample = df.head(50).to_html()

    # charts
    dept_sales = df.groupby("department")["spend"].sum()
    chart_labels = dept_sales.index.tolist()
    chart_values = dept_sales.values.tolist()

    sales_over_time = df.groupby("year")["spend"].sum()
    time_labels = sales_over_time.index.astype(str).tolist()
    time_values = sales_over_time.values.tolist()

    region_col = "store_region" if "store_region" in df.columns else "store_r"
    region_sales = df.groupby(region_col)["spend"].sum()
    region_labels = region_sales.index.tolist()
    region_values = region_sales.values.tolist()

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

        top_dept="Filtered",
        top_region="Filtered",
        top_pairs=[],
        ml_prediction="Filtered",
        churn_count=0
    )

if __name__ == "__main__":
    app.run()
