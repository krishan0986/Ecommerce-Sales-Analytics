
import pandas as pd
import numpy as np

print("\n========== DATA CLEANING STARTED ==========")

# 1. Load original dataset
df = pd.read_excel("data/Online Retail.xlsx")

print("Original Records:", len(df))

# 2. Remove duplicate records
duplicates = df.duplicated().sum()
df = df.drop_duplicates()

print("Duplicates Removed:", duplicates)

# 3. Remove missing product descriptions
missing_descriptions = df["Description"].isnull().sum()
df = df.dropna(subset=["Description"])

print("Missing Descriptions Removed:", missing_descriptions)

# 4. Identify cancelled invoices
df["InvoiceNo"] = df["InvoiceNo"].astype(str).str.strip()

cancelled = df["InvoiceNo"].str.startswith("C")

print("Cancelled Invoice Records:", cancelled.sum())

# 5. Identify return / non-positive quantity records
non_positive_quantity = df["Quantity"] <= 0

print("Non-positive Quantity Records:", non_positive_quantity.sum())

# 6. Identify invalid prices
invalid_prices = df["UnitPrice"] <= 0

print("Non-positive Price Records:", invalid_prices.sum())

# 7. Keep valid sales transactions
clean_df = df[
    (~cancelled) &
    (df["Quantity"] > 0) &
    (df["UnitPrice"] > 0)
].copy()

# 8. Convert invoice date into datetime
clean_df["InvoiceDate"] = pd.to_datetime(
    clean_df["InvoiceDate"],
    errors="coerce"
)

clean_df = clean_df.dropna(subset=["InvoiceDate"])

# 9. Calculate revenue
clean_df["Revenue"] = (
    clean_df["Quantity"] * clean_df["UnitPrice"]
)

# 10. Save cleaned dataset
clean_df.to_csv(
    "data/cleaned_online_retail.csv",
    index=False
)

# 11. Final report
print("\n========== CLEANING REPORT ==========")

print("Original Records:", len(pd.read_excel(
    "data/Online Retail.xlsx",
    usecols=["InvoiceNo"]
)))

print("Cleaned Records:", len(clean_df))

print("Removed Records:", 
      len(df) - len(clean_df))

print("Total Revenue: £",
      round(clean_df["Revenue"].sum(), 2))

print("Average Revenue: £",
      round(clean_df["Revenue"].mean(), 2))

print("Maximum Revenue: £",
      round(clean_df["Revenue"].max(), 2))

print("Minimum Revenue: £",
      round(clean_df["Revenue"].min(), 2))

print("\nCleaned Dataset Saved Successfully!")

print("\n========== DATA CLEANING COMPLETED ==========")
