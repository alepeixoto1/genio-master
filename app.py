import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da Página
st.set_page_config(page_title="Gênio Master 2026", layout="wide")

# --- 1. CONFIGURAÇÃO DA PLANILHA ---
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"

CONFIG = {
    "Financeiro": {"gid": "0", "cor": "#636EFA"},
    "Ativos": {"gid": "1179272110", "cor": "#EF553B"},
    "Esg": {"gid": "1026863401", "cor": "#00CC96"}, 
    "Slas": {"gid": "2075740723", "cor": "#AB63FA"}
}

# --- 2. MENU LATERAL ---
st.sidebar.title("🚀 Gênio Master")
setor = st.sidebar.selectbox("Escolha o Módulo", list(CONFIG.keys()))

# --- 3. DADOS E GRÁFICOS ---
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG[setor]['gid']}"

try:
    df = pd.read_csv(url, skiprows=2)
    df = df.dropna(how='all', axis=1).dropna(how='all', axis=0)

    st.title(f"📊 Dashboard {setor}")

    if not df.empty:
        # Criando duas colunas para os gráficos ficarem lado a lado
        col1, col2 = st.columns(2)

        with col1:
            # GRÁFICO 1: ROSCA (DONUT)
            cols_texto = df.select_dtypes(include=['object']).columns
            if len(cols_texto) > 0:
                col_nome = cols_texto[0]
                fig_pie = px.pie(
                    df, names=col_nome, 
                    hole=0.5, # Deixa o furo no meio (estilo Donut)
                    title=f"<b>Distribuição: {col_nome}</b>",
                    color_discrete_sequence=[CONFIG[setor]["cor"], "#333d44", "#9ca3af"]
                )
                fig_pie.update_layout(showlegend=True)
                st.plotly_chart(fig_pie, use_container_width=True)

        with col2:
            # GRÁFICO 2: BARRAS
            # Tenta usar a primeira coluna de texto no X e a primeira numérica no Y
            cols_num = df.select_dtypes(include=['float64', 'int64']).columns
            if len(cols_texto) > 0 and len(cols_num) > 0:
                fig_bar = px.bar(
                    df, x=cols_texto[0], y=cols_num[0],
                    title=f"<b>Valores por {cols_texto[0]}</b>",
                    color_discrete_sequence=[CONFIG[setor]["cor"]]
                )
                fig_bar.update_layout(plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_bar, use_container_width=True)
            else:
                st.info("Adicione números na planilha para ver o gráfico de barras.")

        # Tabela simplificada embaixo
        with st.expander("Ver dados da planilha"):
            st.dataframe(df, use_container_width=True)
            
    else:
        st.warning("Aba vazia.")

except Exception as e:
    st.error("Erro ao carregar. Verifique o compartilhamento da planilha.")
