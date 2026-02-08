import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Gênio Master Pro", layout="wide")

# --- LOGIN ---
if "logado" not in st.session_state:
    st.title("🔒 Gênio Master")
    senha = st.text_input("Chave de Acesso:", type="password")
    if st.button("Acessar"):
        if senha == "mestre2026":
            st.session_state["logado"] = True
            st.rerun()
        else:
            st.error("Senha incorreta")
    st.stop()

# --- CONFIGURAÇÃO DAS ABAS (VERIFIQUE O GID NA SUA PLANILHA) ---
# Dica: Abra sua planilha no navegador, clique na aba 'Esg' e veja o número após 'gid=' na URL.
config_abas = {
    "Financeiro": {"gid": "0", "cor": "#FFD700", "img": "header_financeiro.png"},
    "Ativos": {"gid": "1179272110", "cor": "#00CCFF", "img": "header_ativos.png"},
    "Esg": {"gid": "1026863401", "cor": "#00FF88", "img": "header_esg.png"},
    "Slas": {"gid": "2075740723", "cor": "#FF3366", "img": "header_slas.png"}
}

# --- MENU LATERAL ÚNICO ---
st.sidebar.title("🚀 Gênio Master")
setor = st.sidebar.selectbox("Selecione o Módulo", list(config_abas.keys()))
st.sidebar.divider()
st.sidebar.info(f"Módulo Atual: {setor}")

# --- HEADER ---
img_path = config_abas[setor]["img"]
if os.path.exists(img_path):
    st.image(img_path, use_container_width=True)
else:
    st.title(f"📊 Painel {setor}")

# --- CARREGAR DADOS ---
sheet_id = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4il3o"
gid = config_abas[setor]["gid"]
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gid}"

try:
    df = pd.read_csv(url)
    
    if not df.empty:
        # KPI Cards
        c1, c2, c3 = st.columns(3)
        c1.metric("Registros", len(df))
        c2.metric("Status", "Conectado ✅")
        c3.metric("Módulo", setor)

        st.divider()

        # Gráfico Dinâmico
        cols_texto = df.select_dtypes(include=['object']).columns
        if len(cols_texto) > 0:
            fig = px.pie(df, names=cols_texto[0], hole=0.4, 
                         title=f"Distribuição - {setor}",
                         color_discrete_sequence=[config_abas[setor]["cor"]])
            st.plotly_chart(fig, use_container_width=True)
        
        # Tabela
        with st.expander("Ver Dados Completos"):
            st.dataframe(df, use_container_width=True)
    else:
        st.warning(f"A aba {setor} parece estar vazia.")

except Exception as e:
    st.error(f"Erro ao conectar com {setor}. Verifique se o GID '{gid}' está correto na planilha.")
