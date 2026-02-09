import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import base64

# -----------------------------------
# CONFIGURAÇÃO DA PÁGINA
# -----------------------------------

st.set_page_config(
    page_title="Gênio Master • Financeiro",
    page_icon="💰",
    layout="wide"
)

# -----------------------------------
# CSS PROFISSIONAL
# -----------------------------------

st.markdown("""
<style>

.main {
    background: linear-gradient(135deg, #0b1a3a 0%, #020617 100%);
}

.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.1);
}

.metric-title {
    font-size: 14px;
    color: #94a3b8;
}

.metric-value {
    font-size: 28px;
    font-weight: bold;
    color: white;
}

.title {
    font-size: 36px;
    font-weight: bold;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# DADOS EXEMPLO
# -----------------------------------

data = {
    "data": pd.date_range(start="2024-01-01", periods=5, freq="M"),
    "valor": [1000, 2500, 1800, 3200, 4100],
    "mes": ["março", "abril", "maio", "junho", "julho"]
}

df = pd.DataFrame(data)

# -----------------------------------
# HEADER
# -----------------------------------

st.markdown("# 💰 Gênio Master • Financeiro")

col1, col2, col3, col4 = st.columns(4)

col1.metric("TOTAL REGISTROS", len(df))
col2.metric("VOLUME", df["valor"].sum())
col3.metric("STATUS", "Online")
col4.metric("SYNC", "100%")

st.divider()

# -----------------------------------
# FILTROS
# -----------------------------------

st.subheader("Filtros")

mes = st.selectbox(
    "Selecionar mês",
    ["Todos"] + list(df["mes"].unique())
)

if mes != "Todos":
    df = df[df["mes"] == mes]

# -----------------------------------
# GRÁFICO 1 — LINHA MODERNA
# -----------------------------------

col1, col2 = st.columns(2)

with col1:

    fig = px.area(
        df,
        x="data",
        y="valor",
        title="Tendência Acumulada",
        template="plotly_dark"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white")
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# GRÁFICO 2 — DONUT
# -----------------------------------

with col2:

    fig2 = go.Figure(data=[go.Pie(
        labels=df["mes"],
        values=df["valor"],
        hole=.6
    )])

    fig2.update_layout(
        title="Distribuição",
        template="plotly_dark"
    )

    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------------
# BOTÃO GERAR RELATÓRIO
# -----------------------------------

st.divider()

col1, col2 = st.columns(2)

with col1:

    if st.button("📄 Gerar Relatório"):

        total = df["valor"].sum()

        st.success(f"""
        Relatório gerado com sucesso!

        Total: R$ {total:,.2f}
        Registros: {len(df)}
        """)

# -----------------------------------
# EXPORTAR CSV
# -----------------------------------

with col2:

    csv = df.to_csv(index=False).encode()

    st.download_button(
        "⬇ Exportar Dados",
        csv,
        "relatorio.csv",
        "text/csv"
    )

# -----------------------------------
# EXPORTAR PDF (SIMULAÇÃO)
# -----------------------------------

st.download_button(
    "⬇ Exportar PDF",
    csv,
    "relatorio.pdf",
    "application/pdf"
)


