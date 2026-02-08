import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gênio Master", layout="wide")

# Login Master
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

# ID Único da sua planilha
sheet_id = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"

# Menu lateral revisado
st.sidebar.header("Navegação")
aba_nome = st.sidebar.selectbox("Escolha o Painel", ["Financeiro", "Ativos", "Esg", "Slas"])

# GIDs confirmados pelos seus links
gids = {
    "Financeiro": "0",
    "Ativos": "1179272110",
    "Esg": "1026863401",
    "Slas": "2075740723"
}

try:
    # URL de exportação correta
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gids[aba_nome]}"
    
    # Lendo os dados
    df = pd.read_csv(url)
    
    if df.empty:
        st.warning(f"A aba '{aba_nome}' está sem dados na linha 2.")
    else:
        st.subheader(f"Dados: {aba_nome}")
        st.dataframe(df, use_container_width=True)
        st.success(f"Conectado com sucesso!")

except Exception as e:
    st.error(f"Erro ao carregar a aba '{aba_nome}'.")
    st.write("Dica: Verifique se a planilha está em 'Qualquer pessoa com o link' (Leitor).")
