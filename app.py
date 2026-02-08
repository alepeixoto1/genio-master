import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Gênio Master Spectacular", layout="wide")

# --- ESTILO CSS PROFISSIONAL ---
st.markdown("""
    <style>
    .stApp { background: #0b0e14; }
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.02);
        border-left: 5px solid #00FFA3;
        border-radius: 10px;
    }
    .plot-container { border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.5); }
    </style>
    """, unsafe_allow_html=True)

SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"
CONFIG = {
    "Financeiro": {"gid": "0", "cor": "#00FFA3", "sec": "#004d31"},
    "Ativos": {"gid": "1179272110", "cor": "#00B2FF", "sec": "#003a54"},
    "Esg": {"gid": "1026863401", "cor": "#BF5AF2", "sec": "#411f52"},
    "Slas": {"gid": "2075740723", "cor": "#FF375F", "sec": "#5e1423"}
}

setor = st.sidebar.selectbox("Dashboard", list(CONFIG.keys()))
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG[setor]['gid']}"

try:
    df = pd.read_csv(url, skiprows=2).dropna(how='all', axis=1).dropna(how='all', axis=0)
    
    st.markdown(f"<h1 style='text-align: left; color: white;'>{setor} <span style='color:{CONFIG[setor]['cor']}'>Insight</span></h1>", unsafe_allow_html=True)

    if not df.empty:
        # --- TOP KPIs ---
        m1, m2, m3 = st.columns(3)
        m1.metric("Volume Total", f"{len(df)} itens")
        m2.metric("Status", "Operacional", delta="100%")
        m3.metric("Última Sync", "Agora")

        st.write("---")

        # --- GRÁFICOS ESPETACULARES ---
        c1, c2 = st.columns([1, 1])

        with c1:
            # Gráfico de Rosca com Efeito de Anel Moderno
            cols_texto = df.select_dtypes(include=['object']).columns
            if len(cols_texto) > 0:
                fig_donut = go.Figure(data=[go.Pie(
                    labels=df[cols_texto[0]], 
                    values=df.index, # Ou substitua por coluna numérica se houver
                    hole=.75,
                    marker=dict(colors=[CONFIG[setor]['cor'], CONFIG[setor]['sec'], '#1c1f26', '#2d323d'],
                                line=dict(color='#0b0e14', width=3))
                )])
                fig_donut.update_layout(
                    title=dict(text="<b>DISTRIBUIÇÃO ESTRATÉGICA</b>", font=dict(color="white", size=18)),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    showlegend=True,
                    legend=dict(font=dict(color="white"), orientation="h", y=-0.2)
                )
                st.plotly_chart(fig_donut, use_container_width=True)

        with c2:
            # Gráfico de Barras Estilizado com Bordas Arredondadas
            cols_num = df.select_dtypes(include=['number']).columns
            if len(cols_texto) > 0 and len(cols_num) > 0:
                fig_bar = px.bar(
                    df.sort_values(by=cols_num[0], ascending=True).tail(8), 
                    x=cols_num[0], y=cols_texto[0],
                    orientation='h',
                    template="plotly_dark"
                )
                fig_bar.update_traces(
                    marker_color=CONFIG[setor]['cor'],
                    marker_line_color=CONFIG[setor]['cor'],
                    marker_line_width=1, opacity=0.9
                )
                fig_bar.update_layout(
                    title=dict(text="<b>RANKING DE PERFORMANCE</b>", font=dict(color="white", size=18)),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis=dict(showgrid=False, zeroline=False),
                    yaxis=dict(showgrid=False)
                )
                st.plotly_chart(fig_bar, use_container_width=True)

        # --- ÁREA DINÂMICA (TABELA) ---
        st.markdown("### 💎 Detalhamento Premium")
        st.table(df.head(10)) # Table simples fica muito elegante em dark mode

except Exception as e:
    st.error(f"Erro ao conectar com os dados: {e}")
