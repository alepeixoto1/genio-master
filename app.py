import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# =====================================
# CONFIG
# =====================================

st.set_page_config(
    page_title="Gênio Master Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================
# CSS PROFISSIONAL
# =====================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(180deg,#0f172a,#020617);
    color: white;
}

.card {
    background: #111827;
    padding:20px;
    border-radius:12px;
    border:1px solid #1f2937;
}

.sidebar .sidebar-content {
    background: #020617;
}

</style>
""", unsafe_allow_html=True)

# =====================================
# MENU
# =====================================

pagina = st.sidebar.radio(
    "Menu",
    [
        "📊 Financeiro",
        "📦 Ativos",
        "🌱 ESG",
        "⏱️ SLAs",
        "📄 Relatórios",
        "⚙️ Configurações"
    ]
)

# =====================================
# GOOGLE SHEETS CONFIG
# =====================================

SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"

CONFIG = {
    "Financeiro": "0",
    "Ativos": "1179272110",
    "Esg": "1026863401",
    "Slas": "2075740723"
}

# =====================================
# FUNÇÃO LOAD DATA
# =====================================

@st.cache_data(ttl=60)
def load_data(setor):

    gid = CONFIG[setor]

    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"

    df = pd.read_csv(url, skiprows=2)

    df = df.dropna(how="all")

    return df

# =====================================
# RELATÓRIOS
# =====================================

if pagina == "📄 Relatórios":

    st.title("Central de Relatórios")

    setor = st.selectbox(
        "Selecionar módulo",
        list(CONFIG.keys())
    )

    df = load_data(setor)

    col1, col2 = st.columns(2)

    with col1:

        csv = df.to_csv(index=False).encode()

        st.download_button(
            "Exportar CSV",
            csv,
            file_name="relatorio.csv"
        )

    with col2:

        excel = df.to_excel("temp.xlsx", index=False)

        with open("temp.xlsx", "rb") as f:

            st.download_button(
                "Exportar Excel",
                f,
                file_name="relatorio.xlsx"
            )

    st.stop()

# =====================================
# CONFIGURAÇÕES
# =====================================

if pagina == "⚙️ Configurações":

    st.title("Configurações")

    st.toggle("Modo escuro", True)

    st.stop()

# =====================================
# DEFINIR SETOR
# =====================================

if pagina == "📊 Financeiro":
    setor = "Financeiro"

elif pagina == "📦 Ativos":
    setor = "Ativos"

elif pagina == "🌱 ESG":
    setor = "Esg"

elif pagina == "⏱️ SLAs":
    setor = "Slas"

# =====================================
# LOAD DATA
# =====================================

df = load_data(setor)

# =====================================
# HEADER
# =====================================

st.title(f"Gênio Master • {setor}")

# =====================================
# CARDS
# =====================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "TOTAL",
    len(df)
)

col2.metric(
    "COLUNAS",
    len(df.columns)
)

col3.metric(
    "STATUS",
    "Online"
)

col4.metric(
    "SYNC",
    "100%"
)

# =====================================
# GRÁFICOS
# =====================================

col1, col2 = st.columns(2)

numeric = df.select_dtypes("number").columns

text = df.select_dtypes("object").columns

if len(numeric) > 0:

    with col1:

        fig = px.area(
            df,
            y=numeric[0],
            title="Tendência"
        )

        fig.update_layout(
            template="plotly_dark",
            height=400
        )

        st.plotly_chart(fig, width="stretch")

if len(text) > 0:

    with col2:

        fig2 = px.pie(
            df,
            names=text[0],
            hole=0.7,
            title="Distribuição"
        )

        fig2.update_layout(
            template="plotly_dark",
            height=400
        )

        st.plotly_chart(fig2, width="stretch")

# =====================================
# TABELA
# =====================================

st.subheader("Dados")

st.dataframe(
    df,
    width="stretch",
    height=400
)

# =====================================
# EXPORT
# =====================================

csv = df.to_csv(index=False).encode()

st.download_button(
    "Exportar CSV",
    csv,
    file_name="dados.csv"
)

