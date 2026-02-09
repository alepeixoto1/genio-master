import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================
# CONFIG
# =========================================

st.set_page_config(
    page_title="Gênio Master",
    layout="wide",
    page_icon="💎"
)

# =========================================
# CSS PROFISSIONAL
# =========================================

st.markdown("""
<style>

.stApp {
    background-color: #f4f7fb;
}

.card {
    background: linear-gradient(135deg,#0f172a,#1e293b);
    padding:20px;
    border-radius:12px;
    color:white;
}

.metric-title {
    font-size:13px;
    opacity:0.7;
}

.metric-value {
    font-size:28px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# MENU
# =========================================

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Dashboard",
        "Financeiro",
        "Ativos",
        "ESG",
        "SLAs"
    ]
)

# =========================================
# GOOGLE SHEETS
# =========================================

SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"

def load(gid):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
    return pd.read_csv(url)

df_fin = load("0")
df_ativos = load("1179272110")
df_esg = load("1026863401")
df_slas = load("2075740723")

# =========================================
# DASHBOARD
# =========================================

if menu == "Dashboard":

    st.title("💎 Dashboard Executivo")

    total = df_fin["Realizado"].sum()
    saving = df_fin["Saving"].sum()
    ativos = len(df_ativos)

    c1,c2,c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="card">
        <div class="metric-title">REALIZADO</div>
        <div class="metric-value">R$ {total:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="card">
        <div class="metric-title">SAVING</div>
        <div class="metric-value">R$ {saving:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="card">
        <div class="metric-title">ATIVOS</div>
        <div class="metric-value">{ativos}</div>
        </div>
        """, unsafe_allow_html=True)

    col1,col2 = st.columns(2)

    fig1 = px.line(
        df_fin,
        x="Mês",
        y="Realizado",
        title="Performance"
    )

    col1.plotly_chart(fig1, use_container_width=True)

    fig2 = px.pie(
        df_fin,
        names="Categoria",
        values="Realizado",
        hole=0.6
    )

    col2.plotly_chart(fig2, use_container_width=True)

# =========================================
# FINANCEIRO
# =========================================

elif menu == "Financeiro":

    st.title("💰 Financeiro")

    c1,c2,c3 = st.columns(3)

    c1.metric("Previsto", f"R$ {df_fin['Previsto'].sum():,.0f}")
    c2.metric("Realizado", f"R$ {df_fin['Realizado'].sum():,.0f}")
    c3.metric("Saving", f"R$ {df_fin['Saving'].sum():,.0f}")

    fig = px.bar(
        df_fin,
        x="Mês",
        y=["Previsto","Realizado"]
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(df_fin, use_container_width=True)

    csv = df_fin.to_csv(index=False).encode()

    st.download_button(
        "Baixar CSV",
        csv,
        "financeiro.csv"
    )

# =========================================
# ATIVOS
# =========================================

elif menu == "Ativos":

    st.title("📦 Ativos")

    st.metric("Total", len(df_ativos))

    st.dataframe(df_ativos, use_container_width=True)

    fig = px.bar(df_ativos)

    st.plotly_chart(fig, use_container_width=True)

# =========================================
# ESG
# =========================================

elif menu == "ESG":

    st.title("🌱 ESG")

    st.metric("Total", len(df_esg))

    st.dataframe(df_esg, use_container_width=True)

    fig = px.bar(df_esg)

    st.plotly_chart(fig, use_container_width=True)

# =========================================
# SLAs
# =========================================

elif menu == "SLAs":

    st.title("⏱️ SLAs")

    st.metric("Total", len(df_slas))

    st.dataframe(df_slas, use_container_width=True)

    fig = px.bar(df_slas)

    st.plotly_chart(fig, use_container_width=True)

