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

# ID Único da sua planilha (confirmado)
sheet_id = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4il3o"

# Menu lateral
st.sidebar.header("Navegação")
aba_nome = st.sidebar.selectbox("Escolha o Painel", ["Financeiro", "Ativos", "Esg", "Slas"])

# GIDs das suas abas (Ajustados conforme seus novos links)
gids = {
    "Financeiro": "0",
    "Ativos": "1179272110",
    "Esg": "1026863401",  # Conferido do seu link anterior
    "Slas": "2075740723"  # Conferido do seu link anterior
}

try:
    # URL de exportação
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gids[aba_nome]}"
    df = pd.read_csv(url)
    
    st.subheader(f"Dados: {aba_nome}")
    st.dataframe(df, use_container_width=True)
    st.success(f"Conectado com sucesso à aba {aba_nome}!")

except Exception as e:
    st.error(f"A aba '{aba_nome}' ainda não foi configurada corretamente na planilha.")
    st.info("Verifique se o nome da aba no Google Sheets está EXATAMENTE igual ao menu lateral.")
    st.write(f"Erro técnico: {e}")
