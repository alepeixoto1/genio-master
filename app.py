import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================

st.set_page_config(
    page_title="Gênio Master",
    page_icon="📊",
    layout="wide"
)

# =====================================
# MENU LATERAL
# =====================================

st.sidebar.title("🏠 Gênio Master")

pagina = st.sidebar.selectbox(
    "Selecione o módulo",
    [
        "📊 Dashboard",
        "💰 Financeiro",
        "📦 Ativos",
        "🌱 ESG",
        "⏱️ SLAs"
    ]
)

# =====================================
# CONEXÃO COM GOOGLE SHEETS
# =====================================

SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"

def carregar(gid):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
    return pd.read_csv(url)

df_financeiro = carregar("0")
df_ativos = carregar("1179272110")
df_esg = carregar("1026863401")
df_slas = carregar("2075740723")

# =====================================
# DASHBOARD
# =====================================

if pagina == "📊 Dashboard":

    st.title("📊 Dashboard Geral")

    total_previsto = df_financeiro["Previsto"].sum()
    total_realizado = df_financeiro["Realizado"].sum()
    total_saving = df_financeiro["Saving"].sum()
    total_ativos = len(df_ativos)

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Previsto", f"R$ {total_previsto:,.2f}")
    col2.metric("Realizado", f"R$ {total_realizado:,.2f}")
    col3.metric("Saving", f"R$ {total_saving:,.2f}")
    col4.metric("Ativos", total_ativos)

    st.divider()

    col1, col2 = st.columns(2)

    fig1 = px.bar(
        df_financeiro,
        x="Mês",
        y=["Previsto", "Realizado"],
        barmode="group",
        title="Financeiro Mensal",
        template="plotly_white"
    )

    col1.plotly_chart(fig1, use_container_width=True)

    fig2 = px.pie(
        df_financeiro,
        names="Categoria",
        values="Realizado",
        title="Distribuição por Categoria",
        hole=0.5
    )

    col2.plotly_chart(fig2, use_container_width=True)

# =====================================
# FINANCEIRO
# =====================================

elif pagina == "💰 Financeiro":

    st.title("💰 Financeiro")

    total_previsto = df_financeiro["Previsto"].sum()
    total_realizado = df_financeiro["Realizado"].sum()
    total_saving = df_financeiro["Saving"].sum()

    col1, col2, col3 = st.columns(3)

    col1.metric("Previsto Total", f"R$ {total_previsto:,.2f}")
    col2.metric("Realizado Total", f"R$ {total_realizado:,.2f}")
    col3.metric("Saving Total", f"R$ {total_saving:,.2f}")

    st.divider()

    fig = px.line(
        df_financeiro,
        x="Mês",
        y=["Previsto", "Realizado", "Saving"],
        markers=True,
        title="Evolução Financeira"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("Tabela Financeira")

    st.dataframe(
        df_financeiro,
        use_container_width=True
    )

    csv = df_financeiro.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Baixar CSV",
        csv,
        "financeiro.csv",
        "text/csv"
    )

# =====================================
# ATIVOS
# =====================================

elif pagina == "📦 Ativos":

    st.title("📦 Ativos")

    st.metric("Total de Ativos", len(df_ativos))

    st.divider()

    st.dataframe(
        df_ativos,
        use_container_width=True
    )

# =====================================
# ESG
# =====================================

elif pagina == "🌱 ESG":

    st.title("🌱 ESG")

    st.metric("Total Registros ESG", len(df_esg))

    st.divider()

    st.dataframe(
        df_esg,
        use_container_width=True
    )

# =====================================
# SLAS
# =====================================

elif pagina == "⏱️ SLAs":

    st.title("⏱️ SLAs")

    st.metric("Total SLAs", len(df_slas))

    st.divider()

    st.dataframe(
        df_slas,
        use_container_width=True
    )

