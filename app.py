import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# CONFIGURAÇÃO E ESTILO (LIGHT MODE)
# =====================================================
st.set_page_config(page_title="Gênio Master", layout="wide", page_icon="💎")

st.markdown("""
<style>
    /* Fundo claro e fontes escuras */
    .stApp { background-color: #f8fafc; color: #1e293b; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
    
    /* Cards Claros com Sombra Suave */
    .card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    .card-title { font-size: 13px; color: #64748b; font-weight: 600; text-transform: uppercase; }
    .card-value { font-size: 28px; font-weight: 800; color: #0f172a; margin-top: 8px; }
    
    /* Ajuste de títulos Streamlit para modo claro */
    h1, h2, h3 { color: #0f172a !important; font-weight: 700 !important; }
</style>
""", unsafe_allow_html=True)

# =====================================================
# FUNÇÃO DE CARREGAMENTO SEGURO
# =====================================================
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"

def carregar(gid):
    try:
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        # Limpeza de números brasileiros
        for col in ["Previsto", "Realizado", "Saving", "Performance"]:
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
# MENU LATERAL
# =====================================================
with st.sidebar:
    st.title("💎 Gênio Master")
    menu = st.radio("Navegação", ["Dashboard", "Financeiro", "Ativos", "ESG", "SLAs"])

# =====================================================
# LÓGICA DAS PÁGINAS (GRÁFICOS EXCLUSIVOS)
# =====================================================

# 1. DASHBOARD: CARTÕES + ROSCA
if menu == "Dashboard":
    st.title("📊 Resumo Executivo")
    
    c1, c2, c3 = st.columns(3)
    realizado = df_fin["Realizado"].sum() if "Realizado" in df_fin.columns else 0
    saving = df_fin["Saving"].sum() if "Saving" in df_fin.columns else 0
    
    c1.markdown(f'<div class="card"><div class="card-title">Realizado</div><div class="card-value">R$ {realizado:,.0f}</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="card"><div class="card-title">Saving</div><div class="card-value">R$ {saving:,.0f}</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="card"><div class="card-title">Ativos</div><div class="card-value">{len(df_ativos)}</div></div>', unsafe_allow_html=True)

    st.subheader("Distribuição por Categoria")
    fig_pie = px.pie(df_fin, names="Categoria", values="Realizado", hole=0.5, template="plotly_white", color_discrete_sequence=px.colors.qualitative.Safe)
    st.plotly_chart(fig_pie, use_container_width=True)

# 2. FINANCEIRO: GRÁFICO DE BARRAS AGRUPADAS
elif menu == "Financeiro":
    st.title("💰 Gestão Financeira")
    st.dataframe(df_fin, use_container_width=True)
    
    st.subheader("Comparativo Mensal: Orçado vs Gasto")
    fig_bar = px.bar(df_fin, x="Mês", y=["Previsto", "Realizado"], barmode="group", template="plotly_white", color_discrete_map={"Previsto": "#94a3b8", "Realizado": "#3b82f6"})
    st.plotly_chart(fig_bar, use_container_width=True)

# 3. ATIVOS: GRÁFICO DE ÁREA
elif menu == "Ativos":
    st.title("📦 Inventário de Ativos")
    st.dataframe(df_ativos, use_container_width=True)
    
    st.subheader("Evolução de Ativos")
    # Gráfico de área para ser diferente dos outros
    fig_area = px.area(df_ativos, x=df_ativos.columns[0], y=df_ativos.columns[-1] if len(df_ativos.columns)>1 else None, template="plotly_white", color_discrete_sequence=['#8b5cf6'])
    st.plotly_chart(fig_area, use_container_width=True)

# 4. ESG: BARRAS HORIZONTAIS
elif menu == "ESG":
    st.title("🌱 Painel ESG")
    st.dataframe(df_esg, use_container_width=True)
    
    st.subheader("Impacto das Iniciativas")
    # Gráfico horizontal
    fig_esg = px.bar(df_esg, x=df_esg.columns[-1], y=df_esg.columns[0], orientation='h', template="plotly_white", color_discrete_sequence=['#10b981'])
    st.plotly_chart(fig_esg, use_container_width=True)

# 5. SLAs: GRÁFICO DE LINHAS COM MARCADORES
elif menu == "SLAs":
    st.title("⏱️ Monitoramento de SLAs")
    st.dataframe(df_slas, use_container_width=True)
    
    if "Performance" in df_slas.columns:
        st.subheader("Performance por Serviço")
        fig_line = px.line(df_slas, x="Mês" if "Mês" in df_slas.columns else df_slas.columns[0], y="Performance", markers=True, template="plotly_white", color_discrete_sequence=['#f43f5e'])
        st.plotly_chart(fig_line, use_container_width=True)
