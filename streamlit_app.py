import streamlit as st
import pandas as pd
import plotly.express as px

# =====================
# PAGE CONFIG
# =====================
st.set_page_config(
    page_title="Sales Performance Dashboard",
    layout="wide"
)

st.title("📊 Sales Performance Dashboard")
st.caption("Upload an Excel file to analyze sales performance")

# =====================
# FILE UPLOAD
# =====================
uploaded_file = st.file_uploader(
    "📥 Upload your sales Excel file",
    type=["xlsx"]
)

if not uploaded_file:
    st.info("Please upload an Excel file to start the analysis.")
    st.stop()

# =====================
# LOAD DATA
# =====================


@st.cache_data
def load_excel(file):
    return pd.read_excel(file)


df = load_excel(uploaded_file)

# =====================
# VALIDATION
# =====================
required_columns = {
    "Date", "Region", "City", "Sales_Rep", "Sales", "Target"
}

if not required_columns.issubset(df.columns):
    st.error(
        f"Excel file must contain the following columns:\n{', '.join(required_columns)}"
    )
    st.stop()

df["Date"] = pd.to_datetime(df["Date"])

# =====================
# SIDEBAR FILTERS
# =====================
st.sidebar.header("🔍 Filters")

regions = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

sales_reps = st.sidebar.multiselect(
    "Select Sales Representative",
    options=df["Sales_Rep"].unique(),
    default=df["Sales_Rep"].unique()
)

filtered_df = df[
    (df["Region"].isin(regions)) &
    (df["Sales_Rep"].isin(sales_reps))
]

# =====================
# KPIs
# =====================
total_sales = filtered_df["Sales"].sum()
total_target = filtered_df["Target"].sum()
achievement = (total_sales / total_target * 100) if total_target > 0 else 0

top_rep = (
    filtered_df.groupby("Sales_Rep")["Sales"]
    .sum()
    .idxmax()
)

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Sales", f"${total_sales:,.0f}")
col2.metric("🎯 Target Achievement", f"{achievement:.1f}%")
col3.metric("🏆 Top Performer", top_rep)

st.divider()

# =====================
# SALES BY REP
# =====================
rep_sales = (
    filtered_df.groupby("Sales_Rep")["Sales"]
    .sum()
    .reset_index()
    .sort_values("Sales")
)

fig_rep = px.bar(
    rep_sales,
    x="Sales",
    y="Sales_Rep",
    orientation="h",
    title="Sales Performance by Representative"
)

st.plotly_chart(fig_rep, use_container_width=True)

# =====================
# SALES BY REGION
# =====================
fig_region = px.pie(
    filtered_df,
    values="Sales",
    names="Region",
    title="Sales Contribution by Region"
)

st.plotly_chart(fig_region, use_container_width=True)

# =====================
# TREND OVER TIME
# =====================
trend_df = (
    filtered_df
    .groupby(["Date", "Region"])["Sales"]
    .sum()
    .reset_index()
)

fig_trend = px.line(
    trend_df,
    x="Date",
    y="Sales",
    color="Region",
    title="Sales Trend Over Time"
)

st.plotly_chart(fig_trend, use_container_width=True)

# =====================
# FOOTER
# =====================
st.markdown("---")
st.markdown(
    """
    ### 🙋 About the Author
    **Felippe Santos**  
    🔗 [LinkedIn](https://www.linkedin.com/in/felippe-santos-54058111a/)
    """
)
