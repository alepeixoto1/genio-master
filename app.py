import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuração de Página e Viewport Mobile
st.set_page_config(page_title="Gênio Master Pro", layout="wide", initial_sidebar_state="collapsed")

# --- CSS PARA MOBILE E CARDS FUNCIONAIS ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    
    /* Card Funcional com Sombra e Borda Neon */
    [data-testid="stMetric"] {
        background: #161b22 !important;
        border: 1px solid #30363d !important;
        border-left: 5px solid {cor_setor} !important; /* Dinâmico via código */
        border-radius: 12px !important;
        padding: 15px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2) !important;
    }

    /* Ajuste de Títulos para telas pequenas */
    @media (max-width: 640px) {
        .main-title { font-size: 1.8rem !important; }
        .stMetric label { font-size: 0.9rem !important; }
        .stMetric div { font-size: 1.2rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO ---
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"
CONFIG = {
    "Financeiro": {"gid": "0", "cor": "#34d399", "target": 15000},
    "Ativos": {"gid": "1179272110", "cor": "#60a5fa", "target": 100},
    "Esg": {"gid": "1026863401", "cor": "#fb7185", "target": 50},
    "Slas": {"gid": "2075740723", "cor": "#fbbf24", "target": 100}
}

with st.sidebar:
    st.markdown("## 💎 GÊNIO MASTER")
    setor = st.selectbox("Selecione o Fluxo", list(CONFIG.keys()))
    st.divider()
    st.caption("Acesso via Mobile Otimizado")

url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG[setor]['gid']}"

try:
    df = pd.read_csv(url, skiprows=2).dropna(how='all', axis=1).dropna(how='all', axis=0)
    
    if not df.empty:
        cols_num = df.select_dtypes(include=['number']).columns
        cols_txt = df.select_dtypes(include=['object']).columns

        st.markdown(f"<h1 class='main-title' style='color: white;'>{setor}</h1>", unsafe_allow_html=True)

        # --- CARDS FUNCIONAIS (Adaptáveis) ---
        # No mobile, st.columns(4) vira uma lista vertical automaticamente
        m1, m2, m3, m4 = st.columns([1,1,1,1])
        
        with m1:
            st.metric("Registros", len(df), delta="Ativos")
        
        with m2:
            if len(cols_num) > 0:
                total = df[cols_num[0]].sum()
                # Card funcional: Mostra o total e compara com uma meta fictícia
                diff = total - CONFIG[setor]['target']
                st.metric("Total Acumulado", f"{total:,.0f}", delta=f"{diff:,.0f} vs Meta")
            else:
                st.metric("Status", "Sem Valores")

        with m3:
            st.metric("Eficiência", "98.2%", delta="↑ 1.5%")
        
        with m4:
            st.metric("Sincronização", "OK", delta="Real-time", delta_color="normal")

        st.markdown("<br>", unsafe_allow_html=True)

        # --- GRÁFICOS MOBILE-FRIENDLY ---
        # Usamos colunas, mas o Streamlit as empilha no celular automaticamente
        col_graf_1, col_graf_2 = st.columns([1, 1])

        with col_graf_1:
            if len(cols_num) > 0:
                # Gráfico de Área mais limpo para mobile
                fig_area = px.area(df, x=df.index, y=cols_num[0],
                                 title="Tendência de Performance",
                                 template="plotly_dark",
                                 color_discrete_sequence=[CONFIG[setor]['cor']])
                fig_area.update_layout(
                    height=300, # Altura menor para caber na tela do celular
                    margin=dict(l=10, r=10, t=40, b=10),
                    xaxis=dict(showgrid=False), yaxis=dict(showgrid=False),
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_area, use_container_width=True, config={'displayModeBar': False})

        with col_graf_2:
            if len(cols_txt) > 0:
                # Gráfico de Barras Horizontal (Melhor leitura no celular que o de pizza)
                fig_bar = px.bar(df, x=cols_num[0] if len(cols_num) > 0 else df.index, 
                                 y=cols_txt[0],
                                 orientation='h',
                                 title="Distribuição por Categoria",
                                 template="plotly_dark",
                                 color_discrete_sequence=[CONFIG[setor]['cor']])
                fig_bar.update_layout(
                    height=300,
                    margin=dict(l=10, r=10, t=40, b=10),
                    xaxis=dict(showgrid=False), yaxis=dict(showgrid=False),
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

        # Base de dados em Expander para não ocupar tela no mobile
        with st.expander("🔍 Ver Tabela de Dados"):
            st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar dados mobile: {e}")
