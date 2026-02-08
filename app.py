import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Gênio Master", layout="wide")

# Sistema de Login
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

st.title("📊 Painel de Facilities - Gênio Master")

# ID Único da sua planilha
sheet_id = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"

# Menu lateral para navegar entre as planilhas
st.sidebar.header("Navegação")
aba_selecionada = st.sidebar.radio(
    "Selecione o Painel:", 
    ["Financeiro", "Ativos", "ESG", "SLAs"]
)

# Mapeamento EXATO dos GIDs que você enviou
gids = {
    "Financeiro": "0",
    "Ativos": "1179272110",
    "ESG": "1026863401",
    "SLAs": "2075740723"
}

try:
    # Monta o link de exportação para a aba escolhida
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gids[aba_selecionada]}"
    
    # Lê os dados
    df = pd.read_csv(url)
    
    st.subheader(f"Exibindo: {aba_selecionada}")
    
    if df.empty:
        st.info(f"A aba {aba_selecionada} está conectada, mas não possui dados preenchidos.")
    else:
        st.dataframe(df, use_container_width=True)
        st.success(f"Dados de {aba_selecionada} atualizados!")

except Exception as e:
    st.error("Erro ao carregar os dados.")
    st.info("Certifique-se de que a planilha está compartilhada como 'Qualquer pessoa com o link'.")
