import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuração de Interface
st.set_page_config(page_title="Gênio Master Pro", layout="wide", initial_sidebar_state="expanded")

# --- CSS DEFINITIVO (SEM ERROS) ---
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
    .stTabs [data-baseweb="tab"] { color: white; }
</style>
""", unsafe_allow_html=True)

# --- ACESSO ---
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
    st.info("Sistema Conectado via Cloud")

# --- LÓGICA DE DADOS ---
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG[setor]['gid']}"

try:
    # Lendo pulando as 2 linhas de título da sua planilha
    df = pd.read_csv(url, skiprows=2).dropna(how='all', axis=1).dropna(how='all', axis=0)
    
    st.markdown(f"<h1 style='color: white;'>📊 Dashboard {setor}</h1>", unsafe_allow_html=True)

    if not df.empty:
        # 2. KPIs COM ALINHAMENTO CORRIGIDO
        m1, m2, m3, m4 = st.columns(4)
        
        # Detecta automaticamente colunas para não haver erro de nome
        cols_num = df.select_dtypes(include=['number']).columns
        cols_txt = df.select_dtypes(include=['object']).columns

        with m1:
            st.metric("Total de Registros", len(df))
        with m2:
            if len(cols_num) > 0:
                # Soma a primeira coluna de valores que ele achar
                val_total = df[cols_num[0]].sum()
                st.metric("Volume Acumulado", f"{val_total:,.0f}")
            else:
                st.metric("Volume", "---")
        with m3:
            st.metric("Status", "Operacional", delta="Normal")
        with m4:
            st.metric("Sync", "Real-time")

        st.markdown("<br>", unsafe_allow_html=True)

        # 3. GRÁFICOS PERSONALIZADOS POR ABA
        tab1, tab2 = st.tabs(["🎯 ANÁLISE VISUAL", "📋 TABELA DE DADOS"])

        with tab1:
            c1, c2 = st.columns([1, 1])
            
            with c1:
                if len(cols_txt) > 0:
                    # Gráfico de Rosca moderno
                    fig_pie = px.pie(df, names=cols_txt[0], hole=0.7,
                                   color_discrete_sequence=[CONFIG[setor]['cor'], '#1c1f26', '#3e4451'])
                    fig_pie.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
                    st.plotly_chart(fig_pie, use_container_width=True)

            with c2:
                if len(cols_txt) > 0 and len(cols_num) > 0:
                    # Gráfico de Barras - Aqui ele vai usar os valores REAIS da sua planilha
                    fig_bar = px.bar(df, x=cols_num[0], y=cols_txt[0], orientation='h',
                                   color_discrete_sequence=[CONFIG[setor]['cor']])
                    fig_bar.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', 
                                        xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
                    st.plotly_chart(fig_bar, use_container_width=True)
                else:
                    st.warning("Adicione números na planilha para ver o gráfico de barras.")

        with tab2:
            st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
