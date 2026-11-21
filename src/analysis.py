
import pandas as pd
import numpy as np
import os

print("\n========== E-COMMERCE SALES ANALYSIS ==========")

# 1. Load cleaned dataset
df = pd.read_csv("data/cleaned_online_retail.csv")

# 2. Basic business metrics
total_revenue = df["Revenue"].sum()
total_orders = df["InvoiceNo"].nunique()
total_customers = df["CustomerID"].nunique()
total_products = df["StockCode"].nunique()

average_order_value = total_revenue / total_orders

print("\n========== BUSINESS OVERVIEW ==========")
print(f"Total Revenue: £{total_revenue:,.2f}")
print(f"Total Orders: {total_orders:,}")
print(f"Total Customers: {total_customers:,}")
print(f"Unique Products: {total_products:,}")
print(f"Average Order Value: £{average_order_value:,.2f}")

# 3. Top 10 products by revenue
top_products = (
    df.groupby(["StockCode", "Description"])
    .agg(
        Total_Quantity=("Quantity", "sum"),
        Total_Revenue=("Revenue", "sum")
    )
    .sort_values("Total_Revenue", ascending=False)
    .head(10)
)

print("\n========== TOP 10 PRODUCTS BY REVENUE ==========")
print(top_products.to_string())

# 4. Monthly sales trends
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

df["Month"] = df["InvoiceDate"].dt.to_period("M")

monthly_sales = (
    df.groupby("Month")["Revenue"]
    .sum()
    .reset_index()
)

monthly_sales["Month"] = monthly_sales["Month"].astype(str)

monthly_sales["Growth_Percent"] = (
    monthly_sales["Revenue"].pct_change() * 100
)

print("\n========== MONTHLY SALES ==========")
print(monthly_sales.to_string(index=False))

# 5. Country-wise revenue
country_sales = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print("\n========== TOP 10 COUNTRIES ==========")
print(country_sales.to_string())

# 6. Best sales month
best_month = monthly_sales.loc[
    monthly_sales["Revenue"].idxmax()
]

print("\n========== BEST SALES MONTH ==========")
print("Month:", best_month["Month"])
print(f"Revenue: £{best_month['Revenue']:,.2f}")

# 7. Revenue validation
print("\n========== REVENUE VALIDATION ==========")
print("Zero Revenue Rows:", (df["Revenue"] == 0).sum())
print("Negative Revenue Rows:", (df["Revenue"] < 0).sum())

# 8. Save analysis reports
os.makedirs("data/analysis_outputs", exist_ok=True)

top_products.to_csv(
    "data/analysis_outputs/top_products.csv"
)

monthly_sales.to_csv(
    "data/analysis_outputs/monthly_sales.csv",
    index=False
)

country_sales.to_csv(
    "data/analysis_outputs/country_sales.csv"
)

print("\nAnalysis reports saved successfully!")

print("\n========== SALES ANALYSIS COMPLETED ==========")
