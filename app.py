import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIGURAÇÃO
st.set_page_config(
    page_title="Gênio Master Pro",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS
st.markdown("""
<style>
.stApp {
    background-color: #f4f6fb;
}

.genio-card {
    background: linear-gradient(135deg,#0f172a,#1e293b);
    border-radius:12px;
    padding:20px;
    color:white;
}
</style>
""", unsafe_allow_html=True)

# CONFIG PLANILHA
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"

CONFIG = {
    "Financeiro": {"gid": "0", "icon": "💰"},
    "Ativos": {"gid": "1179272110", "icon": "📦"},
    "Esg": {"gid": "1026863401", "icon": "🌱"},
    "Slas": {"gid": "2075740723", "icon": "⏱️"}
}

# MENU
setor = st.sidebar.selectbox(
    "Módulo",
    list(CONFIG.keys())
)

url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG[setor]['gid']}"

# TRY CORRETO
try:

    df = pd.read_csv(url, skiprows=2)

    df = df.dropna(how="all", axis=1)
    df = df.dropna(how="all", axis=0)

    if df.empty:

        st.warning("Sem dados disponíveis")

    else:

        st.title(f"Gênio Master • {setor}")

        # COLUNAS NUMÉRICAS
        cols_num = df.select_dtypes(include="number").columns

        # CARDS
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric("Total", len(df))

        with c2:
            if len(cols_num) > 0:
                st.metric("Volume", int(df[cols_num[0]].sum()))

        with c3:
            st.metric("Status", "Online")

        with c4:
            st.metric("Sistema", "Operacional")

        st.divider()

        # GRÁFICOS
        col1, col2 = st.columns(2)

        with col1:

            if len(cols_num) > 0:

                fig = px.area(
                    df,
                    x=df.index,
                    y=cols_num[0],
                    title="Tendência"
                )

                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                )

                st.plotly_chart(
                    fig,
                    width="stretch"
                )

        with col2:

            cols_txt = df.select_dtypes(include="object").columns

            if len(cols_txt) > 0:

                fig2 = px.pie(
                    df,
                    names=cols_txt[0],
                    hole=0.7,
                    title="Distribuição"
                )

                st.plotly_chart(
                    fig2,
                    width="stretch"
                )

# EXCEPT OBRIGATÓRIO
except Exception as e:

    st.error(f"Erro ao carregar dados: {e}")
