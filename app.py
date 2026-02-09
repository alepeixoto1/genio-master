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
# ESTILO CSS CUSTOMIZADO (DARK MODE)
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
    .card-title { font-size: 12px; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; }
    .card-value { font-size: 24px; font-weight: bold; color: white; margin-top: 5px; }
</style>
""", unsafe_allow_html=True)

# =====================================================
# FUNÇÃO DE CARREGAMENTO (GOOGLE SHEETS)
# =====================================================
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"

def carregar_dados(gid):
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")
    return df

# Cache dos dados
df_fin = carregar_dados("0")
df_ativos = carregar_dados("1179272110")
df_esg = carregar_dados("1026863401")
df_slas = carregar_dados("2075740723")

# =====================================================
# SIDEBAR / MENU
# =====================================================
with st.sidebar:
    st.title("Gênio Master 💎")
    menu = st.radio("Selecione a página:", ["Dashboard", "Financeiro", "Ativos", "ESG", "SLAs"])

# =====================================================
# COMPONENTE DE CARDS (KPIs GLOBAIS)
# =====================================================
def mostrar_cards():
    realizado = df_fin["Realizado"].sum() if "Realizado" in df_fin else 0
    saving = df_fin["Saving"].sum() if "Saving" in df_fin else 0
    ativos_total = len(df_ativos)
    
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f'<div class="card"><div class="card-title">Realizado</div><div class="card-value">R$ {realizado:,.0f}</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="card"><div class="card-title">Saving</div><div class="card-value">R$ {saving:,.0f}</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="card"><div class="card-title">Ativos</div><div class="card-value">{ativos_total}</div></div>', unsafe_allow_html=True)

# =====================================================
# LÓGICA DAS PÁGINAS
# =====================================================

if menu == "Dashboard":
    st.header("📊 Dashboard Executivo")
    mostrar_cards()
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.line(df_fin, x="Mês", y="Realizado", title="Evolução Mensal", template="plotly_dark", markers=True)
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = px.pie(df_fin, names="Categoria", values="Realizado", hole=0.5, title="Distribuição por Categoria", template="plotly_dark")
        st.plotly_chart(fig2, use_container_width=True)

elif menu == "Financeiro":
    st.header("💰 Gestão Financeira")
    mostrar_cards()
    st.divider()
    st.dataframe(df_fin, use_container_width=True)
    fig_bar = px.bar(df_fin, x="Mês", y=["Previsto", "Realizado"], barmode="group", title="Previsto vs Realizado", template="plotly_dark")
    st.plotly_chart(fig_bar, use_container_width=True)

elif menu == "Ativos":
    st.header("📦 Inventário de Ativos")
    st.info(f"Total de ativos catalogados: {len(df_ativos)}")
    st.dataframe(df_ativos, use_container_width=True)
    if "Status" in df_ativos.columns:
        fig_ativos = px.treemap(df_ativos, path=['Status', 'Tipo'], values='Valor' if 'Valor' in df_ativos else None, template="plotly_dark")
        st.plotly_chart(fig_ativos, use_container_width=True)

elif menu == "ESG":
    st.header("🌱 Indicadores ESG")
    st.markdown("### Impacto Socioambiental")
    if "Impacto" in df_esg.columns:
        fig_esg = px.bar(df_esg, x="Valor", y="Iniciativa", orientation='h', color="Impacto", title="Iniciativas por Impacto", template="plotly_dark")
        st.plotly_chart(fig_esg, use_container_width=True)
    st.dataframe(df_esg, use_container_width=True)

elif menu == "SLAs":
    st.header("⏱️ Níveis de Serviço (SLAs)")
    cols = st.columns(len(df_slas))
    for i, row in df_slas.iterrows():
        cols[i].metric(label=row['Serviço'], value=f"{row['Performance']}%", delta=f"{row['Status']}")
    st.divider()
    st.table(df_slas)
