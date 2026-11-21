import streamlit as st
import pandas as pd

# ---------------------------------
# PAGE SETTINGS
# ---------------------------------

st.set_page_config(
    page_title="E-Commerce Sales Analytics",
    page_icon="📊",
    layout="wide"
)

# ---------------------------------
# LOAD DATA
# ---------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv(
        "data/cleaned_online_retail.csv",
        dtype={"InvoiceNo": str}
    )

    # Convert date column
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    return df


df = load_data()

# ---------------------------------
# DASHBOARD TITLE
# ---------------------------------

st.title("📊 E-Commerce Sales Analytics Dashboard")
st.markdown(
    """
    Analyze **sales performance, customer activity, products and geographic trends**
    using real-world e-commerce transaction data.
    """
)

st.divider()


# ---------------------------------
# BASIC DATA INFORMATION
# ---------------------------------
# ---------------------------------
# SIDEBAR FILTER
# ---------------------------------

st.sidebar.title("📊 Sales Analytics")
st.sidebar.write("Filter the dashboard data")
st.sidebar.divider()


st.sidebar.header("🔍 Filters")

country_list = ["All Countries"] + sorted(df["Country"].dropna().unique().tolist())

selected_country = st.sidebar.selectbox(
    "Select Country",
    country_list
)

# Date filter
min_date = df["InvoiceDate"].min().date()
max_date = df["InvoiceDate"].max().date()

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Apply country filter
if selected_country == "All Countries":
    filtered_df = df
else:
    filtered_df = df[df["Country"] == selected_country]


# Apply date filter
if len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = filtered_df[
        (filtered_df["InvoiceDate"].dt.date >= start_date) &
        (filtered_df["InvoiceDate"].dt.date <= end_date)
    ]

# ---------------------------------
# CURRENT FILTER SUMMARY
# ---------------------------------

st.sidebar.divider()
st.sidebar.subheader("📌 Current Selection")

st.sidebar.write(f"📦 Transactions: {len(filtered_df):,}")
st.sidebar.write(f"🌍 Country: {selected_country}")

if len(date_range) == 2:
    st.sidebar.write(f"📅 From: {date_range[0]}")
    st.sidebar.write(f"📅 To: {date_range[1]}")

st.subheader("Dataset Overview")

# Calculate business KPIs
total_revenue = filtered_df["Revenue"].sum()
total_orders = filtered_df["InvoiceNo"].nunique()
total_customers = filtered_df["CustomerID"].nunique()

average_order_value = total_revenue / total_orders if total_orders > 0 else 0
# Display KPI cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Total Revenue",
        f"£{total_revenue:,.2f}"
    )

with col2:
    st.metric(
        "🧾 Total Orders",
        f"{total_orders:,}"
    )

with col3:
    st.metric(
        "👥 Total Customers",
        f"{total_customers:,}"
    )

with col4:
    st.metric(
        "🛒 Avg Order Value",
        f"£{average_order_value:,.2f}"
    )

# ---------------------------------
# DATA PREVIEW
# ---------------------------------
# ---------------------------------
# MONTHLY REVENUE TREND
# ---------------------------------

st.subheader("📈 Monthly Revenue Trend")

monthly_revenue = (
    filtered_df
    .set_index("InvoiceDate")
    .resample("ME")["Revenue"]
    .sum()
    .reset_index()
)

st.line_chart(
    monthly_revenue,
    x="InvoiceDate",
    y="Revenue",
    width="stretch"
)


# ---------------------------------
# TOP 10 PRODUCTS BY REVENUE
# ---------------------------------

st.subheader("🏆 Top 10 Products by Revenue")

top_products = (
    filtered_df
    .groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

st.bar_chart(
    top_products,
    horizontal=True,
    width="stretch"
)

# ---------------------------------
# TOP COUNTRIES BY REVENUE
# ---------------------------------

st.subheader("🌍 Top Countries by Revenue")

country_revenue = (
    filtered_df
    .groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

st.bar_chart(
    country_revenue,
    horizontal=True,
    width="stretch"
)
# ---------------------------------
# TOP 10 CUSTOMERS BY REVENUE
# ---------------------------------

st.subheader("👥 Top 10 Customers by Revenue")

top_customers = (
    filtered_df
    .dropna(subset=["CustomerID"])
    .groupby("CustomerID")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

st.bar_chart(
    top_customers,
    horizontal=True,
    width="stretch"
)

# ---------------------------------
# CUSTOMER BEHAVIOR
# ---------------------------------

st.subheader("🔁 Customer Purchase Behavior")

customer_orders = (
    filtered_df
    .dropna(subset=["CustomerID"])
    .groupby("CustomerID")["InvoiceNo"]
    .nunique()
)

repeat_customers = (customer_orders > 1).sum()
one_time_customers = (customer_orders == 1).sum()

total_identified_customers = len(customer_orders)

if total_identified_customers > 0:
    repeat_rate = (
        repeat_customers / total_identified_customers
    ) * 100
else:
    repeat_rate = 0

customer_col1, customer_col2, customer_col3 = st.columns(3)

with customer_col1:
    st.metric(
        "🔁 Repeat Customers",
        f"{repeat_customers:,}"
    )

with customer_col2:
    st.metric(
        "🧍 One-Time Customers",
        f"{one_time_customers:,}"
    )

with customer_col3:
    st.metric(
        "📈 Repeat Customer Rate",
        f"{repeat_rate:.1f}%"
    )
# ---------------------------------
# DAILY REVENUE TREND
# ---------------------------------

st.subheader("📅 Daily Revenue Trend")

daily_revenue = (
    filtered_df
    .set_index("InvoiceDate")
    .resample("D")["Revenue"]
    .sum()
    .reset_index()
)

st.line_chart(
    daily_revenue,
    x="InvoiceDate",
    y="Revenue",
    width="stretch"
)

# ---------------------------------
# DATA EXPLORER
# ---------------------------------

with st.expander("🔎 View Transaction Data"):

    st.dataframe(
        filtered_df,
        width="stretch"
    )

    csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Data",
    data=csv,
    file_name="filtered_ecommerce_data.csv",
    mime="text/csv"
)