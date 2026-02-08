import streamlit as st
import pandas as pd

# Configuração visual da página
st.set_page_config(page_title="Gênio Master", layout="wide")

# --- SISTEMA DE LOGIN ---
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

# --- MENU LATERAL DE NAVEGAÇÃO ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1055/1055644.png", width=100)
st.sidebar.title("Navegação")
aba_escolhida = st.sidebar.radio(
    "Selecione o Painel:", 
    ["Financeiro", "Ativos", "ESG", "SLAs"]
)

st.title(f"📊 Painel: {aba_escolhida}")

# ID Único da sua planilha (Extraído dos seus links)
sheet_id = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"

# Mapeamento EXATO dos GIDs que me enviou
gids = {
    "Financeiro": "0",
    "Ativos": "1179272110",
    "ESG": "1026863401",
    "SLAs": "2075740723"
}

# --- CARREGAMENTO DOS DADOS ---
try:
    # Cria o link de exportação específico para a aba selecionada
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gids[aba_escolhida]}"
    
    df = pd.read_csv(url)
    
    # Exibição dos dados
    if df.empty:
        st.warning(f"A aba '{aba_escolhida}' está ligada, mas não tem dados na linha 2.")
    else:
        # Mostra a tabela de forma interativa
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.success(f"Dados de {aba_escolhida} carregados com sucesso!")

except Exception as e:
    st.error("Erro ao carregar os dados desta aba.")
    st.info("Dica: Verifique se escreveu algo na segunda linha da aba no Google Sheets.")
