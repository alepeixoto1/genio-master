import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Setup de Interface (Focado em Clean Design)
st.set_page_config(page_title="Gênio Master Pro", layout="wide", initial_sidebar_state="collapsed")

# --- CSS ESTILO iMÓDULO (GRID & TILES) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #f0f2f6; } /* Fundo leve para destacar os cards */
    
    /* Estilização dos Cards (Tiles) */
    .tile-card {
        background-color: #07477e; /* Azul do modelo iMódulo */
        color: white;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        min-height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .tile-title { font-weight: 700; font-size: 1.2rem; margin-bottom: 5px; }
    .tile-subtitle { font-size: 0.9rem; opacity: 0.8; }
    .tile-icon { font-size: 2rem; margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO DE DADOS ---
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"
CONFIG = {
    "Financeiro": {"gid": "0", "cor": "#07477e", "icon": "📊"},
    "Ativos": {"gid": "1179272110", "cor": "#07477e", "icon": "📦"},
    "Esg": {"gid": "1026863401", "cor": "#07477e", "icon": "🌱"},
    "Slas": {"gid": "2075740723", "cor": "#07477e", "icon": "⏱️"}
}

# Cabeçalho Estilo App
col_logo, col_text = st.columns([1, 10])
with col_text:
    st.markdown(f"<h1 style='color: #333; margin-bottom: 0;'>Gênio Master</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #666;'>Unidade: 11654 - GESTÃO OPERACIONAL</p>", unsafe_allow_html=True)

# Menu de Seleção Superior (estilo Tabs do iMódulo)
setor = st.selectbox("Selecione o Módulo Ativo:", list(CONFIG.keys()))

url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG[setor]['gid']}"

try:
    df = pd.read_csv(url, skiprows=2).dropna(how='all', axis=1).dropna(how='all', axis=0)
    
    if not df.empty:
        # --- SISTEMA DE TILES (GRID) ---
        st.markdown("### Painel de Controle")
        
        # Grid 1: Indicadores Principais
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.markdown(f"""<div class='tile-card'>
                <div class='tile-icon'>🔍</div>
                <div>
                    <div class='tile-title'>Consultas</div>
                    <div class='tile-subtitle'>Verificar {len(df)} registros ativos no sistema.</div>
                </div>
            </div>""", unsafe_allow_html=True)
            
        with c2:
            val_total = df.select_dtypes(include=['number']).iloc[:, 0].sum() if not df.select_dtypes(include=['number']).empty else 0
            st.markdown(f"""<div class='tile-card'>
                <div class='tile-icon'>💰</div>
                <div>
                    <div class='tile-title'>Operações</div>
                    <div class='tile-subtitle'>Volume total identificado: {val_total:,.0f}</div>
                </div>
            </div>""", unsafe_allow_html=True)

        with c3:
            st.markdown(f"""<div class='tile-card'>
                <div class='tile-icon'>🔔</div>
                <div>
                    <div class='tile-title'>Notificações</div>
                    <div class='tile-subtitle'>Sincronização Cloud realizada com sucesso.</div>
                </div>
            </div>""", unsafe_allow_html=True)

        # --- SEÇÃO DE GRÁFICOS (Design Refinado) ---
        st.markdown("### Análise Estratégica")
        
        tab_vis, tab_data = st.tabs(["🖼️ Visualização", "📋 Dados Brutos"])
        
        with tab_vis:
            g1, g2 = st.columns([1.5, 1])
            with g1:
                # Gráfico de Área Estilo Clean
                fig = px.area(df, x=df.index, y=df.select_dtypes(include=['number']).columns[0],
                              template="simple_white", color_discrete_sequence=["#07477e"])
                fig.update_layout(margin=dict(l=0, r=0, t=20, b=0))
                st.plotly_chart(fig, use_container_width=True)
            
            with g2:
                # Donut Chart Clean
                fig_pie = px.pie(df, names=df.select_dtypes(include=['object']).columns[0], hole=0.6,
                                 color_discrete_sequence=["#07477e", "#336699", "#5c85ad"])
                fig_pie.update_layout(showlegend=False, margin=dict(l=0, r=0, t=20, b=0))
                st.plotly_chart(fig_pie, use_container_width=True)

        with tab_data:
            st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar o modo Tile: {e}")
