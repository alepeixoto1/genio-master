import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração Inicial
st.set_page_config(page_title="Gênio Master 2026", layout="wide")

# 2. Identificação Única da Planilha (ID revisado)
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"

# Configuração de Cores e GIDs
CONFIG = {
    "Financeiro": {"gid": "0", "cor": "#00FFA3"},
    "Ativos": {"gid": "1179272110", "cor": "#00B2FF"},
    "Esg": {"gid": "1026863401", "cor": "#BF5AF2"},
    "Slas": {"gid": "2075740723", "cor": "#FF375F"}
}

# 3. Menu Lateral
st.sidebar.title("🚀 Gênio Master")
setor = st.sidebar.selectbox("Módulo Ativo:", list(CONFIG.keys()))

# 4. Construção do Link de Dados
# Usamos o link direto que você testou e funcionou
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG[setor]['gid']}"

try:
    # Lendo os dados - Pula 2 linhas iniciais da sua planilha
    df = pd.read_csv(url, skiprows=2)
    
    # Limpeza básica: remove linhas/colunas totalmente vazias
    df = df.dropna(how='all', axis=1).dropna(how='all', axis=0)

    st.markdown(f"<h1 style='text-align: center; color: {CONFIG[setor]['cor']};'>📊 {setor.upper()}</h1>", unsafe_allow_html=True)

    if not df.empty:
        col1, col2 = st.columns(2)

        with col1:
            # Gráfico de Rosca (Donut)
            cols_texto = df.select_dtypes(include=['object']).columns
            if len(cols_texto) > 0:
                fig_pie = px.pie(df, names=cols_texto[0], hole=0.7,
                                 color_discrete_sequence=[CONFIG[setor]["cor"], "#2D2D2D"])
                st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            # Gráfico de Barras
            cols_num = df.select_dtypes(include=['number']).columns
            if len(cols_texto) > 0 and len(cols_num) > 0:
                fig_bar = px.bar(df.head(10), x=cols_num[0], y=cols_texto[0], orientation='h',
                                 color_discrete_sequence=[CONFIG[setor]["cor"]])
                st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("### 📋 Visão Detalhada")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("A aba selecionada parece estar sem dados abaixo da linha 3.")

except Exception as e:
    st.error("⚠️ Ocorreu um erro ao processar os dados.")
    st.info(f"Detalhe técnico: {e}")
