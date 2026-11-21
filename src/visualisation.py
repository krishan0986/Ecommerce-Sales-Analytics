
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ======================================
# 1. PROJECT CONFIGURATION
# ======================================

print("\n========== DATA VISUALIZATION ==========")

os.makedirs("screenshots", exist_ok=True)

sns.set_theme(style="whitegrid")

# Load cleaned dataset
df = pd.read_csv(
    "data/cleaned_online_retail.csv",
    low_memory=False
)
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# ======================================
# 2. MONTHLY REVENUE TREND
# ======================================

df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)

monthly_sales = (
    df.groupby("Month")["Revenue"]
    .sum()
    .reset_index()
)

plt.figure(figsize=(12, 6))

sns.lineplot(
    data=monthly_sales,
    x="Month",
    y="Revenue",
    marker="o"
)

plt.title("Monthly E-Commerce Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (£)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("screenshots/monthly_revenue.png")
plt.close()

# ======================================
# 3. TOP 10 PRODUCTS
# ======================================

top_products = (
    df.groupby("Description")["Revenue"]
    .sum()
    .nlargest(10)
    .sort_values()
    .reset_index()
)

plt.figure(figsize=(12, 7))

sns.barplot(
    data=top_products,
    x="Revenue",
    y="Description"
)

plt.title("Top 10 Products by Revenue")
plt.xlabel("Revenue (£)")
plt.ylabel("Product")

plt.tight_layout()

plt.savefig("screenshots/top_products.png")
plt.close()

# ======================================
# 4. COUNTRY-WISE SALES
# ======================================

country_sales = (
    df.groupby("Country")["Revenue"]
    .sum()
    .nlargest(10)
    .sort_values()
    .reset_index()
)

plt.figure(figsize=(12, 7))

sns.barplot(
    data=country_sales,
    x="Revenue",
    y="Country"
)

plt.title("Top 10 Countries by Revenue")
plt.xlabel("Revenue (£)")
plt.ylabel("Country")

plt.tight_layout()

plt.savefig("screenshots/country_sales.png")
plt.close()

# ======================================
# 5. DAILY REVENUE DISTRIBUTION
# ======================================

df["Date"] = df["InvoiceDate"].dt.date

daily_sales = df.groupby("Date")["Revenue"].sum()

plt.figure(figsize=(12, 6))

sns.histplot(
    daily_sales,
    bins=30,
    kde=True
)

plt.title("Daily Revenue Distribution")
plt.xlabel("Daily Revenue (£)")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig("screenshots/daily_revenue.png")
plt.close()

# ======================================
# 6. FINAL REPORT
# ======================================

print("\nAll visualizations created successfully!")

print("\nGenerated Charts:")

print("1. Monthly Revenue Trend")
print("2. Top 10 Products")
print("3. Top 10 Countries")
print("4. Daily Revenue Distribution")

print("\nCharts saved in screenshots folder.")

print("\n========== VISUALIZATION COMPLETED ==========")
