import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# CONFIGURAÇÃO E ESTILO (LIGHT MODE TOTAL)
# =====================================================
st.set_page_config(page_title="Gênio Master", layout="wide", page_icon="💎")

st.markdown("""
<style>
    /* Fundo da página e Sidebar */
    .stApp { background-color: #fcfcfc; color: #1e293b; }
    [data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #f0f0f0; }
    
    /* Títulos em preto sólido */
    h1, h2, h3 { color: #000000 !important; font-family: 'Segoe UI', sans-serif; }

    /* Cards Brancos com Borda Fina e Sombra */
    .card {
        background: #ffffff;
        padding: 24px;
        border-radius: 12px;
        border: 1px solid #eaeaea;
        text-align: left;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .card-title { font-size: 12px; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
    .card-value { font-size: 32px; font-weight: 800; color: #2563eb; margin-top: 4px; }

    /* Remove o fundo escuro padrão do Streamlit nos gráficos */
    .stPlotlyChart { background-color: #ffffff; border-radius: 12px; }
</style>
""", unsafe_allow_html=True)

# =====================================================
# CARREGAMENTO E LIMPEZA (GIDs ATUALIZADOS)
# =====================================================
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"

def carregar(gid):
    try:
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={gid}"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        # Tratamento numérico para colunas financeiras
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
# MENU
# =====================================================
with st.sidebar:
    st.markdown("### 💎 Gênio Master")
    menu = st.radio("Menu Principal", ["Painel Geral", "Financeiro", "Ativos", "Sustentabilidade", "SLAs"])

# =====================================================
# PÁGINAS COM GRÁFICOS DISTINTOS (LIGHT)
# =====================================================

# 1. PAINEL GERAL: Gráfico de Rosca (Donut)
if menu == "Painel Geral":
    st.title("📊 Resumo de Operações")
    
    c1, c2, c3 = st.columns(3)
    realizado = df_fin["Realizado"].sum() if "Realizado" in df_fin.columns else 0
    saving = df_fin["Saving"].sum() if "Saving" in df_fin.columns else 0
    
    c1.markdown(f'<div class="card"><div class="card-title">Realizado</div><div class="card-value">R$ {realizado:,.0f}</div></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="card"><div class="card-title">Saving</div><div class="card-value">R$ {saving:,.0f}</div></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="card"><div class="card-title">Qtd Ativos</div><div class="card-value">{len(df_ativos)}</div></div>', unsafe_allow_html=True)

    st.subheader("Custos por Categoria")
    fig1 = px.pie(df_fin, names="Categoria", values="Realizado", hole=0.6, 
                  template="plotly_white", color_discrete_sequence=px.colors.qualitative.Prism)
    st.plotly_chart(fig1, use_container_width=True)

# 2. FINANCEIRO: Gráfico de Barras Agrupadas
elif menu == "Financeiro":
    st.title("💰 Detalhamento de Verba")
    st.dataframe(df_fin, use_container_width=True)
    
    st.subheader("Análise Mensal: Previsto x Realizado")
    fig2 = px.bar(df_fin, x="Mês", y=["Previsto", "Realizado"], 
                  barmode="group", template="plotly_white", 
                  color_discrete_map={"Previsto": "#cbd5e1", "Realizado": "#2563eb"})
    st.plotly_chart(fig2, use_container_width=True)

# 3. ATIVOS: Gráfico de Área (Evolução/Volume)
elif menu == "Ativos":
    st.title("📦 Gestão de Patrimônio")
    st.dataframe(df_ativos, use_container_width=True)
    
    if not df_ativos.empty:
        st.subheader("Distribuição de Valor por Item")
        # Gráfico de área para mudar o padrão visual
        fig3 = px.area(df_ativos, x=df_ativos.columns[0], y=df_ativos.columns[-1], 
                       template="plotly_white", color_discrete_sequence=['#8b5cf6'])
        st.plotly_chart(fig3, use_container_width=True)

# 4. SUSTENTABILIDADE: Gráfico de Barras Horizontais
elif menu == "Sustentabilidade":
    st.title("🌱 Indicadores ESG")
    st.dataframe(df_esg, use_container_width=True)
    
    if not df_esg.empty:
        st.subheader("Impacto por Iniciativa")
        fig4 = px.bar(df_esg, x=df_esg.columns[-1], y=df_esg.columns[0], 
                      orientation='h', template="plotly_white", 
                      color_discrete_sequence=['#10b981'])
        st.plotly_chart(fig4, use_container_width=True)

# 5. SLAs: Gráfico de Linha com Marcadores
elif menu == "SLAs":
    st.title("⏱️ Performance e SLAs")
    st.dataframe(df_slas, use_container_width=True)
    
    if "Performance" in df_slas.columns:
        st.subheader("Histórico de Cumprimento (%)")
        fig5 = px.line(df_slas, x="Mês" if "Mês" in df_slas.columns else df_slas.columns[0], 
                       y="Performance", markers=True, template="plotly_white", 
                       color_discrete_sequence=['#ef4444'])
        st.plotly_chart(fig5, use_container_width=True)
