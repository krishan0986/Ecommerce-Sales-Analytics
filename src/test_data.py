
import pandas as pd
import numpy as np

# ==================================
# 1. LOAD DATASET
# ==================================

print("\n========== E-COMMERCE SALES ANALYSIS ==========")

df = pd.read_excel("data/Online Retail.xlsx")

print("\nDataset Loaded Successfully!")

# ==================================
# 2. DISPLAY FIRST 5 ROWS
# ==================================

print("\n========== FIRST 5 RECORDS ==========")
print(df.head())

# ==================================
# 3. DATASET INFORMATION
# ==================================

print("\n========== DATASET INFORMATION ==========")
print(df.info())

# ==================================
# 4. DATASET SHAPE
# ==================================

print("\n========== DATASET SHAPE ==========")
print("Total Rows:", df.shape[0])
print("Total Columns:", df.shape[1])

# ==================================
# 5. COLUMN NAMES
# ==================================

print("\n========== COLUMN NAMES ==========")
print(df.columns.tolist())

# ==================================
# 6. MISSING VALUES
# ==================================

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())

# ==================================
# 7. DUPLICATE RECORDS
# ==================================

print("\n========== DUPLICATE RECORDS ==========")
print("Duplicates:", df.duplicated().sum())

# ==================================
# 8. BASIC STATISTICS
# ==================================

print("\n========== STATISTICAL SUMMARY ==========")
print(df.describe())

print("\n========== ANALYSIS COMPLETED ==========")
