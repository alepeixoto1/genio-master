import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Configuração Profissional
st.set_page_config(page_title="Gênio Master Pro", layout="wide", initial_sidebar_state="collapsed")

# --- CSS PARA ESTILO CORPORATIVO ---
st.markdown("""
    <style>
    .metric-card {
        background-color: #1a1c23;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #00ffcc;
    }
    .stMetric { background-color: rgba(255,255,255,0.05); padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SISTEMA DE ACESSO ---
if "logado" not in st.session_state:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if os.path.exists("logo.png"): st.image("logo.png", width=250)
        st.title("Enterprise Login")
        senha = st.text_input("Credencial Master:", type="password")
        if st.button("Autenticar"):
            if senha == "mestre2026":
                st.session_state["logado"] = True
                st.rerun()
            else:
                st.error("Credencial Inválida")
    st.stop()

# --- ESTRUTURA DE DADOS ---
config = {
    "Financeiro": {"gid": "0", "img": "header_financeiro.png", "color": "#00d4ff"},
    "Ativos": {"gid": "1179272110", "img": "header_ativos.png", "color": "#70ff00"},
    "Esg": {"gid": "1026863401", "img": "header_esg.png", "color": "#00ff88"},
    "Slas": {"gid": "2075740723", "img": "header_slas.png", "color": "#ff3e3e"}
}

# --- BARRA LATERAL (FILTROS) ---
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png")
else:
    st.sidebar.markdown("## 💡 Gênio Master")

setor = st.sidebar.selectbox("Módulo", list(config.keys()))
st.sidebar.divider()
st.sidebar.subheader("Filtros de Gestão")
data_range = st.sidebar.date_input("Período")

# --- HEADER DINÂMICO ---
img_path = config[setor]["img"]
if os.path.exists(img_path):
    st.image(img_path, use_container_width=True)
else:
    st.title(f"🏢 Gestão de {setor}")

# --- CARREGAMENTO DE DADOS ---
try:
    # URL atualizada com o ID correto da sua planilha
    url = f"https://docs.google.com/spreadsheets/d/1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o/export?format=csv&gid={config[setor]['gid']}"
    df = pd.read_csv(url)

    # --- CAMADA 1: KPIS DE ALTO NÍVEL ---
    st.subheader("📌 Indicadores Críticos")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    
    with kpi1:
        st.metric("Total de Registros", len(df))
    with kpi2:
        # Tenta somar valores se houver coluna numérica, senão mostra o total de aptos únicos
        col_valor = df.select_dtypes(include=['number']).columns
        if len(col_valor) > 0:
            val = df[col_valor[0]].sum()
            st.metric("Volume Total", f"R$ {val:,.2f}")
        else:
            aptos = df['APT'].nunique() if 'APT' in df.columns else 0
            st.metric("Unidades Envolvidas", aptos)
            
    with kpi3:
        st.metric("Status Operacional", "100%", delta="Normal")
    with kpi4:
        st.metric("Alertas Ativos", "0", delta_color="inverse")

    st.divider()

    # --- CAMADA 2: DASHBOARDS GRÁFICOS ---
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("### 📊 Distribuição por Assunto")
        # Identifica a coluna de categorias (ex: Assunto)
        col_cat = 'Assunto' if 'Assunto' in df.columns else df.select_dtypes(include=['object']).columns[0]
        fig = px.pie(df, names=col_cat, hole=.4, color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(margin=dict(t=30, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.markdown("### 📈 Ocorrências por Torre")
        col_torre = 'Torre' if 'Torre' in df.columns else df.select_dtypes(include=['object']).columns[1]
        if col_torre in df.columns:
            df_counts = df[col_torre].value_counts().reset_index()
            fig_bar = px.bar(df_counts, x=col_torre, y='count', color_discrete_sequence=[config[setor]["color"]])
            fig_bar.update_layout(margin=dict(t=30, b=0, l=0, r=0))
            st.plotly_chart(fig_bar, use_container_width=True)

    # --- CAMADA 3: TABELA TÉCNICA ---
    with st.expander("🔍 Visualizar Base de Dados Completa"):
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Aguardando conexão com o módulo {setor}. Verifique se a planilha está publicada na web.")
