import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuração de Página Otimizada
st.set_page_config(
    page_title="Gênio Master Pro", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- CSS PROFISSIONAL (Mobile-First & Glassmorphism) ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');
    
    * {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
    .stApp {{ background-color: #0b0e14; }}
    
    /* Cards de Métricas Estilo Premium */
    div[data-testid="stMetric"] {{
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }}
    div[data-testid="stMetric"]:hover {{
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.04);
        border-color: rgba(255, 255, 255, 0.2);
    }}
    
    /* Ajustes de Títulos */
    h1, h2, h3 {{ color: #ffffff !important; letter-spacing: -0.5px; }}
    .stMarkdown p {{ color: #94a3b8; }}

    /* Customização da Tabela */
    .stDataFrame {{ 
        border: 1px solid rgba(255, 255, 255, 0.1); 
        border-radius: 12px; 
    }}

    /* Mobile Adjustments */
    @media (max-width: 768px) {{
        div[data-testid="stMetric"] {{ padding: 15px !important; }}
    }}
</style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO DE ACESSO ---
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"
CONFIG = {
    "Financeiro": {"gid": "0", "cor": "#34d399", "icon": "💰"},
    "Ativos": {"gid": "1179272110", "cor": "#60a5fa", "icon": "📦"},
    "Esg": {"gid": "1026863401", "cor": "#fb7185", "icon": "🌱"},
    "Slas": {"gid": "2075740723", "cor": "#fbbf24", "icon": "⏱️"}
}

with st.sidebar:
    st.markdown("<h2 style='font-size: 24px;'>💎 GÊNIO MASTER</h2>", unsafe_allow_html=True)
    st.markdown("---")
    setor = st.selectbox("Selecione o Módulo", list(CONFIG.keys()))
    st.markdown("<br>"*2, unsafe_allow_html=True)
    st.caption("v5.1 Premium Edition")
    st.caption("Inteligência em Facilities")

# --- LEITURA DE DADOS ---
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG[setor]['gid']}"

try:
    # Mantendo a lógica estável de pular 2 linhas
    df = pd.read_csv(url, skiprows=2).dropna(how='all', axis=1).dropna(how='all', axis=0)
    
    if not df.empty:
        # Título do Módulo
        st.markdown(f"## {CONFIG[setor]['icon']} {setor} Overview")
        st.markdown("Análise de indicadores e performance em tempo real.")
        
        # --- CARDS DE PERFORMANCE (KPIs) ---
        m1, m2, m3, m4 = st.columns(4)
        cols_num = df.select_dtypes(include=['number']).columns
        cols_txt = df.select_dtypes(include=['object']).columns

        with m1:
            st.metric("Total Registros", f"{len(df)}", delta="Ativos")
        with m2:
            val = df[cols_num[0]].sum() if len(cols_num) > 0 else 0
            st.metric("Volume Total", f"{val:,.0f}", delta="Mensal")
        with m3:
            st.metric("Disponibilidade", "100%", delta="Sync OK")
        with m4:
            st.metric("Sincronização", "Cloud", delta="Real-time")

        st.markdown("<br>", unsafe_allow_html=True)

        # --- GRÁFICOS PROFISSIONAIS ---
        c1, c2 = st.columns([1.3, 0.7])

        with c1:
            if len(cols_num) > 0:
                fig_area = px.area(
                    df, x=df.index, y=cols_num[0],
                    title="<b>TENDÊNCIA ACUMULADA</b>",
                    template="plotly_dark"
                )
                fig_area.update_traces(
                    line_color=CONFIG[setor]['cor'],
                    fillcolor=f"rgba{tuple(int(CONFIG[setor]['cor'].lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (0.2,)}"
                )
                fig_area.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=10, r=10, t=50, b=10),
                    xaxis=dict(showgrid=False), 
                    yaxis=dict(showgrid=False)
                )
                st.plotly_chart(fig_area, use_container_width=True, config={'displayModeBar': False})

        with c2:
            if len(cols_txt) > 0:
                fig_pie = px.pie(
                    df, names=cols_txt[0], hole=0.7,
                    title="<b>DISTRIBUIÇÃO</b>",
                    color_discrete_sequence=[CONFIG[setor]['cor'], "#1e293b", "#334155", "#475569"]
                )
                fig_pie.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', 
                    showlegend=False,
                    margin=dict(l=10, r=10, t=50, b=10)
                )
                fig_pie.update_traces(textinfo='percent', textposition='inside')
                st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False})

        # --- ANÁLISE DETALHADA ---
        st.markdown("#### 📊 Análise por Categoria")
        if len(cols_txt) > 0 and len(cols_num) > 0:
            fig_bar = px.bar(
                df, x=cols_num[0], y=cols_txt[0], 
                orientation='h',
                color_discrete_sequence=[CONFIG[setor]['cor']],
                template="plotly_dark"
            )
            fig_bar.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(showgrid=False), 
                yaxis=dict(showgrid=False)
            )
            st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

        # Tabela Expansível (Limpa no Mobile)
        with st.expander("🔍 Explorar Base de Dados Completa"):
            st.dataframe(df, use_container_width=True)

    else:
        st.info("Aguardando inserção de dados na planilha...")

except Exception as e:
    st.error(f"Sistema em atualização ou erro na planilha. Detalhe: {e}")
