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

st.title("📊 Painel de Facilities")

# ID da sua planilha (Extraído da sua foto 74)
sheet_id = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4il3o"

# Menu lateral
st.sidebar.header("Navegação")
aba_nome = st.sidebar.selectbox("Escolha o Painel", ["Financeiro", "Ativos", "Esg", "Slas"])

# GIDs das suas abas (Conforme seus links enviados)
gids = {
    "Financeiro": "0",
    "Ativos": "1179272110",
    "Esg": "1026863401",
    "Slas": "2075740723"
}

try:
    # URL de exportação
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gids[aba_nome]}"
    df = pd.read_csv(url)
    
    if df.empty:
        st.warning(f"A aba '{aba_nome}' está conectada, mas não possui dados preenchidos.")
    else:
        st.subheader(f"Dados: {aba_nome}")
        st.dataframe(df, use_container_width=True)
        st.success(f"Conectado com sucesso!")

except Exception as e:
    st.error(f"Erro ao carregar a aba '{aba_nome}'.")
    st.write(f"Detalhe: {e}")
