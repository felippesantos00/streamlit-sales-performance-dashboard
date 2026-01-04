import streamlit as st

st.set_page_config(
    page_title="Project Overview – Sales Dashboard",
    layout="wide"
)

st.title("📊 Interactive Sales Performance Dashboard")
st.caption("Project Overview")

st.divider()

# =========================
# PROJECT OVERVIEW
# =========================
st.header("🧠 Project Overview")

st.markdown(
    """
Designed and developed an **interactive Sales Performance Dashboard** using **Streamlit**, inspired by a Microsoft Excel-based solution, to help business stakeholders monitor regional and individual sales performance, track target achievement, and identify improvement opportunities through **clear, actionable visual insights**.

The dashboard is built for **non-technical users**, enabling **quick and independent analysis** without the need for complex tools or technical expertise.
"""
)

# =========================
# KEY OBJECTIVES
# =========================
st.header("🎯 Key Objectives")

st.markdown(
    """
- Provide a **centralized view** of sales performance across multiple regions  
- Identify **top-performing and underperforming sales representatives**  
- Track **target achievement** and **performance trends over time**  
- Enable **easy, self-service analysis** for business stakeholders  
"""
)

# =========================
# KEY FEATURES
# =========================
st.header("⚙️ Key Features")

st.subheader("🔎 Interactive Regional Filtering")
st.markdown(
    """
- Dynamic filters to analyze sales performance across cities such as:
  **Chennai, Delhi, Mumbai, Pune, and Surat**
- Multi-select filters for **regions and sales representatives**
"""
)

st.subheader("📈 KPI & Performance Visuals")
st.markdown(
    """
- **Horizontal bar charts** for performance comparison between sales representatives  
- **Pie charts** for contribution analysis by individual and by region  
- **Line charts** to track sales trends over time  
- Key KPIs:
  - Total Sales  
  - Target Achievement (%)  
  - Top Performing Sales Representative  
"""
)

st.subheader("🧩 User-Friendly Dashboard Design")
st.markdown(
    """
- Clean and intuitive layout optimized for **fast interpretation**
- Designed specifically for **non-technical users**
- No configuration or coding required to explore insights
"""
)

# =========================
# BUSINESS INSIGHTS
# =========================
st.header("💡 Business Insights Delivered")

st.markdown(
    """
- Identified **consistent top performers** based on total sales  
- Highlighted **gaps in target achievement**, supporting coaching and improvement initiatives  
- Revealed **regional performance patterns** to guide strategic resource allocation  
- Supported **data-driven decision-making** through clear visual storytelling  
"""
)

# =========================
# TOOLS & SKILLS
# =========================
st.header("🛠️ Tools & Skills Used")

st.markdown(
    """
- **Python**
- **Streamlit**
- **Pandas**
- **Plotly**
- Data Cleaning & Structuring  
- KPI Analysis  
- Data Visualization  
- Business Storytelling  
"""
)

# =========================
# FOOTER
# =========================
st.divider()

st.markdown(
    """
### 🙋 About the Author
**Felippe Santos**  

- 🔗 LinkedIn: https://www.linkedin.com/in/felippe-santos-54058111a/  
- ✍️ Medium: https://medium.com/@felipperodrigues00  
"""
)
