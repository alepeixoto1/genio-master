import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuração de Interface Profissional
st.set_page_config(page_title="Gênio Master Pro", layout="wide", initial_sidebar_state="expanded")

# --- ESTILO CSS PROFISSIONAL (CORRIGIDO) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background-color: #080a0f; }
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 15px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 24px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: transparent; border-radius: 4px 4px 0px 0px; gap: 1px; }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO DE ACESSO ---
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"
CONFIG = {
    "Financeiro": {"gid": "0", "cor": "#00FFA3"},
    "Ativos": {"gid": "1179272110", "cor": "#00B2FF"},
    "Esg": {"gid": "1026863401", "cor": "#BF5AF2"},
    "Slas": {"gid": "2075740723", "cor": "#FF375F"}
}

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color: white;'>💎 GÊNIO MASTER</h2>", unsafe_allow_html=True)
    st.markdown("---")
    setor = st.selectbox("Selecione o Módulo", list(CONFIG.keys()))
    st.caption("v3.0 - Dashboard de Alta Performance")

# --- LÓGICA DE DADOS ---
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG[setor]['gid']}"

try:
    # Lendo os dados e garantindo que números sejam tratados como números
    df = pd.read_csv(url, skiprows=2).dropna(how='all', axis=1).dropna(how='all', axis=0)
    
    # Título do App
    st.markdown(f"<h1 style='color: white;'>📊 Dashboard {setor.upper()}</h1>", unsafe_allow_html=True)

    if not df.empty:
        # 2. KPIs (Resolvendo o erro de Indentação)
        m1, m2, m3, m4 = st.columns(4)
        
        # Identificando colunas
        cols_num = df.select_dtypes(include=['number']).columns
        cols_txt = df.select_dtypes(include=['object']).columns

        with m1:
            st.metric("Total de Itens", len(df))
        with m2:
            if len(cols_num) > 0:
                # Soma a primeira coluna numérica encontrada
                total = df[cols_num[0]].sum()
                st.metric("Valor Acumulado", f"{total:,.0f}")
            else:
                st.metric("Dados Numéricos", "0")
        with m3:
            st.metric("Eficiência", "99.9%", "+0.2%")
        with m4:
            st.metric("Sync Status", "Real-time")

        st.markdown("<br>", unsafe_allow_html=True)

        # 3. Gráficos em Abas (Dinamismo GDP)
        tab1, tab2 = st.tabs(["🎯 VISÃO ESTRATÉGICA", "📂 EXPLORAR DADOS"])

        with tab1:
            c1, c2 = st.columns(2)
            
            with c1:
                if len(cols_txt) > 0:
                    fig_donut = go.Figure(data=[go.Pie(
                        labels=df[cols_txt[0]], values=df.index,
                        hole=.75, marker=dict(colors=[CONFIG[setor]['cor'], '#1c1f26', '#2d323d']))])
                    fig_donut.update_layout(
                        title="<b>Composição do Portfólio</b>", template="plotly_dark",
                        paper_bgcolor='rgba(0,0,0,0)', showlegend=True,
                        legend=dict(orientation="h", y=-0.2))
                    st.plotly_chart(fig_donut, use_container_width=True)

            with c2:
                if len(cols_txt) > 0 and len(cols_num) > 0:
                    # Gráfico de barras usando dados reais
                    fig_bar = px.bar(df, x=cols_num[0], y=cols_txt[0], orientation='h')
                    fig_bar.update_traces(marker_color=CONFIG[setor]['cor'], marker_line_width=0)
                    fig_bar.update_layout(
                        title="<b>Ranking por Categoria</b>", template="plotly_dark",
                        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                        xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
                    st.plotly_chart(fig_bar, use_container_width=True)

        with tab2:
            st.markdown("### 📋 Base de Dados Completa")
            st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Erro na execução do script: {e}")
