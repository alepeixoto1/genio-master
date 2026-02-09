import streamlit as st
import pandas as pd
import plotly.express as px

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Dashboard Gênio Master",
    page_icon="💰",
    layout="wide"
)

# SIDEBAR
st.sidebar.title("🏠 Menu")
pagina = st.sidebar.selectbox(
    "Selecione:",
    ["📊 Dashboard", "📁 Financeiro", "⚙️ Configurações"]
)

# DADOS EXEMPLO
dados_linha = pd.DataFrame({
    "Mes": ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul"],
    "Valor": [120, 220, 350, 500, 800, 1200, 1800]
})

dados_pizza = pd.DataFrame({
    "Categoria": ["março", "abril", "maio", "junho", "julho"],
    "Valor": [21, 21, 15, 24, 20]
})

# DASHBOARD
if pagina == "📊 Dashboard":

    st.title("💰 Dashboard Gênio Master")

    # CARDS SUPERIORES
    col1, col2, col3 = st.columns(3)

    col1.metric("TOTAL REGISTROS", "310")
    col2.metric("VOLUME", "R$ 27.321,00")
    col3.metric("STATUS", "Online")

    st.divider()

    # GRÁFICOS
    col1, col2 = st.columns(2)

    # GRÁFICO DE LINHA
    fig_linha = px.line(
        dados_linha,
        x="Mes",
        y="Valor",
        title="Tendência Acumulada",
        markers=True
    )

    col1.plotly_chart(fig_linha, use_container_width=True)

    # GRÁFICO DE PIZZA
    fig_pizza = px.pie(
        dados_pizza,
        names="Categoria",
        values="Valor",
        title="Distribuição de Ativos",
        hole=0.5
    )

    col2.plotly_chart(fig_pizza, use_container_width=True)

    st.divider()

    col1, col2 = st.columns(2)

    if col1.button("Gerar Relatório"):
        st.success("Relatório gerado!")

    if col2.button("Exportar PDF"):
        st.success("PDF exportado!")


# FINANCEIRO
elif pagina == "📁 Financeiro":
    st.title("📁 Financeiro")
    st.write("Área financeira em construção")

# CONFIGURAÇÕES
elif pagina == "⚙️ Configurações":
    st.title("⚙️ Configurações")
    st.write("Área de configurações em construção")


