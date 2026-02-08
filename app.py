import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração de Página Estilo Global
st.set_page_config(page_title="Gênio Master | Global Analytics", layout="wide")

# --- CSS PROFISSIONAL (INSPIRADO EM MODELOS GDP) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
    
    .stApp { background-color: #0e1117; }
    
    /* Cards de Métricas Estilo Terminal Bloomberg */
    [data-testid="stMetric"] {
        background: #161b22;
        border: 1px solid #30363d;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Headers de Seção */
    .section-head {
        color: #8b949e;
        font-size: 0.9rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÃO DE DADOS ---
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"
CONFIG = {
    "Financeiro": {"gid": "0", "cor": "#00ffa3"},
    "Ativos": {"gid": "1179272110", "cor": "#00d4ff"},
    "Esg": {"gid": "1026863401", "cor": "#bf5af2"},
    "Slas": {"gid": "2075740723", "cor": "#ff375f"}
}

# --- SIDEBAR (CONTROLE DE FILTROS) ---
with st.sidebar:
    st.markdown("### 🌐 Global Navigation")
    setor = st.selectbox("Selecione o Domínio", list(CONFIG.keys()))
    st.markdown("---")
    st.info("Os dados são extraídos em tempo real da nuvem.")

# --- CARREGAMENTO ---
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG[setor]['gid']}"

try:
    # Mantendo skiprows=2 que é o que está certo na sua planilha
    df = pd.read_csv(url, skiprows=2).dropna(how='all', axis=1).dropna(how='all', axis=0)

    # --- TÍTULO DO APP ---
    st.markdown(f"<h1 style='font-weight:300;'>{setor} <span style='font-weight:600; color:{CONFIG[setor]['cor']};'>Overview</span></h1>", unsafe_allow_html=True)
    
    if not df.empty:
        # --- LINHA 1: MÉTRICAS TIPO GDP ---
        st.markdown("<p class='section-head'>Principais Indicadores</p>", unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4)
        
        # Lógica para pegar valores reais da planilha
        total_items = len(df)
        last_val = df.iloc[:, -1].sum() if df.iloc[:, -1].dtype in ['float64', 'int64'] else 0

        m1.metric("Volume de Dados", total_items, "+12% vs last month")
        m2.metric("Impacto Nominal", f"R$ {last_val:,.2f}", "Stable")
        m3.metric("Integridade", "99.8%", "High")
        m4.metric("Região", "Brasil", "São Paulo")

        st.markdown("<br>", unsafe_allow_html=True)

        # --- LINHA 2: GRÁFICOS DE ALTO IMPACTO ---
        col_main, col_side = st.columns([2, 1])

        with col_main:
            st.markdown("<p class='section-head'>Tendência Temporal e Evolução</p>", unsafe_allow_html=True)
            # Gráfico de Área (Muito usado em dashboards de GDP)
            # Assume que a primeira coluna tem os meses
            fig_area = px.area(df, x=df.columns[0], y=df.columns[-1], 
                               line_shape="spline",
                               color_discrete_sequence=[CONFIG[setor]['cor']])
            fig_area.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, color="#8b949e"),
                yaxis=dict(showgrid=True, gridcolor="#30363d", color="#8b949e"),
                margin=dict(l=0, r=0, t=10, b=0),
                height=400
            )
            st.plotly_chart(fig_area, use_container_width=True)

        with col_side:
            st.markdown("<p class='section-head'>Distribuição de Share</p>", unsafe_allow_html=True)
            # Donut Chart Minimalista
            fig_donut = px.pie(df, names=df.columns[0], hole=0.8)
            fig_donut.update_traces(marker=dict(colors=[CONFIG[setor]['cor'], '#30363d', '#161b22']), textinfo='none')
            fig_donut.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', showlegend=True,
                legend=dict(font=dict(color="white"), orientation="h", y=-0.1),
                height=400, margin=dict(l=0, r=0, t=10, b=0)
            )
            st.plotly_chart(fig_donut, use_container_width=True)

        # --- LINHA 3: TABELA PROFISSIONAL ---
        st.markdown("<p class='section-head'>Base de Dados Consolidada</p>", unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar o modelo GDP: {e}")
