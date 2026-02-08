import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração de Alta Performance
st.set_page_config(page_title="Gênio Master Pro", layout="wide", initial_sidebar_state="expanded")

# --- CSS CUSTOMIZADO PARA ESTILO "APP NATIVO" ---
st.markdown("""
    <style>
    /* Fundo e Container */
    .stApp { background-color: #0E1117; }
    
    /* Estilização dos Cards de Métricas */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 15px 20px;
        border-radius: 12px;
        transition: transform 0.3s;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.08);
    }
    
    /* Ajuste de Títulos */
    h1, h2, h3 { font-family: 'Inter', sans-serif; font-weight: 700; }
    
    /* Melhoria na Tabela */
    .stDataFrame { border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- CONFIGURAÇÃO DE ACESSO ---
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"

CONFIG = {
    "Financeiro": {"gid": "0", "cor": "#00FFA3", "emoji": "💵"},
    "Ativos": {"gid": "1179272110", "cor": "#00B2FF", "emoji": "🏗️"},
    "Esg": {"gid": "1026863401", "cor": "#BF5AF2", "emoji": "🌱"},
    "Slas": {"gid": "2075740723", "cor": "#FF375F", "emoji": "📊"}
}

# --- MENU LATERAL REFINADO ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1055/1055644.png", width=80) # Ícone Genérico de Dashboard
    st.title("Gênio Master")
    st.markdown("---")
    setor = st.selectbox("Selecione o Módulo", list(CONFIG.keys()), format_func=lambda x: f"{CONFIG[x]['emoji']} {x}")
    st.markdown("---")
    st.caption("v2.0 - Atualizado em tempo real")

# --- BUSCA DE DADOS ---
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG[setor]['gid']}"

try:
    df = pd.read_csv(url, skiprows=2)
    df = df.dropna(how='all', axis=1).dropna(how='all', axis=0)

    # --- CABEÇALHO DO DASHBOARD ---
    st.markdown(f"<h1 style='color: {CONFIG[setor]['cor']}; margin-bottom: 0;'>{CONFIG[setor]['emoji']} Dashboard {setor}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: #808495;'>Gestão inteligente de indicadores para {setor.lower()}.</p>", unsafe_allow_html=True)
    
    if not df.empty:
        # --- LINHA 1: CARDS DE MÉTRICAS (KPIs) ---
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Total de Itens", len(df))
        with m2:
            # Tenta converter a última coluna em número para somar, se possível
            try:
                total_val = df.iloc[:, -1].astype(float).sum()
                st.metric("Valor Total", f"R$ {total_val:,.2f}")
            except:
                st.metric("Status", "Ativo ✅")
        with m3:
            st.metric("Módulo", setor)
        with m4:
            st.metric("Atualização", "Cloud Sync")

        st.markdown("<br>", unsafe_allow_html=True)

        # --- LINHA 2: GRÁFICOS ---
        col_graf_1, col_graf_2 = st.columns([1, 1])

        with col_graf_1:
            cols_texto = df.select_dtypes(include=['object']).columns
            if len(cols_texto) > 0:
                fig_pie = px.pie(
                    df, names=cols_texto[0], hole=0.7,
                    title="<b>Distribuição Percentual</b>",
                    color_discrete_sequence=[CONFIG[setor]["cor"], "#23272E", "#3E4451"]
                )
                fig_pie.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font_color="#808495", showlegend=True,
                    legend=dict(orientation="h", y=-0.1)
                )
                st.plotly_chart(fig_pie, use_container_width=True)

        with col_graf_2:
            cols_num = df.select_dtypes(include=['number']).columns
            if len(cols_texto) > 0 and len(cols_num) > 0:
                fig_bar = px.bar(
                    df, x=cols_num[0], y=cols_texto[0], orientation='h',
                    title=f"<b>Análise por {cols_texto[0]}</b>",
                    color_discrete_sequence=[CONFIG[setor]["cor"]]
                )
                fig_bar.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font_color="#808495", xaxis_title="", yaxis_title=""
                )
                fig_bar.update_xaxes(showgrid=False)
                fig_bar.update_yaxes(showgrid=False)
                st.plotly_chart(fig_bar, use_container_width=True)

        # --- LINHA 3: TABELA DETALHADA ---
        st.markdown("### 📋 Base de Dados Completa")
        # Estilizando a tabela para combinar com o dark mode
        st.dataframe(df, use_container_width=True)

    else:
        st.info("Aguardando inserção de dados na planilha...")

except Exception as e:
    st.error(f"⚠️ Erro de conexão: {e}")
