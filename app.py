import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# CONFIGURAÇÃO
# =====================================================

st.set_page_config(
    page_title="Gênio Master",
    layout="wide",
    page_icon="💎"
)

# =====================================================
# ESTILO PROFISSIONAL (igual imagem)
# =====================================================

st.markdown("""
<style>

.stApp {
    background-color: #f1f5f9;
}

.card {
    background: linear-gradient(135deg,#0f172a,#1e293b);
    padding:20px;
    border-radius:14px;
    color:white;
    box-shadow:0 4px 12px rgba(0,0,0,0.15);
}

.card-title {
    font-size:13px;
    opacity:0.7;
}

.card-value {
    font-size:28px;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# MENU LATERAL
# =====================================================

menu = st.sidebar.radio(
    "Menu",
    [
        "Dashboard",
        "Financeiro",
        "Ativos",
        "ESG",
        "SLAs"
    ]
)

# =====================================================
# CONEXÃO COM PLANILHA (SEGURO)
# =====================================================

SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"

def carregar(gid):

    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"

    df = pd.read_csv(url)

    # limpar nomes
    df.columns = df.columns.str.strip()

    # converter números
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")

    return df

df_fin = carregar("0")
df_ativos = carregar("1179272110")
df_esg = carregar("1026863401")
df_slas = carregar("2075740723")

# =====================================================
# DASHBOARD
# =====================================================

if menu == "Dashboard":

    st.title("💎 Dashboard Executivo")

    realizado = df_fin["Realizado"].sum() if "Realizado" in df_fin else 0
    saving = df_fin["Saving"].sum() if "Saving" in df_fin else 0
    ativos = len(df_ativos)

    c1,c2,c3 = st.columns(3)

    with c1:
        st.markdown(f"""
        <div class="card">
        <div class="card-title">REALIZADO</div>
        <div class="card-value">R$ {realizado:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="card">
        <div class="card-title">SAVING</div>
        <div class="card-value">R$ {saving:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="card">
        <div class="card-title">ATIVOS</div>
        <div class="card-value">{ativos}</div>
        </div>
        """, unsafe_allow_html=True)

    col1,col2 = st.columns(2)

    if "Mês" in df_fin and "Realizado" in df_fin:

        fig1 = px.line(
            df_fin,
            x="Mês",
            y="Realizado",
            markers=True,
            title="Performance Financeira"
        )

        col1.plotly_chart(fig1, use_container_width=True)

    if "Categoria" in df_fin and "Realizado" in df_fin:

        fig2 = px.pie(
            df_fin,
            names="Categoria",
            values="Realizado",
            hole=0.6,
            title="Distribuição"
        )

        col2.plotly_chart(fig2, use_container_width=True)

# =====================================================
# FINANCEIRO
# =====================================================

elif menu == "Financeiro":

    st.title("💰 Financeiro")

    st.dataframe(df_fin, use_container_width=True)

    if "Previsto" in df_fin and "Realizado" in df_fin:

        fig = px.bar(
            df_fin,
            x="Mês",
            y=["Previsto","Realizado"],
            barmode="group"
        )

        st.plotly_chart(fig, use_container_width=True)

# =====================================================
# ATIVOS
# =====================================================

elif menu == "Ativos":

    st.title("📦 Ativos")

    st.metric("Total", len(df_ativos))

    st.dataframe(df_ativos, use_container_width=True)

# =====================================================
# ESG
# =====================================================

elif menu == "ESG":

    st.title("🌱 ESG")

    st.metric("Total", len(df_esg))

    st.dataframe(df_esg, use_container_width=True)

# =====================================================
# SLAs
# =====================================================

elif menu == "SLAs":

    st.title("⏱️ SLAs")

    st.metric("Total", len(df_slas))

    st.dataframe(df_slas, use_container_width=True)


