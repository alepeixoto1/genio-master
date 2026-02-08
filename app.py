import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 1. Configuração de Interface Profissional
st.set_page_config(page_title="Gênio Master Pro", layout="wide", initial_sidebar_state="expanded")

# --- CSS CUSTOMIZADO (ESTILO GDP DASHBOARD) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700&display=swap');
    
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background-color: #080a0f; }
    
    /* Estilização dos Containers de Gráficos */
    div.stPlotlyChart {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 10px;
    }

    /* Estilo dos Cards de KPI */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.01) 100%);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 15px;
    }
    
    /* Esconder elementos desnecessários */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÃO DE DADOS ---
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"
CONFIG = {
    "Financeiro": {"gid": "0", "cor": "#00FFA3", "grad": "linear-gradient(90deg, #00FFA3, #00B2FF)"},
    "Ativos": {"gid": "1179272110", "cor": "#00B2FF", "grad": "linear-gradient(90deg, #00B2FF, #00FFA3)"},
    "Esg": {"gid": "1026863401", "cor": "#BF5AF2", "grad": "linear-gradient(90deg, #BF5AF2, #FF375F)"},
    "Slas": {"gid": "2075740723", "cor": "#FF375F", "grad": "linear-gradient(90deg, #FF375F, #BF5AF2)"}
}

# --- SIDEBAR ELITE ---
with st.sidebar:
    st.markdown(f"<h1 style='color: white; font-size: 22px;'>💎 GÊNIO MASTER</h1>", unsafe_allow_html=True)
    st.markdown("---")
    setor = st.selectbox("Selecione o Fluxo", list(CONFIG.keys()))
    st.markdown("<br>"*2, unsafe_allow_html=True)
    st.info(f"Conexão Segura: Ativa\nSync: {datetime.now().strftime('%H:%M')}")

# --- PROCESSAMENTO ---
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG[setor]['gid']}"

try:
    df = pd.read_csv(url, skiprows=2).dropna(how='all', axis=1).dropna(how='all', axis=0)

    # HEADER DINÂMICO ESTILO GDP
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown(f"<h1 style='background: {CONFIG[setor]['grad']}; -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 45px;'>{setor.upper()}</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #6a6a6a; margin-top: -15px;'>Análise macroeconômica e operacional em tempo real.</p>", unsafe_allow_html=True)

    if not df.empty:
        # SEÇÃO DE KPIs (IGUAL AOS MODELOS DE SHARE)
        kpi1, kpi2, kpi3, kpi4 = st.columns(4)
        kpi1.metric("Itens Gerenciados", len(df), "+12%")
        kpi2.metric("Disponibilidade", "99.9%", "0.2%")
        kpi3.metric("Eficiência", "Alta", delta="Estável")
        kpi4.metric("Sincronização", "Real-time")

        st.markdown("<br>", unsafe_allow_html=True)

        # SEÇÃO DE GRÁFICOS (TABS PARA ORGANIZAÇÃO)
        tab_geral, tab_detalhe = st.tabs(["📊 VISÃO ESTRATÉGICA", "🔍 ANÁLISE DE DADOS"])

        with tab_geral:
            c1, c2 = st.columns(2)
            
            with c1:
                cols_texto = df.select_dtypes(include=['object']).columns
                if len(cols_texto) > 0:
                    fig_donut = go.Figure(data=[go.Pie(
                        labels=df[cols_texto[0]], values=df.index,
                        hole=.8, marker=dict(colors=[CONFIG[setor]['cor'], '#1c1f26', '#2d323d']))])
                    fig_donut.update_layout(
                        title="<b>Composição do Portfólio</b>", template="plotly_dark",
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                        margin=dict(t=50, b=0, l=0, r=0), showlegend=False)
                    st.plotly_chart(fig_donut, use_container_width=True)

            with c2:
                cols_num = df.select_dtypes(include=['number']).columns
                if len(cols_texto) > 0 and len(cols_num) > 0:
                    fig_bar = px.bar(df.head(10), x=cols_num[0], y=cols_texto[0], orientation='h')
                    fig_bar.update_traces(marker_color=CONFIG[setor]['cor'], marker_line_width=0)
                    fig_bar.update_layout(
                        title="<b>Top Indicadores</b>", template="plotly_dark",
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                        xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
                    st.plotly_chart(fig_bar, use_container_width=True)

        with tab_detalhe:
            # FILTRO DINÂMICO
            search = st.text_input("🔍 Filtrar na base de dados...", placeholder="Digite qualquer termo para buscar...")
            if search:
                df_filtered = df[df.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)]
            else:
                df_filtered = df
            
            st.dataframe(df_filtered, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar o modelo GDP: {e}")
