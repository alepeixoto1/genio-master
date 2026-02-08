import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da Página
st.set_page_config(page_title="Gênio Master 2026", layout="wide")

# --- 1. CONFIGURAÇÃO DA PLANILHA ---
# ID extraído do link que você enviou
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"

# GIDs conferidos um por um nos seus links
CONFIG = {
    "Financeiro": {"gid": "0", "cor": "#FFD700"},
    "Ativos": {"gid": "1179272110", "cor": "#00CCFF"},
    "Esg": {"gid": "1026863401", "cor": "#00FF88"}, 
    "Slas": {"gid": "2075740723", "cor": "#FF3366"}
}

# --- 2. MENU LATERAL ---
st.sidebar.title("🚀 Gênio Master 2026")
setor = st.sidebar.selectbox("Escolha o Módulo", list(CONFIG.keys()))
st.sidebar.divider()
st.sidebar.info(f"Módulo Atual: {setor}")

# --- 3. PROCESSAMENTO DE DADOS ---
# Link de exportação CSV do Google Sheets
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG[setor]['gid']}"

try:
    # skiprows=2 pula o título da aba e a linha em branco
    df = pd.read_csv(url, skiprows=2)
    
    st.title(f"📊 Painel {setor}")
    
    # Remove colunas totalmente vazias que o Google Sheets às vezes envia
    df = df.dropna(how='all', axis=1).dropna(how='all', axis=0)

    if not df.empty:
        # Layout de Indicadores
        m1, m2 = st.columns(2)
        m1.metric("Registros Encontrados", len(df))
        m2.metric("Status da Base", "Conectada ✅")
        
        st.divider()

        # Criando o Gráfico de Pizza dinâmico
        # Pega a primeira coluna de texto para as legendas
        cols_texto = df.select_dtypes(include=['object']).columns
        
        if len(cols_texto) > 0:
            col_nome = cols_texto[0]
            fig = px.pie(
                df, 
                names=col_nome, 
                title=f"Distribuição por {col_nome}",
                hole=0.4,
                color_discrete_sequence=[CONFIG[setor]["cor"]]
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Não encontramos colunas de texto para gerar o gráfico.")

        # Exibição dos dados brutos
        with st.expander("📄 Visualizar Tabela de Dados"):
            st.dataframe(df, use_container_width=True)
            
    else:
        st.warning(f"A aba '{setor}' parece estar vazia na planilha.")

except Exception as e:
    st.error(f"⚠️ Erro ao conectar com o módulo {setor}")
    st.info("Verifique se a planilha está compartilhada como 'Qualquer pessoa com o link pode ler'.")
