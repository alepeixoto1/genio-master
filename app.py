import streamlit as st
import pandas as pd

# Link direto da sua planilha (Foto 3)
URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQlUCy8YHlnRGlxmkkp-c9wbg9-ZqEVcubbjvUX715_SwQv1-YnNGpbiOFJ8QD2pyf2VSUGH14NI-VP/pub?output=csv"

st.set_page_config(page_title="Gênio Master", layout="wide")

if "logado" not in st.session_state:
    st.title("🤖 Gênio Master")
    senha = st.text_input("Senha Master:", type="password")
    if st.button("Acessar"):
        if senha == "mestre2026":
            st.session_state["logado"] = True
            st.rerun()
        else:
            st.error("Senha incorreta")
    st.stop()

st.header("📊 Painel de Facilities")
try:
    df = pd.read_csv(URL)
    st.success("Conectado com sucesso!")
    st.dataframe(df)
except:
    st.error("Erro ao ler dados da planilha.")
