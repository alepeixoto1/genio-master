import streamlit as st
import pandas as pd
import plotly.express as px

# resto do código...

try:

    df = pd.read_csv(url, skiprows=2).dropna(how='all', axis=1).dropna(how='all', axis=0)

    if not df.empty:

        # CARDS AQUI

        # COLE OS GRÁFICOS AQUI
        st.markdown("#### PERFORMANCE ANALYTICS")

        g1, g2 = st.columns(2)

        # resto dos gráficos...

