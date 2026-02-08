import streamlit as st
import pandas as pd
import plotly.express as px

# 1. IDENTIFICAÇÃO CORRETA (Cuidado com o final 'l3o')
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"

CONFIG = {
    "Financeiro": {"gid": "0", "cor": "#FFD700"},
    "Ativos": {"gid": "1179272110", "cor": "#00CCFF"},
    "Esg": {"gid": "1026863401", "cor": "#00FF88"},
    "Slas": {"gid": "2075740723", "cor": "#FF3366"}
}

st.set_page_config(page_title="Gênio Master", layout="wide")

# 2. MENU LATERAL
st.sidebar.title("🚀 Gênio Master")
setor = st.sidebar.selectbox("Selecione o Módulo", list(CONFIG.keys()))

# 3. CONEXÃO COM A ABA CORRETA
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG[setor]['gid']}"

try:
    # O segredo para não dar erro de cache é o 'on_map' ou limpar o cache do pandas
    df = pd.read_csv(url)
    
    st.title(f"📊 Painel {setor}")
    
    if not df.empty:
        # Indicadores Rápidos
        st.metric("Total de Registros", len(df))
        
        # Gráfico de Pizza Dinâmico
        # Ele tenta pegar a primeira coluna de texto para fazer o gráfico
        cols_texto = df.select_dtypes(include=['object']).columns
        if len(cols_texto) > 0:
            fig = px.pie(df, names=cols_texto[0], hole=0.4, 
                         color_discrete_sequence=[CONFIG[setor]["cor"]])
            fig.update_layout(showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
        
        # Exibição da Tabela
        with st.expander("🔍 Ver Dados Brutos"):
            st.dataframe(df, use_container_width=True)
    else:
        st.warning(f"A aba {setor} parece estar vazia na planilha.")

except Exception as e:
    st.error(f"Erro ao conectar com {setor}")
    st.info("Verifique se a planilha ainda está com acesso liberado para 'Qualquer pessoa com o link'.")
