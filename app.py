import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuração de Página e Estilo Dark Premium
st.set_page_config(page_title="Gênio Master Elite", layout="wide", initial_sidebar_state="expanded")

# --- CSS AVANÇADO: EFEITO GLASSMORPHISM E NEON ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: radial-gradient(circle at top left, #1e222d, #0e1117);
    }
    
    /* Cards Estilo Glass */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }

    /* Títulos Neon */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(#eee, #333);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    
    /* Customização do Sidebar */
    section[data-testid="stSidebar"] {
        background-color: rgba(14, 17, 23, 0.8);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Tabelas Modernas */
    .stDataFrame {
        border-radius: 15px;
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÃO ---
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"
CONFIG = {
    "Financeiro": {"gid": "0", "cor": "#00FFA3", "grad": "Emerald"},
    "Ativos": {"gid": "1179272110", "cor": "#00B2FF", "grad": "Sky"},
    "Esg": {"gid": "1026863401", "cor": "#BF5AF2", "grad": "Purple"},
    "Slas": {"gid": "2075740723", "cor": "#FF375F", "grad": "Sunset"}
}

# --- SIDEBAR DINÂMICO ---
with st.sidebar:
    st.markdown("<h2 style='letter-spacing: -1px;'>💎 GÊNIO MASTER</h2>", unsafe_allow_html=True)
    st.markdown("---")
    setor = st.selectbox("Navegação Principal", list(CONFIG.keys()))
    st.markdown("<br><br>"*5, unsafe_allow_html=True)
    st.caption("Intelligence System © 2026")

# --- LÓGICA DE DADOS ---
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG[setor]['gid']}"

try:
    df = pd.read_csv(url, skiprows=2).dropna(how='all', axis=1).dropna(how='all', axis=0)
    
    # Cabeçalho Dinâmico
    st.markdown(f"<p style='color:{CONFIG[setor]['cor']}; font-weight:bold; margin-bottom:-15px;'>MÓDULO EXECUTIVO</p>", unsafe_allow_html=True)
    st.markdown(f"<h1 class='main-title'>{setor.upper()}</h1>", unsafe_allow_html=True)
    
    if not df.empty:
        # 1. KPIs com Design de "Dashboard de Luxo"
        cols = st.columns(4)
        metrica_valor = len(df)
        
        with cols[0]:
            st.metric("Total de Registros", f"{metrica_valor}", delta="Ativo")
        with cols[1]:
            st.metric("Sincronização", "Cloud G-Drive", delta="100%")
        with cols[2]:
            st.metric("Performance", "Excelente", delta="98.2%")
        with cols[3]:
            st.metric("Mês de Referência", "Fevereiro")

        st.markdown("<br>", unsafe_allow_html=True)

        # 2. Gráficos com "Efeito de Profundidade"
        c1, c2 = st.columns([1.2, 1])

        with c1:
            # Gráfico de Barras com Gradiente (Plotly Objects para mais controle)
            cols_texto = df.select_dtypes(include=['object']).columns
            cols_num = df.select_dtypes(include=['number']).columns
            
            if len(cols_texto) > 0 and len(cols_num) > 0:
                fig_bar = go.Figure(go.Bar(
                    x=df[cols_num[0]], y=df[cols_texto[0]],
                    orientation='h',
                    marker=dict(color=CONFIG[setor]['cor'], line=dict(color=CONFIG[setor]['cor'], width=1))
                ))
                fig_bar.update_layout(
                    title=f"<b>Ranking de {cols_texto[0]}</b>",
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showgrid=False),
                    yaxis=dict(showgrid=False)
                )
                st.plotly_chart(fig_bar, use_container_width=True)

        with c2:
            # Gráfico de Rosca com Legenda Centralizada
            if len(cols_texto) > 0:
                fig_donut = px.pie(
                    df, names=cols_texto[0], hole=0.8,
                    color_discrete_sequence=[CONFIG[setor]['cor'], "#1f2937", "#374151", "#4b5563"]
                )
                fig_donut.update_layout(
                    title="<b>Composição Relativa</b>",
                    template="plotly_dark",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    legend=dict(orientation="h", y=-0.1)
                )
                fig_donut.update_traces(textinfo='none')
                st.plotly_chart(fig_donut, use_container_width=True)

        # 3. Área de Dados "Limpa"
        with st.expander("🔍 EXPLORAR BASE DE DADOS BRUTA"):
            st.dataframe(df.style.set_properties(**{'background-color': '#161b22', 'color': 'white', 'border-color': '#30363d'}), use_container_width=True)

    else:
        st.warning("Base de dados detectada, mas sem registros válidos.")

except Exception as e:
    st.error(f"Sistema em manutenção ou link quebrado. Erro: {e}")
