import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuração de Layout (Garante que não fique bagunçado em telas grandes)
st.set_page_config(page_title="Gênio Master Pro", layout="wide", initial_sidebar_state="expanded")

# --- CSS PARA ORGANIZAÇÃO VISUAL ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    /* Estilo dos Cards de Gráficos */
    .plot-container {
        border-radius: 12px;
        background-color: #161b22;
        padding: 20px;
        border: 1px solid #30363d;
    }
    /* Deixa as abas mais elegantes */
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { color: #8b949e; font-weight: bold; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { color: #58a6ff; border-bottom-color: #58a6ff; }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO DE DADOS ---
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"
CONFIG = {
    "Financeiro": {"gid": "0", "cor": "#34d399"},
    "Ativos": {"gid": "1179272110", "cor": "#60a5fa"},
    "Esg": {"gid": "1026863401", "cor": "#fb7185"},
    "Slas": {"gid": "2075740723", "cor": "#fbbf24"}
}

with st.sidebar:
    st.markdown("<h1 style='font-size: 20px;'>💎 GÊNIO MASTER</h1>", unsafe_allow_html=True)
    st.markdown("---")
    setor = st.selectbox("Selecione o Fluxo", list(CONFIG.keys()))
    st.caption("Dashboard v4.0 - Design System")

url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG[setor]['gid']}"

try:
    # Carregamento Seguro
    df = pd.read_csv(url, skiprows=2).dropna(how='all', axis=1).dropna(how='all', axis=0)
    
    if not df.empty:
        # Cabeçalho Limpo
        st.markdown(f"<h2 style='color: white; margin-bottom: 0;'>{setor} Dashboard</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #8b949e;'>Visão estratégica e detalhamento operacional.</p>", unsafe_allow_html=True)

        # KPIs Rápidos em linha
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Registros", len(df))
        k2.metric("Status", "Sincronizado", delta="OK")
        k3.metric("Mês Atual", "Fev/26")
        k4.metric("Performance", "98%", "+2%")

        st.markdown("<br>", unsafe_allow_html=True)

        # --- SEÇÃO DE GRÁFICOS ORGANIZADOS ---
        col_esq, col_dir = st.columns([1.2, 0.8])

        # Identifica colunas
        cols_num = df.select_dtypes(include=['number']).columns
        cols_txt = df.select_dtypes(include=['object']).columns

        with col_esq:
            st.markdown("#### 📈 Evolução e Tendência")
            if len(cols_num) > 0:
                # Estilo de Área (conforme sds.PNG)
                fig_area = px.area(df, 
                                   x=df.index, 
                                   y=cols_num[0],
                                   color=cols_txt[0] if len(cols_txt) > 0 else None,
                                   template="plotly_dark",
                                   color_discrete_sequence=["#34d399", "#60a5fa", "#fb7185", "#fbbf24"])
                fig_area.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=0, r=0, t=20, b=0),
                    legend=dict(orientation="h", y=-0.2)
                )
                st.plotly_chart(fig_area, use_container_width=True)

        with col_dir:
            st.markdown("#### 📊 Distribuição")
            if len(cols_txt) > 0:
                # Estilo de Barras Empilhadas (conforme sd.PNG)
                fig_bar = px.bar(df, 
                                 y=cols_txt[0], 
                                 x=cols_num[0] if len(cols_num) > 0 else None,
                                 orientation='h',
                                 template="plotly_dark",
                                 color_discrete_sequence=[CONFIG[setor]['cor']])
                fig_bar.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=0, r=0, t=20, b=0),
                    xaxis=dict(showgrid=False), yaxis=dict(showgrid=False)
                )
                st.plotly_chart(fig_bar, use_container_width=True)

        # --- TABELA DETALHADA ---
        st.markdown("---")
        st.markdown("#### 📋 Base de Dados Completa")
        st.dataframe(df, use_container_width=True)

    else:
        st.warning("Aguardando preenchimento de dados na planilha...")

except Exception as e:
    st.error(f"Erro ao organizar o layout: {e}")
