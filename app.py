import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configurações de Design
st.set_page_config(page_title="Gênio Master Elite", layout="wide")

# CSS para fundo branco/claro se quiser seguir o modelo fiel, ou manter dark refinado
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; } /* Fundo leve para destacar as cores dos modelos */
    [data-testid="stMetric"] { background: white; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    h1, h2, p { color: #1e293b !important; }
</style>
""", unsafe_allow_html=True)

# --- CONEXÃO ---
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"
CONFIG = {
    "Financeiro": {"gid": "0", "colors": ["#f87171", "#34d399", "#60a5fa", "#fbbf24"]},
    "Ativos": {"gid": "1179272110", "colors": ["#818cf8", "#fb7185", "#34d399", "#94a3b8"]},
    "Esg": {"gid": "1026863401", "colors": ["#10b981", "#3b82f6", "#f59e0b", "#6366f1"]},
    "Slas": {"gid": "2075740723", "colors": ["#f43f5e", "#10b981", "#3b82f6", "#facc15"]}
}

setor = st.sidebar.selectbox("Módulo", list(CONFIG.keys()))
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG[setor]['gid']}"

try:
    df = pd.read_csv(url, skiprows=2).dropna(how='all', axis=1).dropna(how='all', axis=0)
    
    if not df.empty:
        st.markdown(f"## {setor} - Dashboard Profissional")
        st.caption("ANÁLISE DE PERFORMANCE E DISTRIBUIÇÃO OPERACIONAL")

        # Identificação automática de colunas
        cols_txt = df.select_dtypes(include=['object']).columns
        cols_num = df.select_dtypes(include=['number']).columns

        # --- MODELO 1: BARRAS EMPILHADAS (Estilo sd.PNG) ---
        if len(cols_txt) >= 2 and len(cols_num) > 0:
            st.markdown("### Status por Categoria")
            fig_bar = px.bar(df, 
                             y=cols_txt[0], 
                             x=cols_num[0], 
                             color=cols_txt[1] if len(cols_txt) > 1 else None,
                             orientation='h',
                             color_discrete_sequence=CONFIG[setor]['colors'],
                             barmode='stack')
            fig_bar.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                  legend=dict(orientation="h", y=-0.2))
            st.plotly_chart(fig_bar, use_container_width=True)

        # --- MODELO 2: ÁREA DE TENDÊNCIA (Estilo sds.PNG) ---
        if len(cols_num) > 0:
            st.markdown("### Tendência de Distribuição")
            fig_area = px.area(df, 
                               x=df.index, 
                               y=cols_num[0],
                               color=cols_txt[0] if len(cols_txt) > 0 else None,
                               color_discrete_sequence=CONFIG[setor]['colors'])
            fig_area.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                   legend=dict(orientation="h", y=-0.2))
            st.plotly_chart(fig_area, use_container_width=True)

        st.markdown("---")
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar estilo premium: {e}")
