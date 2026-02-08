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

# ID ÚNICO DA SUA PLANILHA (Confirmado pela Foto 74)
sheet_id = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4il3o"

# Menu lateral com nomes EXATOS (conforme suas fotos)
st.sidebar.header("Navegação")
aba_selecionada = st.sidebar.selectbox("Escolha o Painel", ["Financeiro", "Ativos", "Esg", "Slas"])

# Mapeamento de GIDs (Se o erro persistir em uma, testaremos o número)
gids = {
    "Financeiro": "0",
    "Ativos": "1179272110",
    "Esg": "1626002778",
    "Slas": "1805560751"
}

# Tenta ler a planilha
try:
    # URL de Exportação que ignora bloqueios básicos
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid={gids[aba_selecionada]}"
    
    # Lendo os dados
    df = pd.read_csv(url)
    
    if df.empty:
        st.warning(f"A aba '{aba_selecionada}' está conectada, mas parece não ter dados escritos.")
    else:
        st.subheader(f"Dados: {aba_selecionada}")
        st.dataframe(df, use_container_width=True)
        st.success("Conectado com sucesso!")

except Exception as e:
    st.error("⚠️ Erro de Conexão Crítico")
    st.write("Dica: Verifique se a planilha está em 'Qualquer pessoa com o link' e se você clicou em 'Publicar na Web'.")
    st.info(f"Detalhe técnico para o suporte: {e}")
