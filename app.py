import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração de Interface
st.set_page_config(page_title="Gênio Master Pro", layout="wide", initial_sidebar_state="collapsed")

# --- CSS EXCLUSIVO ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background-color: #f8f9fb; }

    .genio-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border-radius: 12px;
        padding: 20px;
        color: white;
        min-height: 120px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin-bottom: 15px;
    }

    .genio-label { font-size: 13px; font-weight: 600; opacity: 0.7; letter-spacing: 0.5px; }
    .genio-value { font-size: 22px; font-weight: 800; margin-top: 8px; }
    .genio-delta { font-size: 12px; color: #10b981; margin-top: 5px; font-weight: bold; }

    div.stPlotlyChart {
        background-color: white !important;
        border-radius: 16px !important;
        padding: 10px !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04) !important;
    }

    .footer-genio {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: white;
        border-top: 1px solid #e2e8f0;
        display: flex;
        justify-content: space-around;
        padding: 12px 0;
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)

# --- CONFIGURAÇÃO ---
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"

CONFIG = {
    "Financeiro": {"gid": "0", "cor": "#1e293b", "icon": "💰"},
    "Ativos": {"gid": "1179272110", "cor": "#0f172a", "icon": "📦"},
    "Esg": {"gid": "1026863401", "cor": "#334155", "icon": "🌱"},
    "Slas": {"gid": "2075740723", "cor": "#1e293b", "icon": "⏱️"}
}

setor = st.sidebar.selectbox("Módulo", list(CONFIG.keys()))

url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG[setor]['gid']}"

try:

    df = pd.read_csv(url, skiprows=2).dropna(how='all', axis=1).dropna(how='all', axis=0)

    if not df.empty:

        st.markdown(f"### 💎 Gênio Master | **{setor} Overview**")
        st.markdown(
            "<p style='color:#64748b; margin-top:-15px;'>Análise estratégica em tempo real.</p>",
            unsafe_allow_html=True
        )

        # CARDS
        c1, c2, c3, c4 = st.columns(4)

        cols_num = df.select_dtypes(include=['number']).columns

        with c1:
            st.markdown(
                f'<div class="genio-card">'
                f'<div class="genio-label">{CONFIG[setor]["icon"]} TOTAL {setor.upper()}</div>'
                f'<div class="genio-value">{len(df)}</div>'
                f'<div class="genio-delta">● Ativos</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        with c2:
            val = df[cols_num[0]].sum() if len(cols_num) > 0 else 0
            st.markdown(
                f'<div class="genio-card">'
                f'<div class="genio-label">📈 VOLUME ACUMULADO</div>'
                f'<div class="genio-value">{val:,.0f}</div>'
                f'<div class="genio-delta"># Mensal</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        with c3:
            st.markdown(
                f'<div class="genio-card">'
                f'<div class="genio-label">✅ EFICIÊNCIA</div>'
                f'<div class="genio-value">98.5%</div>'
                f'<div class="genio-delta">↑ 1.2%</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        with c4:
            st.markdown(
                f'<div class="genio-card">'
                f'<div class="genio-label">🌐 DISPONIBILIDADE</div>'
                f'<div class="genio-value">Sync OK</div>'
                f'<div class="genio-delta">v5.2 Stable</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # GRÁFICOS
        st.markdown("#### PERFORMANCE ANALYTICS")

        g1, g2 = st.columns(2)

        with g1:

            if len(cols_num) > 0:

                fig_area = px.area(
                    df,
                    x=df.index,
                    y=cols_num[0],
                    title="TENDÊNCIA ACUMULADA"
                )

                fig_area.update_layout(
                    height=300,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=0, r=0, t=40, b=0),
                    title_x=0.5,
                    font=dict(color="#1e293b")
                )

                st.plotly_chart(
                    fig_area,
                    width="stretch",
                    config={'displayModeBar': False}
                )

        with g2:

            cols_txt = df.select_dtypes(include=['object']).columns

            if len(cols_txt) > 0:

                fig_pie = px.pie(
                    df,
                    names=cols_txt[0],
                    hole=0.6,
                    title="DISTRIBUIÇÃO"
                )

                fig_pie.update_layout(
                    height=300,
                    showlegend=False,
                    margin=dict(l=0, r=0, t=40, b=0),
                    title_x=0.5
                )

                st.plotly_chart(
                    fig_pie,
                    width="stretch",
                    config={'displayModeBar': False}
                )

        # FOOTER
        st.markdown("""
            <div class="footer-genio">
                <div style="text-align:center; color:#0f172a; font-weight:bold;">
                    🏠<br><small>Gênio</small>
                </div>
                <div style="text-align:center; color:#94a3b8;">
                    💬<br><small>Chat</small>
                </div>
                <div style="text-align:center; color:#94a3b8;">
                    🛡️<br><small>Admin</small>
                </div>
                <div style="text-align:center; color:#94a3b8;">
                    🔔<br><small>Alertas</small>
                </div>
            </div>
            <br><br>
        """, unsafe_allow_html=True)

except Exception as e:

    st.error(f"Erro ao carregar dados: {e}")

