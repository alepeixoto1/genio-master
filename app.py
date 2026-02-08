import streamlit as st
import pandas as pd

# Link mestre que você gerou na Foto 3
URL_MESTRE = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQlUCy8YHlnRGlxmkkp-c9wbg9-ZqEVcubbjvUX715_SwQv1-YnNGpbiOFJ8QD2pyf2VSUGH14NI-VP/pub?output=csv"

st.set_page_config(page_title="Gênio Master", layout="wide")

# LOGIN
if "auth" not in st.session_state:
    st.title("🤖 Gênio Master - Acesso")
    senha = st.text_input("Senha Master:", type="password")
    if st.button("Acessar"):
        if senha == "mestre2026":
            st.session_state["auth"] = True
            st.rerun()
        else:
            st.error("Senha incorreta")
    st.stop()

# INTERFACE PRINCIPAL
st.sidebar.title("Menu de Comando")
opcao = st.sidebar.selectbox("Escolha a Visão:", ["Geral (Dados)", "Sustentabilidade (ESG)", "Nível de Serviço (SLA)"])

try:
    # O Google Sheets publica por padrão a primeira aba. 
    # Para ler as outras, usamos o parâmetro 'gid' que você enviou.
    if opcao == "Geral (Dados)":
        url = URL_MESTRE + "&gid=0"
        st.header("📊 Dados da Operação")
    elif opcao == "Sustentabilidade (ESG)":
        url = URL_MESTRE + "&gid=1179272110"
        st.header("🌱 Indicadores ESG")
    elif opcao == "Nível de Serviço (SLA)":
        url = URL_MESTRE + "&gid=2075740723"
        st.header("📜 Gestão de SLAs")

    df = pd.read_csv(url)
    st.dataframe(df, use_container_width=True)
    st.success(f"Dados de {opcao} atualizados!")

except Exception as e:
    st.error("Erro ao conectar com as abas da planilha. Verifique se o documento está 'Publicado na Web'.")
