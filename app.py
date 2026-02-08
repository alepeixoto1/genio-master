import streamlit as st
import pandas as pd

# Configuração da página
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

st.title("📊 Painel de Facilities")

# ID da sua planilha que confirmamos antes
sheet_id = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4il3o"

# Menu lateral para suas abas reais
st.sidebar.header("Navegação")
aba_nome = st.sidebar.selectbox("Escolha o Painel", ["Financeiro", "Ativos", "Esg", "Slas"])

# Mapeamento dos GIDs das suas abas (vimos nas Fotos 63-66)
gids = {
    "Financeiro": "0",
    "Ativos": "1179272110",
    "Esg": "1626002778",
    "Slas": "1805560751"
}

try:
    # Monta a URL de exportação que o Google Sheets aceita
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gids[aba_nome]}"
    df = pd.read_csv(url)
    
    st.subheader(f"Dados: {aba_nome}")
    st.dataframe(df, use_container_width=True)
    st.success("Dados carregados com sucesso!")
except Exception as e:
    st.error("Erro ao carregar os dados desta aba.")
    st.info("Verifique se você preencheu dados na planilha Google.")
