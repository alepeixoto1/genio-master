import streamlit as st
import pandas as pd

# Link direto da sua planilha (Foto 3)
URL = "https://docs.google.com/spreadsheets/d/1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o/export?format=csv"

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
