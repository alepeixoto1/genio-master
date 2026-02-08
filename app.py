import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gênio Master", layout="wide")

# Login
if "logado" not in st.session_state:
    st.title("🔒 Gênio Master")
    senha = st.text_input("Senha Master:", type="password")
    if st.button("Acessar"):
        if senha == "mestre2026":
            st.session_state["logado"] = True
            st.rerun()
        else:
            st.error("Senha incorreta")
    st.stop()

st.title("📊 Painel de Controle - Gênio Master")

# O LINK QUE VOCÊ ME MANDOU, AJUSTADO PARA O SISTEMA LER:
url_publica = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQlUCy8YHlnRGlxmkkp-c9wbg9-ZqEVcubbjvUX715_SwQv1-YnNGpbi0FJ8QD2pyf2VSUGH14Nl-VP/pub?output=csv"

try:
    # Carregando os dados
    df = pd.read_csv(url_publica)
    
    st.subheader("Dados em Tempo Real")
    st.dataframe(df, use_container_width=True)
    st.success("Conectado com sucesso via Web!")

except Exception as e:
    st.error(f"Erro ao ler dados: {e}")
    st.info("Certifique-se de que a planilha tem dados preenchidos na linha 2.")
