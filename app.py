import streamlit as st
import pandas as pd
import plotly.express as px

# ID CORRIGIDO (Final com I maiúsculo)
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"

CONFIG = {
    "Financeiro": {"gid": "0", "cor": "#FFD700"},
    "Ativos": {"gid": "1179272110", "cor": "#00CCFF"},
    "Esg": {"gid": "1026863401", "cor": "#00FF88"},
    "Slas": {"gid": "2075740723", "cor": "#FF3366"}
}

st.set_page_config(page_title="Gênio Master", layout="wide")
st.sidebar.title("🚀 Gênio Master")
setor = st.sidebar.selectbox("Selecione o Módulo", list(CONFIG.keys()))

url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG[setor]['gid']}"

try:
    df = pd.read_csv(url)
    st.title(f"📊 Painel {setor}")
    if not df.empty:
        st.metric("Total de Registros", len(df))
        cols_texto = df.select_dtypes(include=['object']).columns
        if len(cols_texto) > 0:
            fig = px.pie(df, names=cols_texto[0], hole=0.4, color_discrete_sequence=[CONFIG[setor]["cor"]])
            st.plotly_chart(fig, use_container_width=True)
        st.dataframe(df)
except Exception as e:
    st.error("Erro de conexão. Verifique se o ID da planilha está correto no GitHub.")
