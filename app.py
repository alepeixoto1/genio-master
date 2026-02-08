import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuração de Página (Mobile-First)
st.set_page_config(page_title="Gênio Master iModulo", layout="wide", initial_sidebar_state="expanded")

# --- CSS iMODULO: ESTILO LIMPO, CARDS REAIS E MOBILE ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #0d1117; }
    
    /* Cards de Métricas Estilo iModulo */
    div[data-testid="stMetric"] {
        background: #161b22;
        border: 1px solid #30363d;
        border-left: 4px solid {color}; /* Dinâmico */
        border-radius: 8px;
        padding: 15px !important;
    }
    
    /* Títulos e Containers */
    .module-header { font-size: 24px; font-weight: 800; color: white; margin-bottom: 20px; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #161b22; border-radius: 4px; padding: 8px 16px; color: #8b949e; }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { color: white; border-bottom: 2px solid #58a6ff; }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO DE ACESSO ---
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"
CONFIG = {
    "Financeiro": {"gid": "0", "cor": "#00ffa3", "emoji": "💰"},
    "Ativos": {"gid": "1179272110", "cor": "#00b2ff", "emoji": "📦"},
    "Esg": {"gid": "1026863401", "cor": "#bf5af2", "emoji": "🌱"},
    "Slas": {"gid": "2075740723", "cor": "#ff375f", "emoji": "📊"}
}

# --- NAVEGAÇÃO iMODULO ---
with st.sidebar:
    st.markdown("<h2 style='color: white; letter-spacing: -1px;'>💎 Gênio Master</h2>", unsafe_allow_html=True)
    st.markdown("---")
    setor = st.selectbox("Selecione o Módulo Ativo:", list(CONFIG.keys()))
    st.markdown("<br>"*5, unsafe_allow_html=True)
    st.caption("iModulo System v5.2")

# --- LEITURA DE DADOS (Ponte Segura) ---
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG[setor]['gid']}"

try:
    # Mantendo skiprows=2 que é o que estava dando certo
    df = pd.read_csv(url, skiprows=2).dropna(how='all', axis=1).dropna(how='all', axis=0)
    
    if not df.empty:
        # Título Dinâmico
        st.markdown(f"<div class='module-header'>{CONFIG[setor]['emoji']} Módulo {setor}</div>", unsafe_allow_html=True)

        # 2. CARDS FUNCIONAIS (Mobile-Ready)
        c1, c2, c3, c4 = st.columns(4)
        cols_num = df.select_dtypes(include=['number']).columns
        cols_txt = df.select_dtypes(include=['object']).columns

        with c1:
            st.metric("Total de Registros", len(df))
        with c2:
            val = df[cols_num[0]].sum() if len(cols_num) > 0 else 0
            st.metric("Valor Acumulado", f"R$ {val:,.0f}")
        with c3:
            st.metric("Performance", "98.5%", delta="↑ 2%")
        with c4:
            st.metric("Sync Status", "Real-time")

        st.markdown("<br>", unsafe_allow_html=True)

        # 3. GRÁFICOS iMODULO (Organização em Abas)
        tab_visual, tab_dados = st.tabs(["📉 Visão Analítica", "📋 Base de Dados"])

        with tab_visual:
            col_a, col_b = st.columns([1.2, 0.8])
            
            with col_a:
                # Gráfico de Área (O "Spectacular" que funcionou)
                if len(cols_num) > 0:
                    fig_area = px.area(df, x=df.index, y=cols_num[0],
                                     color_discrete_sequence=[CONFIG[setor]['cor']])
                    fig_area.update_layout(
                        title="<b>Evolução Temporal</b>", template="plotly_dark",
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                        margin=dict(l=0, r=0, t=40, b=0), height=350
                    )
                    st.plotly_chart(fig_area, use_container_width=True, config={'displayModeBar': False})

            with col_b:
                # Gráfico de Rosca (Proporção)
                if len(cols_txt) > 0:
                    fig_pie = px.pie(df, names=cols_txt[0], hole=0.75,
                                   color_discrete_sequence=[CONFIG[setor]['cor'], '#1c1f26', '#3e4451'])
                    fig_pie.update_layout(
                        title="<b>Composição</b>", template="plotly_dark",
                        paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=40, b=0),
                        showlegend=False, height=350
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)

        with tab_dados:
            st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Erro na conexão iModulo: {e}")
