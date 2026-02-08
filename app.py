import streamlit as st
import pandas as pd
import plotly.express as px
import os

# CONFIGURAÇÃO DA PÁGINA (PADRÃO CORPORATIVO)
st.set_page_config(page_title="Gênio Master Pro", layout="wide", initial_sidebar_state="expanded")

# --- ESTILO CSS PARA MELHORAR O VISUAL ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; border-left: 5px solid #00ffcc; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE LOGIN ---
if "logado" not in st.session_state:
    st.title("🔒 Gênio Master")
    senha = st.text_input("Chave de Acesso Master:", type="password")
    if st.button("Acessar Painel"):
        if senha == "mestre2026":
            st.session_state["logado"] = True
            st.rerun()
        else:
            st.error("Senha incorreta. Acesso negado.")
    st.stop()

# --- CONFIGURAÇÃO DAS ABAS (GIDs) ---
# DICA: Verifique o número 'gid=' na URL de cada aba da sua planilha
config_abas = {
    "Financeiro": {"gid": "0", "cor": "#FFD700", "img": "header_financeiro.png"},
    "Ativos": {"gid": "1179272110", "cor": "#00CCFF", "img": "header_ativos.png"},
    "Esg": {"gid": "1026863401", "cor": "#00FF88", "img": "header_esg.png"},
    "Slas": {"gid": "2075740723", "cor": "#FF3366", "img": "header_slas.png"}
}

# --- MENU LATERAL ---
st.sidebar.title("🚀 Gênio Master 2026")
setor_selecionado = st.sidebar.selectbox("Navegação por Módulo", list(config_abas.keys()))
st.sidebar.divider()
st.sidebar.info(f"Módulo Ativo: {setor_selecionado}")

# --- CABEÇALHO VISUAL ---
img_path = config_abas[setor_selecionado]["img"]
if os.path.exists(img_path):
    st.image(img_path, use_container_width=True)
else:
    st.title(f"📊 Painel de {setor_selecionado}")

# --- CONEXÃO COM O GOOGLE SHEETS ---
# O ID abaixo é o que você forneceu: 1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4il3o
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4il3o"
GID = config_abas[setor_selecionado]["gid"]
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}"

try:
    # Tentativa de leitura dos dados
    df = pd.read_csv(URL)

    if not df.empty:
        # --- CAMADA DE KPIs ---
        st.subheader(f"Indicadores de Performance - {setor_selecionado}")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total de Registros", len(df))
        with col2:
            st.metric("Status da Conexão", "Online ✅")
        with col3:
            # Tenta somar a primeira coluna numérica que encontrar
            cols_num = df.select_dtypes(include=['number']).columns
            if len(cols_num) > 0:
                total_val = df[cols_num[0]].sum()
                st.metric(f"Total {cols_num[0]}", f"{total_val:,.2f}")
            else:
                st.metric("Métrica", "N/A")

        st.divider()

        # --- CAMADA DE GRÁFICOS ---
        c_left, c_right = st.columns(2)

        with c_left:
            # Gráfico de Distribuição (Usa a primeira coluna de texto)
            cols_txt = df.select_dtypes(include=['object']).columns
            if len(cols_txt) > 0:
                fig_pie = px.pie(df, names=cols_txt[0], hole=0.4, 
                                 color_discrete_sequence=[config_abas[setor_selecionado]["cor"]])
                fig_pie.update_layout(title="Distribuição Categórica")
                st.plotly_chart(fig_pie, use_container_width=True)

        with c_right:
            # Gráfico de Barras (Se houver números e texto)
            if len(cols_num) > 0 and len(cols_txt) > 0:
                fig_bar = px.bar(df, x=cols_txt[0], y=cols_num[0],
                                 color_discrete_sequence=[config_abas[setor_selecionado]["cor"]])
                fig_bar.update_layout(title="Análise Volumétrica")
                st.plotly_chart(fig_bar, use_container_width=True)

        # --- CAMADA DE DADOS ---
        with st.expander("🔍 Ver Detalhes da Planilha"):
            st.dataframe(df, use_container_width=True)

    else:
        st.warning(f"Atenção: A aba '{setor_selecionado}' está conectada, mas não contém dados.")

except Exception as e:
    st.error(f"⚠️ Erro de Conexão no Módulo {setor_selecionado}")
    st.write(f"Detalhes técnicos: {e}")
    st.info("Certifique-se de que a planilha está compartilhada como 'Qualquer pessoa com o link' e que o ID/GID está correto.")
