import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da Página
st.set_page_config(page_title="Gênio Master 2026", layout="wide")

# --- ESTILO CSS PARA LOOK MODERNO ---
st.markdown("""
    <style>
    /* Fundo do App */
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    
    /* Customização dos Cards e Gráficos */
    div[data-testid="stMetric"] {
        background-color: #1E2130;
        border-radius: 15px;
        padding: 15px;
        border: 1px solid #31333F;
    }
    
    /* Botão de Menu Lateral */
    .css-1d391kg { background-color: #161B22; }
    
    /* Esconder o Menu padrão do Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 1. CONFIGURAÇÃO DA PLANILHA ---
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"

# Cores vibrantes estilo Dashboards Modernos
CONFIG = {
    "Financeiro": {"gid": "0", "cor": "#00FFA3"}, # Verde Neon
    "Ativos": {"gid": "1179272110", "cor": "#00B2FF"}, # Azul Cyan
    "Esg": {"gid": "1026863401", "cor": "#BF5AF2"}, # Roxo
    "Slas": {"gid": "2075740723", "cor": "#FF375F"}  # Rosa Red
}

# --- 2. MENU LATERAL ---
st.sidebar.title("🚀 Gênio Master")
st.sidebar.markdown("---")
setor = st.sidebar.selectbox("Módulo Ativo:", list(CONFIG.keys()))
st.sidebar.info("Atualização Automática")

# --- 3. DADOS E GRÁFICOS ---
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG[setor]['gid']}"

try:
    df = pd.read_csv(url, skiprows=2)
    df = df.dropna(how='all', axis=1).dropna(how='all', axis=0)

    # Header de Impacto
    st.markdown(f"<h1 style='text-align: center; color: {CONFIG[setor]['cor']};'>📊 {setor.upper()}</h1>", unsafe_allow_html=True)
    st.markdown("---")

    if not df.empty:
        # Colunas de Gráficos
        c1, c2 = st.columns(2)

        with c1:
            cols_texto = df.select_dtypes(include=['object']).columns
            if len(cols_texto) > 0:
                col_nome = cols_texto[0]
                # Gráfico de Rosca (Donut) com estilo moderno
                fig_pie = px.pie(
                    df, names=col_nome, hole=0.7,
                    color_discrete_sequence=[CONFIG[setor]["cor"], "#2D2D2D", "#4A4A4A"]
                )
                fig_pie.update_traces(textinfo='none', hoverinfo='label+percent')
                fig_pie.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color="white",
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2),
                    margin=dict(t=0, b=0, l=0, r=0)
                )
                # Centralizando texto dentro do Donut (HTML hack)
                st.plotly_chart(fig_pie, use_container_width=True)

        with c2:
            cols_num = df.select_dtypes(include=['float64', 'int64']).columns
            if len(cols_texto) > 0 and len(cols_num) > 0:
                # Gráfico de Barras Horizontais (Mais moderno que o vertical)
                fig_bar = px.bar(
                    df.head(10), x=cols_num[0], y=cols_texto[0],
                    orientation='h',
                    color_discrete_sequence=[CONFIG[setor]["cor"]]
                )
                fig_bar.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font_color="white",
                    xaxis_title="", yaxis_title="",
                    margin=dict(t=20, b=20, l=20, r=20)
                )
                fig_bar.update_xaxes(showgrid=False)
                fig_bar.update_yaxes(showgrid=False)
                st.plotly_chart(fig_bar, use_container_width=True)

        # Tabela Estilizada
        st.markdown("### 📋 Visão Detalhada")
        st.dataframe(df.style.background_gradient(cmap='Blues'), use_container_width=True)
            
    else:
        st.warning("Nenhum dado encontrado para este módulo.")

except Exception as e:
    st.error("Erro na conexão. Verifique o compartilhamento da planilha.")
