import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração Padrão Corporativo
st.set_page_config(page_title="Gênio Master 2026", layout="wide")

# --- 1. IDENTIFICAÇÃO DA PLANILHA ---
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4il3o"

# IMPORTANTE: Se o Financeiro der erro 404, confirme o GID na URL da planilha!
CONFIG = {
    "Financeiro": {"gid": "0", "cor": "#FFD700"},
    "Ativos": {"gid": "1179272110", "cor": "#00CCFF"},
    "Esg": {"gid": "1026863401", "cor": "#00FF88"}, 
    "Slas": {"gid": "2075740723", "cor": "#FF3366"}
}

# --- 2. MENU LATERAL ---
st.sidebar.title("🚀 Gênio Master 2026")
setor = st.sidebar.selectbox("Escolha o Módulo", list(CONFIG.keys()))
st.sidebar.divider()
st.sidebar.info(f"Visualizando: {setor}")

# --- 3. CONEXÃO E GRÁFICOS ---
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG[setor]['gid']}"

try:
    df = pd.read_csv(url)
    st.title(f"📊 Painel de {setor}")
    
    if not df.empty:
        col1, col2 = st.columns(2)
        col1.metric("Total de Itens", len(df))
        col2.metric("Conexão", "Ativa ✅")
        
        cols_texto = df.select_dtypes(include=['object']).columns
        if len(cols_texto) > 0:
            fig = px.pie(df, names=cols_texto[0], hole=0.4, 
                         color_discrete_sequence=[CONFIG[setor]["cor"]])
            st.plotly_chart(fig, use_container_width=True)
            
        with st.expander("Ver base de dados completa"):
            st.dataframe(df, use_container_width=True)
    else:
        st.warning(f"A aba '{setor}' parece estar vazia.")

except Exception as e:
    st.error(f"⚠️ Erro de Conexão no Módulo {setor}")
    st.write("Verifique se a planilha está configurada como 'Qualquer pessoa com o link pode ler'.")
