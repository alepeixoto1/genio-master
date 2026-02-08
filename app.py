import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração Padrão Corporativo
st.set_page_config(page_title="Gênio Master 2026", layout="wide")

# --- 1. IDENTIFICAÇÃO DA PLANILHA ---
# O SHEET_ID é o código longo que está na URL da sua planilha
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4il3o"

# IMPORTANTE: Verifique os números GID no final da URL de cada aba na sua planilha Google
CONFIG = {
    "Financeiro": {"gid": "0", "cor": "#FFD700"},
    "Ativos": {"gid": "1179272110", "cor": "#00CCFF"},
    "Esg": {"gid": "1026863401", "cor": "#00FF88"}, 
    "Slas": {"gid": "2075740723", "cor": "#FF3366"}
}

# --- 2. MENU LATERAL ÚNICO (Sem duplicação) ---
st.sidebar.title("🚀 Gênio Master 2026")
setor = st.sidebar.selectbox("Escolha o Módulo", list(CONFIG.keys()))
st.sidebar.divider()
st.sidebar.info(f"Visualizando: {setor}")

# --- 3. CONEXÃO E GRÁFICOS ---
# Gerando o link direto para a aba selecionada
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG[setor]['gid']}"

try:
    df = pd.read_csv(url)
    st.title(f"📊 Painel de {setor}")
    
    if not df.empty:
        # Indicadores Rápidos
        col1, col2 = st.columns(2)
        col1.metric("Total de Itens", len(df))
        col2.metric("Conexão", "Ativa ✅")
        
        # Gráfico Automático
        # Ele tenta encontrar a primeira coluna com nomes/texto para fazer a pizza
        cols_texto = df.select_dtypes(include=['object']).columns
        if len(cols_texto) > 0:
            fig = px.pie(df, names=cols_texto[0], hole=0.4, 
                         color_discrete_sequence=[CONFIG[setor]["cor"]])
            st.plotly_chart(fig, use_container_width=True)
            
        # Tabela Escondida (Expander)
        with st.expander("Ver base de dados completa"):
            st.dataframe(df, use_container_width=True)
    else:
        st.warning(f"A aba '{setor}' na sua planilha parece estar vazia.")

except Exception as e:
    st.error(f"⚠️ Erro de Conexão no Módulo {setor}")
    st.markdown(f"""
    **O que pode ter acontecido?**
    * O número **GID** ({CONFIG[setor]['gid']}) no código não bate com o da aba na planilha.
    * A aba ainda não tem dados inseridos.
    """)
