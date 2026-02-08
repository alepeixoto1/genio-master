import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuração de Página
st.set_page_config(page_title="Gênio Master 2026", layout="wide")

# --- 1. CONFIGURAÇÃO DE ACESSO (DADOS) ---
# Substitua os GIDs abaixo pelos números que aparecem no final da URL da sua planilha Google
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4il3o"
CONFIG = {
    "Financeiro": {"gid": "0", "cor": "#FFD700"},
    "Ativos": {"gid": "1179272110", "cor": "#00CCFF"},
    "Esg": {"gid": "1026863401", "cor": "#00FF88"},
    "Slas": {"gid": "2075740723", "cor": "#FF3366"}
}

# --- 2. MENU LATERAL (LIMPO E ÚNICO) ---
st.sidebar.title("🚀 Gênio Master 2026")
setor = st.sidebar.selectbox("Navegação por Módulo", list(CONFIG.keys()))
st.sidebar.divider()
st.sidebar.markdown(f"**Módulo Ativo:** {setor}")

# --- 3. LOGICA DE CARREGAMENTO ---
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG[setor]['gid']}"

try:
    df = pd.read_csv(url)
    
    st.title(f"📊 Painel de {setor}")
    
    if not df.empty:
        # Indicadores principais
        col1, col2 = st.columns(2)
        col1.metric("Total de Registros", len(df))
        col2.metric("Status da Conexão", "Online ✅")
        
        st.divider()
        
        # Gráfico Automático (Pega a primeira coluna de texto)
        cols_txt = df.select_dtypes(include=['object']).columns
        if len(cols_txt) > 0:
            fig = px.pie(df, names=cols_txt[0], hole=0.4, 
                         color_discrete_sequence=[CONFIG[setor]["cor"]])
            st.plotly_chart(fig, use_container_width=True)
            
        # Tabela de Dados
        with st.expander("🔍 Ver base de dados completa"):
            st.dataframe(df, use_container_width=True)
    else:
        st.warning(f"A aba {setor} na planilha parece estar vazia.")

except Exception as e:
    st.error(f"Erro de Conexão no Módulo {setor}")
    st.info("Certifique-se de que o GID no código é o mesmo da aba na sua planilha do Google.")
