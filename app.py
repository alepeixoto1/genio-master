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

# O SEU NOVO LINK DE PUBLICAÇÃO (Extraído do que você enviou)
base_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQlUCy8YHlnRGlxmkkp-c9wbg9-ZqEVcubbjvUX715_SwQv1-YnNGpbi0FJ8QD2pyf2VSUGH14Nl-VP/pub?output=csv"

# Menu lateral para as suas abas
st.sidebar.header("Navegação")
aba_selecionada = st.sidebar.selectbox("Escolha o Painel", ["Financeiro", "Ativos", "Esg", "Slas"])

# Mapeamento dos GIDs para o link de publicação
gids = {
    "Financeiro": "0",
    "Ativos": "1179272110",
    "Esg": "1626002778",
    "Slas": "1805560751"
}

try:
    # Monta o link final para download do CSV de cada aba
    final_url = f"{base_url}&gid={gids[aba_selecionada]}"
    df = pd.read_csv(final_url)
    
    if df.empty:
        st.warning(f"A aba '{aba_selecionada}' está conectada, mas não tem dados preenchidos.")
    else:
        st.subheader(f"Dados: {aba_selecionada}")
        st.dataframe(df, use_container_width=True)
        st.success("Conectado com sucesso!")

except Exception as e:
    st.error("Erro ao carregar os dados. Verifique se a planilha tem informações preenchidas.")
    st.info(f"Erro técnico: {e}")
