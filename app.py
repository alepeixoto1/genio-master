import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuração Profissional
st.set_page_config(page_title="Gênio Master 2026", layout="wide")

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

# --- MAPEAMENTO REAL DOS SEUS GIDs ---
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4il3o"
CONFIG_MODULOS = {
    "Financeiro": {"gid": "0", "cor": "#FFD700", "img": "header_financeiro.png"},
    "Ativos": {"gid": "1179272110", "cor": "#00CCFF", "img": "header_ativos.png"},
    "Esg": {"gid": "1026863401", "cor": "#00FF88", "img": "header_esg.png"},
    "Slas": {"gid": "2075740723", "cor": "#FF3366", "img": "header_slas.png"}
}

# --- MENU LATERAL ---
st.sidebar.title("🚀 Gênio Master 2026")
setor = st.sidebar.selectbox("Escolha o Módulo", list(CONFIG_MODULOS.keys()))
st.sidebar.divider()
st.sidebar.success(f"Módulo Ativo: {setor}")

# --- CABEÇALHO ---
img_path = CONFIG_MODULOS[setor]["img"]
if os.path.exists(img_path):
    st.image(img_path, use_container_width=True)
else:
    st.title(f"📊 Gestão de {setor}")

# --- CARREGAMENTO DE DADOS (Padrão Multinacional) ---
# Aqui usamos o ID e o GID exatos que você enviou
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG_MODULOS[setor]['gid']}"

try:
    df = pd.read_csv(url)
    
    if not df.empty:
        # Camada de KPIs
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Total de Itens", len(df))
        kpi2.metric("Base de Dados", "Sincronizada ✅")
        kpi3.metric("Módulo", setor)
        
        st.divider()
        
        # Dashboard Visual
        col_graf, col_info = st.columns([2, 1])
        
        with col_graf:
            # Gráfico dinâmico baseado na primeira coluna de texto (Status ou Categoria)
            cols_obj = df.select_dtypes(include=['object']).columns
            if len(cols_obj) > 0:
                fig = px.pie(df, names=cols_obj[0], hole=0.4, 
                             title=f"Visão Geral: {setor}",
                             color_discrete_sequence=[CONFIG_MODULOS[setor]["cor"]])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Adicione dados de texto na planilha para gerar o gráfico.")

        with col_info:
            st.markdown(f"### 📋 Detalhes {setor}")
            st.write("Dados extraídos em tempo real da nuvem.")
            if st.button("🔄 Forçar Atualização"):
                st.rerun()

        # Tabela Profissional
        with st.expander("🔍 Visualizar Planilha Completa"):
            st.dataframe(df, use_container_width=True)

    else:
        st.warning(f"A aba '{setor}' está conectada, mas não contém dados.")

except Exception as e:
    st.error(f"Erro ao conectar com o módulo {setor}.")
    st.info("Verifique se a aba na planilha não foi renomeada ou excluída.")
