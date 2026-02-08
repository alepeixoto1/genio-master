import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Configuração de Página
st.set_page_config(page_title="Gênio Master Pro", layout="wide", initial_sidebar_state="expanded")

# --- CSS PARA LIMPEZA VISUAL (Estilo Profissional) ---
st.markdown("""
<style>
    .stApp { background-color: #0e1117; }
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px;
    }
    .plot-container { border-radius: 12px; }
    h1, h2, h3 { color: white !important; font-family: 'Plus Jakarta Sans', sans-serif; }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO DE ACESSO ---
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"
CONFIG = {
    "Financeiro": {"gid": "0", "cor": "#34d399"},
    "Ativos": {"gid": "1179272110", "cor": "#60a5fa"},
    "Esg": {"gid": "1026863401", "cor": "#fb7185"},
    "Slas": {"gid": "2075740723", "cor": "#fbbf24"}
}

with st.sidebar:
    st.markdown("<h2 style='font-size: 22px;'>💎 GÊNIO MASTER</h2>", unsafe_allow_html=True)
    st.markdown("---")
    setor = st.selectbox("Escolha o Módulo", list(CONFIG.keys()))
    st.caption("v5.0 - Estabilidade Garantida")

# --- LEITURA DE DADOS ---
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG[setor]['gid']}"

try:
    # Lógica de 3 passos atrás: Pula as 2 primeiras linhas de título
    df = pd.read_csv(url, skiprows=2).dropna(how='all', axis=1).dropna(how='all', axis=0)
    
    if not df.empty:
        # Título e KPIs
        st.markdown(f"## {setor} Overview")
        
        m1, m2, m3, m4 = st.columns(4)
        cols_num = df.select_dtypes(include=['number']).columns
        cols_txt = df.select_dtypes(include=['object']).columns

        with m1: st.metric("Total Registros", len(df))
        with m2: 
            val = df[cols_num[0]].sum() if len(cols_num) > 0 else 0
            st.metric("Volume Total", f"{val:,.0f}")
        with m3: st.metric("Status", "Ativo", delta="Sync OK")
        with m4: st.metric("Update", "Real-time")

        st.markdown("<br>", unsafe_allow_html=True)

        # --- GRÁFICOS (Design de Alta Performance) ---
        c1, c2 = st.columns([1.2, 0.8])

        with c1:
            # Gráfico de Área (Igual ao modelo sds.PNG que você gostou)
            if len(cols_num) > 0:
                fig_area = px.area(df, x=df.index, y=cols_num[0],
                                   title="<b>TENDÊNCIA ACUMULADA</b>",
                                   template="plotly_dark",
                                   color_discrete_sequence=[CONFIG[setor]['cor']])
                fig_area.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                      margin=dict(l=0, r=10, t=40, b=0))
                st.plotly_chart(fig_area, use_container_width=True)

        with c2:
            # Gráfico de Rosca (Clean)
            if len(cols_txt) > 0:
                fig_pie = px.pie(df, names=cols_txt[0], hole=0.7,
                                 title="<b>DISTRIBUIÇÃO</b>",
                                 template="plotly_dark",
                                 color_discrete_sequence=[CONFIG[setor]['cor'], "#1c1f26", "#3e4451"])
                fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', showlegend=False,
                                     margin=dict(l=0, r=0, t=40, b=0))
                st.plotly_chart(fig_pie, use_container_width=True)

        # Gráfico de Barras Empilhadas (Estilo sd.PNG)
        st.markdown("#### Análise Detalhada por Categoria")
        if len(cols_txt) > 0 and len(cols_num) > 0:
            fig_bar = px.bar(df, x=cols_num[0], y=cols_txt[0], orientation='h',
                             color_discrete_sequence=[CONFIG[setor]['cor']],
                             template="plotly_dark")
            fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                                  xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
            st.plotly_chart(fig_bar, use_container_width=True)

        # Tabela Final
        with st.expander("🔍 Visualizar Base Completa"):
            st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar dados. Verifique a planilha. Detalhe: {e}")
