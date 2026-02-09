import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# CONFIG
st.set_page_config(
    page_title="Gênio Master Pro",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS PREMIUM
st.markdown("""
<style>

.stApp {
    background: linear-gradient(180deg,#0f172a 0%,#020617 100%);
}

.block-container {
    padding-top: 2rem;
}

.genio-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    border-radius: 16px;
    padding: 20px;
}

.card-title {
    font-size: 13px;
    color: #94a3b8;
}

.card-value {
    font-size: 28px;
    font-weight: bold;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# CONFIG PLANILHA
SHEET_ID = "1jFpKsA1jxOchNS4s6yE5M9YvQz9yM_NgWONjly4iI3o"

CONFIG = {
    "Financeiro": {"gid": "0", "icon": "💰"},
    "Ativos": {"gid": "1179272110", "icon": "📦"},
    "Esg": {"gid": "1026863401", "icon": "🌱"},
    "Slas": {"gid": "2075740723", "icon": "⏱️"}
}

setor = st.sidebar.selectbox("Módulo", CONFIG.keys())

url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={CONFIG[setor]['gid']}"

try:

    df = pd.read_csv(url, skiprows=2)

    df = df.dropna(how="all", axis=1)
    df = df.dropna(how="all", axis=0)

    st.markdown(f"# {CONFIG[setor]['icon']} Gênio Master • {setor}")

    cols_num = df.select_dtypes(include="number").columns

    # KPIs
    c1,c2,c3,c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="genio-card">
        <div class="card-title">TOTAL REGISTROS</div>
        <div class="card-value">{len(df)}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        total = int(df[cols_num[0]].sum()) if len(cols_num)>0 else 0
        st.markdown(f"""
        <div class="genio-card">
        <div class="card-title">VOLUME</div>
        <div class="card-value">{total}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="genio-card">
        <div class="card-title">STATUS</div>
        <div class="card-value">Online</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown("""
        <div class="genio-card">
        <div class="card-title">SYNC</div>
        <div class="card-value">100%</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("## Analytics")

    g1,g2 = st.columns(2)

    # AREA CHART PREMIUM
    with g1:

        if len(cols_num)>0:

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=df.index,
                y=df[cols_num[0]],
                mode='lines',
                line=dict(
                    width=4,
                    color='#3b82f6'
                ),
                fill='tozeroy',
                fillcolor='rgba(59,130,246,0.2)'
            ))

            fig.update_layout(

                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',

                font=dict(color="white"),

                margin=dict(l=0,r=0,t=30,b=0),

                xaxis=dict(showgrid=False),

                yaxis=dict(
                    gridcolor='rgba(255,255,255,0.05)'
                )
            )

            st.plotly_chart(fig, width="stretch")

    # DONUT PREMIUM
    with g2:

        cols_txt = df.select_dtypes(include="object").columns

        if len(cols_txt)>0:

            fig2 = px.pie(
                df,
                names=cols_txt[0],
                hole=0.8
            )

            fig2.update_layout(

                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color="white"),

                showlegend=True,

                margin=dict(l=0,r=0,t=30,b=0)
            )

            st.plotly_chart(fig2, width="stretch")

except Exception as e:

    st.error(e)

