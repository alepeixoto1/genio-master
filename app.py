import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# CONFIGURAÇÃO E ESTILO (PADRÃO PREMIUM)
# =====================================================
st.set_page_config(page_title="Gênio Master", layout="wide", page_icon="💎")

st.markdown("""
<style>
    .stApp { background-color: #0f172a; color: white; }
    [data-testid="stSidebar"] { background-color: #1e293b; }
    .card {
        background: linear-gradient(135deg, #1e293b, #0f172a);
        padding: 20px; border-radius: 12px; border: 1px solid #38bdf8;
        text-align: center; margin-bottom: 15px;
    }
    .card-title { font-size: 11px; color: #94a3b8; text-transform: uppercase; }
    .card-value { font-size: 24px; font-weight: bold; color: #38bdf8; }
</style>
""", unsafe_allow_html=True)

# =====================================================
# CONEXÃO E LIMPEZA DE DADOS
# =====================================================
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"

def carregar_seguro(gid):
    try:
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        # Converte moedas e números brasileiros (1.500,00 -> 1500.00)
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    df[col] = pd.to_numeric(df[col].str.replace('.', '').str.replace(',', '.'), errors='ignore')
                except: pass
        return df
    except: return pd.DataFrame()

df_fin = carregar_seguro("0")
df_ativos = carregar_seguro("1179272110")
df_esg = carregar_seguro("1026863401")
df_slas = carregar_seguro("2075740723")

# =====================================================
# MENU LATERAL
# =====================================================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/625/625099.png", width=50)
    st.title("Gênio Master")
    menu = st.radio("Navegação", ["Dashboard", "Financeiro", "Ativos", "ESG", "SLAs"])

# =====================================================
# PÁGINAS COM GRÁFICOS DIFERENCIADOS
# =====================================================

# 1. DASHBOARD: VISÃO EXECUTIVA (CARTÕES + ROSCA)
if menu == "Dashboard":
    st.header("💎 Dashboard Executivo")
    c1, c2, c3 = st.columns(3)
    realizado = df_fin["Realizado"].sum() if "Realizado" in df_fin.columns else 0
    saving = df_fin["Saving"].sum() if "Saving" in df_fin.columns else 0
    
    c1.markdown(f'<div class="card"><div class="card-title">Realizado Total</div><div class="card-value">R$ {realizado:,.0f}</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="card"><div class="card-title">Saving Total</div><div class="card-value">R$ {saving:,.0f}</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="card"><div class="card-title">Itens Ativos</div><div class="card-value">{len(df_ativos)}</div></div>', unsafe_allow_html=True)

    st.subheader("Distribuição de Custos por Categoria")
    fig_dash = px.pie(df_fin, names="Categoria", values="Realizado", hole=0.7, template="plotly_dark", color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_dash, use_container_width=True)

# 2. FINANCEIRO: PERFORMANCE (GRÁFICO DE ÁREA/LINHA)
elif menu == "Financeiro":
    st.header("💰 Performance Financeira")
    st.dataframe(df_fin, use_container_width=True)
    
    st.subheader("Evolução Mensal: Realizado vs Saving")
    # Gráfico de Área para dar profundidade
    fig_fin = px.area(df_fin, x="Mês", y=["Realizado", "Saving"], template="plotly_dark", 
                      color_discrete_map={"Realizado": "#38bdf8", "Saving": "#10b981"},
                      line_shape="spline")
    st.plotly_chart(fig_fin, use_container_width=True)

# 3. ATIVOS: INVENTÁRIO (GRÁFICO DE BARRAS VERTICAIS)
elif menu == "Ativos":
    st.header("📦 Gestão de Ativos")
    st.dataframe(df_ativos, use_container_width=True)
    
    if not df_ativos.empty:
        st.subheader("Contagem de Ativos por Tipo")
        # Usamos barras verticais para diferenciar do financeiro
        fig_at = px.bar(df_ativos, x=df_ativos.columns[0], template="plotly_dark", color_discrete_sequence=['#fbbf24'])
        st.plotly_chart(fig_at, use_container_width=True)

# 4. ESG: IMPACTO (GRÁFICO DE BARRAS HORIZONTAIS)
elif menu == "ESG":
    st.header("🌱 Sustentabilidade (ESG)")
    st.dataframe(df_esg, use_container_width=True)
    
    if not df_esg.empty:
        st.subheader("Iniciativas e Impacto")
        # Barras horizontais para facilitar a leitura de nomes longos
        fig_esg = px.bar(df_esg, x=df_esg.columns[-1], y=df_esg.columns[0], orientation='h', 
                         template="plotly_dark", color_discrete_sequence=['#22c55e'])
        st.plotly_chart(fig_esg, use_container_width=True)

# 5. SLAs: DISPONIBILIDADE (TABELA + MÉTRICAS)
elif menu == "SLAs":
    st.header("⏱️ Níveis de Serviço (SLAs)")
    st.dataframe(df_slas, use_container_width=True)
    
    if not df_slas.empty:
        st.subheader("Status de Cumprimento")
        # Gráfico de Funil ou Barras Coloridas por Status
        fig_sla = px.bar(df_slas, x="Performance" if "Performance" in df_slas.columns else df_slas.columns[0], 
                         y="Serviço" if "Serviço" in df_slas.columns else df_slas.columns[0],
                         template="plotly_dark", color_discrete_sequence=['#ef4444'])
        st.plotly_chart(fig_sla, use_container_width=True)
