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
st.caption("Upload an Excel or CSV file to analyze sales performance")

# =====================
# FILE UPLOAD
# =====================
uploaded_file = st.file_uploader(
    "📥 Upload your sales file",
    type=["xlsx", "csv"]
)

if not uploaded_file:
    st.info("Please upload a CSV or Excel file to start the analysis.")
    st.stop()

# =====================
# LOAD DATA
# =====================


@st.cache_data
def load_file(file):
    if file.name.endswith(".csv"):
        try:
            return pd.read_csv(file)
        except UnicodeDecodeError:
            return pd.read_csv(file, encoding="latin1")
    else:
        return pd.read_excel(file)


df = load_file(uploaded_file)

# =====================
# VALIDATION
# =====================
required_columns = {
    "Date", "Region", "City", "Sales_Rep", "Sales", "Target"
}

missing = required_columns - set(df.columns)

if missing:
    st.error(
        f"The uploaded file is missing the following columns:\n"
        f"{', '.join(missing)}"
    )
    st.stop()

# =====================
# DATA PREP
# =====================
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Date"])

# =====================
# SIDEBAR FILTERS
# =====================
st.sidebar.header("🔍 Filters")

regions = st.sidebar.multiselect(
    "Region",
    options=sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

sales_reps = st.sidebar.multiselect(
    "Sales Representative",
    options=sorted(df["Sales_Rep"].unique()),
    default=sorted(df["Sales_Rep"].unique())
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
    .sort_values(ascending=False)
    .index[0]
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
    filtered_df.groupby("Sales_Rep", as_index=False)["Sales"]
    .sum()
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
# SALES TREND
# =====================
trend_df = (
    filtered_df
    .groupby(["Date", "Region"], as_index=False)["Sales"]
    .sum()
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
