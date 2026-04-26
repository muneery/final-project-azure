📊 Retail Analytics Dashboard
Introduction to Cloud Computing — CS 5165 / 6065

Authors:
Muneer Al-Khasawneh
Muhanad Al-Khasawneh

Final Group Project: Data Science and Analytics Using Azure Cloud Computing Technologies

🔗 Live Application

https://retail-dashboard-alkhasme.azurewebsites.net

📌 Overview

This project is a cloud-based retail analytics dashboard deployed on Microsoft Azure. It enables users to explore customer purchasing behavior, analyze retail trends, and generate insights using data processing and machine learning techniques.

🚀 Features
🔐 User Authentication
Secure login with username, password, and email
📈 Interactive Dashboard
Displays key performance indicators:
Total Sales
Average Spend
Total Units
Total Transactions
🔍 Search Functionality
Filter and analyze data by Household ID (HSHD_NUM)
📊 Data Visualizations (Chart.js)
Sales by Department
Sales Over Time
Sales by Region
🧠 Machine Learning (Random Forest)
Classifies high vs low spenders
Demonstrates predictive analytics
🛒 Basket Analysis
Identifies commonly purchased product pairs
Supports cross-selling strategies
⚠️ Churn Prediction
Detects customers with below-average spending
Highlights potential disengagement risk
🗄️ Data Source

The dataset consists of:

Transactions
Households
Products

Data is managed using CSV-based ingestion within an Azure-hosted environment, allowing efficient and low-cost processing.

🧪 Technologies Used
Python (Flask)
Pandas
Scikit-learn (Random Forest)
Chart.js
Microsoft Azure Web App Services
⚙️ How to Run Locally
git clone <your-repo-link>
cd project-folder

pip install -r requirements.txt

python app.py

Open in browser:

http://127.0.0.1:5000
📌 Key Insights
Certain product combinations frequently occur together, enabling cross-selling opportunities
Customer spending varies by region and over time
Machine learning helps identify high-value customers
Low-spending customers may indicate churn risk
👥 Team — Group 24
Muneer Al-Khasawneh
(Add teammates here)
🎯 Project Objective

The goal of this project is to demonstrate how cloud computing and machine learning can be integrated to generate meaningful retail insights and support data-driven decision-making.

✅ Status

✔ Fully Deployed on Azure
✔ Functional Web Application
✔ Meets Course Requirements
