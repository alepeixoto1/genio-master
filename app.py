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

# ID da sua planilha
sheet_id = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4il3o"

# Menu lateral
st.sidebar.header("Navegação")
# Note que mudei a ordem para "Ativos" ser a primeira, já que é a que vimos o ID
aba_nome = st.sidebar.selectbox("Escolha o Painel", ["Ativos", "Financeiro", "Esg", "Slas"])

# GIDs extraídos das suas fotos
gids = {
    "Ativos": "1179272110",
    "Financeiro": "0",
    "Esg": "1626002778",
    "Slas": "1805560751"
}

try:
    # URL de exportação direta
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gids[aba_nome]}"
    df = pd.read_csv(url)
    
    if df.empty:
        st.warning(f"A aba '{aba_nome}' está conectada, mas não possui dados preenchidos.")
    else:
        st.subheader(f"Dados: {aba_nome}")
        st.dataframe(df, use_container_width=True)
        st.success("Conectado com sucesso!")
except Exception as e:
    st.error("Erro de conexão.")
    st.info("Verifique se a aba no Google Sheets tem pelo menos uma linha com dados.")
