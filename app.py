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

# ID Único da sua planilha (Extraído da sua Foto 74)
sheet_id = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4il3o"

# Menu lateral com nomes limpos
st.sidebar.header("Navegação")
aba_nome = st.sidebar.selectbox("Escolha o Painel", ["Financeiro", "Ativos", "Esg", "Slas"])

# Mapeamento de GIDs (Identificadores das abas da sua planilha)
gids = {
    "Financeiro": "0",
    "Ativos": "1179272110",
    "Esg": "1026863401",
    "Slas": "2075740723"
}

try:
    # URL de exportação direta para CSV
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gids[aba_nome]}"
    
    # Carregando os dados da planilha
    df = pd.read_csv(url)
    
    if df.empty:
        st.warning(f"A aba '{aba_nome}' está conectada, mas não possui dados preenchidos na linha 2.")
    else:
        st.subheader(f"Dados: {aba_nome}")
        st.dataframe(df, use_container_width=True)
        st.success(f"Conectado com sucesso ao painel de {aba_nome}!")

except Exception as e:
    st.error(f"⚠️ Não foi possível carregar a aba '{aba_nome}'.")
    st.info("Dica: Verifique se a planilha está como 'Qualquer pessoa com o link' e se você clicou em 'Publicar na Web'.")
    st.write(f"Erro técnico para ajuste: {e}")
