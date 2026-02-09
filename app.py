import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# CONFIGURAÇÃO DA PÁGINA (ESTILO CLEAN)
# =====================================================
st.set_page_config(page_title="Gênio Master", layout="wide", page_icon="💎")

st.markdown("""
<style>
    .stApp { background-color: #f8fafc; color: #1e293b; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e2e8f0; }
    
    h1, h2, h3, p, span, label { color: #0f172a !important; }

    .card {
        background: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .card-title { font-size: 13px; color: #64748b; font-weight: 600; text-transform: uppercase; }
    .card-value { font-size: 28px; font-weight: 700; color: #2563eb; margin-top: 5px; }
</style>
""", unsafe_allow_html=True)

# =====================================================
# CONEXÃO COM PLANILHA (TRATAMENTO DE DADOS BR)
# =====================================================
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"

def carregar(gid):
    try:
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        # Converte formatos brasileiros (1.500,00 -> 1500.0)
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
    st.markdown("## 💎 Gênio Master")
    menu = st.radio("Selecione o Painel:", ["Dashboard Geral", "Financeiro", "Ativos", "ESG", "SLAs"])

# =====================================================
# PÁGINAS CORRIGIDAS
# =====================================================

# 1. DASHBOARD GERAL: Cartões + Gráfico de Rosca
if menu == "Dashboard Geral":
    st.title("📊 Painel Executivo")
    c1, c2, c3 = st.columns(3)
    realizado = df_fin["Realizado"].sum() if "Realizado" in df_fin.columns else 0
    saving = df_fin["Saving"].sum() if "Saving" in df_fin.columns else 0
    
    c1.markdown(f'<div class="card"><div class="card-title">Realizado</div><div class="card-value">R$ {realizado:,.0f}</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="card"><div class="card-title">Saving</div><div class="card-value">R$ {saving:,.0f}</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="card"><div class="card-title">Itens Ativos</div><div class="card-value">{len(df_ativos)}</div></div>', unsafe_allow_html=True)

    fig1 = px.pie(df_fin, names="Categoria", values="Realizado", hole=0.6, title="Distribuição de Custos", color_discrete_sequence=px.colors.qualitative.Safe)
    fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#1e293b", title_x=0.5)
    st.plotly_chart(fig1, use_container_width=True)

# 2. FINANCEIRO: Gráfico de Barras Agrupadas
elif menu == "Financeiro":
    st.title("💰 Detalhamento de Verba")
    st.dataframe(df_fin, use_container_width=True)
    
    fig2 = px.bar(df_fin, x="Mês", y=["Previsto", "Realizado"], barmode="group", title="Análise Mensal: Orçado x Gasto", color_discrete_map={"Previsto": "#cbd5e1", "Realizado": "#3b82f6"})
    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#1e293b", xaxis_title="")
    st.plotly_chart(fig2, use_container_width=True)

# 3. ATIVOS: Gráfico de Área (Volume)
elif menu == "Ativos":
    st.title("📦 Inventário de Ativos")
    st.dataframe(df_ativos, use_container_width=True)
    
    if not df_ativos.empty:
        fig3 = px.area(df_ativos, x=df_ativos.columns[0], y=df_ativos.columns[-1], title="Evolução de Ativos em Estoque", color_discrete_sequence=['#8b5cf6'])
        fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#1e293b")
        st.plotly_chart(fig3, use_container_width=True)

# 4. ESG: Gráfico de Barras Horizontais
elif menu == "ESG":
    st.title("🌱 Performance Sustentável")
    st.dataframe(df_esg, use_container_width=True)
    
    if not df_esg.empty:
        fig4 = px.bar(df_esg, x=df_esg.columns[-1], y=df_esg.columns[0], orientation='h', title="Impacto por Iniciativa", color_discrete_sequence=['#10b981'])
        fig4.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#1e293b")
        st.plotly_chart(fig4, use_container_width=True)

# 5. SLAs: Gráfico de Linha com Marcadores
elif menu == "SLAs":
    st.title("⏱️ Monitoramento de SLAs")
    st.dataframe(df_slas, use_container_width=True)
    
    if not df_slas.empty:
        col_y = "Performance" if "Performance" in df_slas.columns else df_slas.columns[-1]
        fig5 = px.line(df_slas, x=df_slas.columns[0], y=col_y, markers=True, title="Histórico de Cumprimento (%)", color_discrete_sequence=['#ef4444'])
        fig5.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#1e293b")
        st.plotly_chart(fig5, use_container_width=True)
