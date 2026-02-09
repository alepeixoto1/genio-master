import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# CONFIGURAÇÃO DA PÁGINA
# =====================================================
st.set_page_config(
    page_title="Gênio Master",
    layout="wide",
    page_icon="💎"
)

# =====================================================
# ESTILO CSS PROFISSIONAL (DARK MODE)
# =====================================================
st.markdown("""
<style>
    .stApp { background-color: #0f172a; color: white; }
    [data-testid="stSidebar"] { background-color: #1e293b; }
    
    .card {
        background: linear-gradient(135deg, #1e293b, #334155);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #38bdf8;
        text-align: center;
        margin-bottom: 10px;
    }
    .card-title { font-size: 12px; color: #94a3b8; text-transform: uppercase; font-weight: bold; }
    .card-value { font-size: 26px; font-weight: bold; color: white; margin-top: 5px; }
</style>
""", unsafe_allow_html=True)

# =====================================================
# CARREGAMENTO DE DADOS
# =====================================================
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"

def carregar(gid):
    try:
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip() # Remove espaços extras
        # Converte colunas numéricas (trocando vírgula por ponto se necessário)
        for col in ["Previsto", "Realizado", "Saving", "Performance", "Valor"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace('.', '').str.replace(',', '.'), errors='coerce')
        return df
    except:
        return pd.DataFrame()

df_fin = carregar("0")
df_ativos = carregar("1179272110")
df_esg = carregar("1026863401")
df_slas = carregar("2075740723")

# =====================================================
# MENU
# =====================================================
with st.sidebar:
    st.title("Gênio Master 💎")
    menu = st.radio("Menu Navigation", ["Dashboard", "Financeiro", "Ativos", "ESG", "SLAs"])

# =====================================================
# PÁGINAS
# =====================================================

# 1. DASHBOARD (Visão Geral)
if menu == "Dashboard":
    st.header("📊 Dashboard Executivo")
    
    c1, c2, c3 = st.columns(3)
    realizado = df_fin["Realizado"].sum() if "Realizado" in df_fin.columns else 0
    saving = df_fin["Saving"].sum() if "Saving" in df_fin.columns else 0
    total_ativos = len(df_ativos)

    c1.markdown(f'<div class="card"><div class="card-title">Realizado</div><div class="card-value">R$ {realizado:,.2f}</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="card"><div class="card-title">Saving</div><div class="card-value">R$ {saving:,.2f}</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="card"><div class="card-title">Ativos</div><div class="card-value">{total_ativos}</div></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.line(df_fin, x="Mês", y="Realizado", title="Tendência de Gastos", template="plotly_dark", markers=True)
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = px.pie(df_fin, names="Categoria", values="Realizado", hole=0.6, title="Distribuição por Categoria", template="plotly_dark")
        st.plotly_chart(fig2, use_container_width=True)

# 2. FINANCEIRO (Comparativo)
elif menu == "Financeiro":
    st.header("💰 Detalhamento Financeiro")
    st.dataframe(df_fin, use_container_width=True)
    
    # Gráfico de Barras Comparativo
    fig_fin = px.bar(df_fin, x="Mês", y=["Previsto", "Realizado"], barmode="group", 
                     title="Previsto vs Realizado por Mês", template="plotly_dark",
                     color_discrete_map={"Previsto": "#64748b", "Realizado": "#38bdf8"})
    st.plotly_chart(fig_fin, use_container_width=True)

# 3. ATIVOS (Inventário)
elif menu == "Ativos":
    st.header("📦 Gestão de Ativos")
    st.dataframe(df_ativos, use_container_width=True)
    
    if not df_ativos.empty:
        # Gráfico de Barras Simples (Diferente dos outros)
        fig_at = px.bar(df_ativos, x=df_ativos.columns[0], y=df_ativos.columns[-1] if len(df_ativos.columns)>1 else None,
                        title="Valor por Item", template="plotly_dark", color_discrete_sequence=['#fbbf24'])
        st.plotly_chart(fig_at, use_container_width=True)

# 4. ESG (Sustentabilidade)
elif menu == "ESG":
    st.header("🌱 Indicadores ESG")
    st.dataframe(df_esg, use_container_width=True)
    
    if not df_esg.empty:
        # Gráfico Funil ou Barras Horizontais para ESG
        fig_esg = px.bar(df_esg, x=df_esg.columns[-1], y=df_esg.columns[0], orientation='h',
                         title="Impacto das Iniciativas", template="plotly_dark", color_discrete_sequence=['#10b981'])
        st.plotly_chart(fig_esg, use_container_width=True)

# 5. SLAs (Performance)
elif menu == "SLAs":
    st.header("⏱️ Acordos de Nível de Serviço")
    st.dataframe(df_slas, use_container_width=True)
    
    if "Performance" in df_slas.columns:
        # Gráfico de Radar ou Área para SLAs
        fig_sla = px.area(df_slas, x="Mês" if "Mês" in df_slas.columns else df_slas.columns[0], 
                          y="Performance", title="Performance de SLA (%)", template="plotly_dark")
        st.plotly_chart(fig_sla, use_container_width=True)
