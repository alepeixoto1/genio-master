import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Gênio Master 2026", layout="wide")

# --- 1. AJUSTE OS NÚMEROS GID AQUI ---
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4il3o"
CONFIG = {
    "Financeiro": {"gid": "0", "cor": "#FFD700"},
    "Ativos": {"gid": "1179272110", "cor": "#00CCFF"},
    "Esg": {"gid": "1026863401", "cor": "#00FF88"}, # Troque se for diferente na sua planilha
    "Slas": {"gid": "2075740723", "cor": "#FF3366"}  # Troque se for diferente na sua planilha
}

# --- 2. MENU LATERAL ÚNICO ---
st.sidebar.title("🚀 Gênio Master 2026")
# Use apenas um selectbox para não dar erro
setor = st.sidebar.selectbox("Selecione o Módulo", list(CONFIG.keys()), key="menu_unico")

# --- 3. CONEXÃO E DASHBOARD ---
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG[setor]['gid']}"

try:
    df = pd.read_csv(url)
    st.header(f"📊 Painel de {setor}")
    
    if not df.empty:
        st.metric("Total de Registros", len(df))
        
        # Gráfico dinâmico
        cols_texto = df.select_dtypes(include=['object']).columns
        if len(cols_texto) > 0:
            fig = px.pie(df, names=cols_texto[0], hole=0.4, color_discrete_sequence=[CONFIG[setor]["cor"]])
            st.plotly_chart(fig, use_container_width=True)
            
        with st.expander("Ver dados completos"):
            st.dataframe(df, use_container_width=True)
    else:
        st.warning("Esta aba está vazia na sua planilha.")

except Exception as e:
    st.error(f"Erro de Conexão no Módulo {setor}")
    st.info(f"Detalhe técnico: {e}")
