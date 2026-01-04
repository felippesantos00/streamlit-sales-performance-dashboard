import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# Page config
# =====================================================
st.set_page_config(
    page_title="Sales Performance Dashboard",
    layout="wide"
)

# =====================================================
# Sidebar - Navigation
# =====================================================
st.sidebar.title("📊 Navegação")
page = st.sidebar.radio(
    "Selecione a página:",
    ["Dashboard", "Sobre o Projeto"]
)

# =====================================================
# Upload
# =====================================================
st.sidebar.markdown("### 📂 Upload de Dados")
uploaded_file = st.sidebar.file_uploader(
    "Envie um arquivo Excel ou CSV",
    type=["xlsx", "csv"]
)

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Padronização
    df.columns = df.columns.str.lower()

    # Conversão de data
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        df["month"] = df["date"].dt.to_period("M").astype(str)

# =====================================================
# DASHBOARD
# =====================================================
if page == "Dashboard":

    st.title("📈 Sales Performance Dashboard")

    if not uploaded_file:
        st.warning("Faça o upload de um arquivo Excel ou CSV para iniciar.")
        st.stop()

    # =========================
    # Filters
    # =========================
    col1, col2 = st.columns(2)

    with col1:
        region_filter = st.multiselect(
            "Selecione a Região:",
            options=df["region"].unique(),
            default=df["region"].unique()
        )

    with col2:
        rep_filter = st.multiselect(
            "Selecione o Vendedor:",
            options=df["sales_rep"].unique(),
            default=df["sales_rep"].unique()
        )

    filtered_df = df[
        (df["region"].isin(region_filter)) &
        (df["sales_rep"].isin(rep_filter))
    ]

    # =========================
    # KPIs
    # =========================
    total_sales = filtered_df["sales"].sum()
    total_target = filtered_df["target"].sum()
    achievement = (total_sales / total_target) * 100 if total_target > 0 else 0

    k1, k2, k3 = st.columns(3)

    k1.metric("💰 Total Sales", f"{total_sales:,.0f}")
    k2.metric("🎯 Total Target", f"{total_target:,.0f}")
    k3.metric("📊 Achievement", f"{achievement:.2f}%")

    # =========================
    # Sales by Rep
    # =========================
    st.markdown("### 🧑‍💼 Performance por Vendedor")

    rep_perf = (
        filtered_df
        .groupby("sales_rep", as_index=False)
        .agg({"sales": "sum"})
        .sort_values("sales")
    )

    fig_rep = px.bar(
        rep_perf,
        x="sales",
        y="sales_rep",
        orientation="h",
        title="Total Sales por Vendedor"
    )

    st.plotly_chart(fig_rep, use_container_width=True)

    # =========================
    # Sales by Region
    # =========================
    st.markdown("### 🌍 Contribuição por Região")

    region_perf = (
        filtered_df
        .groupby("region", as_index=False)
        .agg({"sales": "sum"})
    )

    fig_region = px.pie(
        region_perf,
        values="sales",
        names="region",
        title="Participação por Região"
    )

    st.plotly_chart(fig_region, use_container_width=True)

    # =========================
    # Real vs Target por Mês
    # =========================
    st.markdown("### 📆 Real vs Target por Mês")

    monthly_perf = (
        filtered_df
        .groupby("month", as_index=False)
        .agg({
            "sales": "sum",
            "target": "sum"
        })
    )

    fig_month = px.line(
        monthly_perf,
        x="month",
        y=["sales", "target"],
        markers=True,
        title="Comparação Mensal: Real vs Target"
    )

    st.plotly_chart(fig_month, use_container_width=True)

    # =========================
    # INSIGHTS AUTOMÁTICOS
    # =========================
    st.markdown("### 🧠 Insights Automáticos")

    best_rep = rep_perf.iloc[-1]["sales_rep"]
    worst_rep = rep_perf.iloc[0]["sales_rep"]

    best_month = monthly_perf.loc[
        monthly_perf["sales"].idxmax(), "month"
    ]

    worst_month = monthly_perf.loc[
        monthly_perf["sales"].idxmin(), "month"
    ]

    gap = total_target - total_sales

    st.info(
        f"""
        🔹 **Top Performer:** {best_rep} lidera em vendas totais.  
        🔹 **Atenção:** {worst_rep} apresenta o menor desempenho e pode se beneficiar de coaching.  
        🔹 **Melhor mês:** {best_month} teve o maior volume de vendas.  
        🔹 **Pior mês:** {worst_month} indica uma possível queda de performance.  
        🔹 **Gap para o Target:** faltam {gap:,.0f} em vendas para atingir a meta total.
        """
    )

# =====================================================
# SOBRE O PROJETO
# =====================================================
else:
    st.title("📘 Sobre o Projeto")

    st.markdown("""
### Project Overview

Este projeto consiste no desenvolvimento de um **Dashboard Interativo de Performance de Vendas**, utilizando **Streamlit**, com foco em **usuários não técnicos**.

O dashboard permite acompanhar o desempenho de vendas por região, vendedor e período, comparando resultados reais com metas estabelecidas.

---

### Key Objectives

• Centralizar a visualização da performance de vendas  
• Identificar vendedores e regiões com melhor e pior desempenho  
• Acompanhar metas e tendências ao longo do tempo  
• Facilitar análises rápidas e autônomas para stakeholders  

---

### Key Features

**Interactive Filtering**
• Filtros dinâmicos por região e vendedor  

**Visual Analytics**
• Gráficos de barras, pizza e linhas  
• Comparação mensal Real vs Target  

**Automated Insights**
• Geração automática de insights textuais  

**Data Upload**
• Suporte para arquivos Excel (.xlsx) e CSV (.csv)  

---

### Tools & Skills Used

• Python  
• Streamlit  
• Pandas  
• Plotly  
• Data Analysis & Storytelling  

---

### Outcome

O dashboard permite decisões mais rápidas, identifica oportunidades de melhoria e oferece uma visão clara e acionável da performance comercial.
""")
