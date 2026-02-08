import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. Setup de Elite
st.set_page_config(page_title="Gênio Master Custom", layout="wide")

# CSS para cards e estilo Dark
st.markdown("""
<style>
    .stApp { background-color: #080a0f; }
    [data-testid="stMetric"] { background: rgba(255, 255, 255, 0.03); border-radius: 15px; border: 1px solid rgba(255, 255, 255, 0.1); }
</style>
""", unsafe_allow_html=True)

SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"
CONFIG = {
    "Financeiro": {"gid": "0", "cor": "#00FFA3", "icon": "💰"},
    "Ativos": {"gid": "1179272110", "cor": "#00B2FF", "icon": "📦"},
    "Esg": {"gid": "1026863401", "cor": "#BF5AF2", "icon": "🌱"},
    "Slas": {"gid": "2075740723", "cor": "#FF375F", "icon": "⏱️"}
}

with st.sidebar:
    st.title("💎 GÊNIO MASTER")
    setor = st.selectbox("Escolha o Módulo", list(CONFIG.keys()))

url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG[setor]['gid']}"

try:
    df = pd.read_csv(url, skiprows=2).dropna(how='all', axis=1).dropna(how='all', axis=0)
    cols_num = df.select_dtypes(include=['number']).columns
    cols_txt = df.select_dtypes(include=['object']).columns

    st.markdown(f"<h1 style='color: white;'>{CONFIG[setor]['icon']} {setor.upper()}</h1>", unsafe_allow_html=True)

    if not df.empty:
        # --- DEFINIÇÃO DE GRÁFICO POR ABA ---
        c1, c2 = st.columns([1.5, 1])

        with c1:
            if setor == "Financeiro":
                # GRÁFICO 1: Velocímetro (Gauge) de Performance Financeira
                meta = 10000 # Valor de exemplo
                atual = df[cols_num[0]].sum() if len(cols_num) > 0 else 0
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = atual,
                    title = {'text': "Volume Financeiro Acumulado", 'font': {'color': "white"}},
                    gauge = {'axis': {'range': [None, meta]}, 'bar': {'color': CONFIG[setor]['cor']}}
                ))
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
                st.plotly_chart(fig, use_container_width=True)

            elif setor == "Ativos":
                # GRÁFICO 2: Treemap (Ótimo para ver inventário/ativos)
                fig = px.treemap(df, path=[cols_txt[0]], values=cols_num[0] if len(cols_num) > 0 else None,
                                 color_discrete_sequence=[CONFIG[setor]['cor'], "#1c1f26"])
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

            elif setor == "Esg":
                # GRÁFICO 3: Sunburst (Impacto Circular)
                fig = px.sunburst(df, path=[cols_txt[0]], values=cols_num[0] if len(cols_num) > 0 else None,
                                  color_discrete_sequence=[CONFIG[setor]['cor'], "#3e4451"])
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

            elif setor == "Slas":
                # GRÁFICO 4: Área (Evolução de Tempo/Resposta)
                fig = px.area(df, x=df.index, y=cols_num[0] if len(cols_num) > 0 else None,
                              line_group=cols_txt[0] if len(cols_txt) > 0 else None)
                fig.update_traces(line_color=CONFIG[setor]['cor'], fillcolor=f"rgba{tuple(int(CONFIG[setor]['cor'].lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (0.3,)}")
                fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

        with c2:
            # Gráfico Auxiliar (Rosca Moderna para todos)
            if len(cols_txt) > 0:
                fig_donut = go.Figure(data=[go.Pie(labels=df[cols_txt[0]], values=df.index, hole=.8)])
                fig_donut.update_traces(marker=dict(colors=[CONFIG[setor]['cor'], '#1c1f26', '#2d323d']))
                fig_donut.update_layout(title="<b>RESUMO DE COMPOSIÇÃO</b>", paper_bgcolor='rgba(0,0,0,0)', template="plotly_dark", showlegend=False)
                st.plotly_chart(fig_donut, use_container_width=True)

        st.markdown("### 📋 Detalhamento dos Dados")
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar o módulo: {e}")
