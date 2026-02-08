# --- LINHA 1: CARDS DE MÉTRICAS (KPIs) ---
        m1, m2, m3, m4 = st.columns(4)
        
        # Identifica colunas numéricas para cálculos
        cols_num = df.select_dtypes(include=['number']).columns
        cols_txt = df.select_dtypes(include=['object']).columns

        with m1:
            st.metric("Total de Itens", len(df))
        with m2:
            if len(cols_num) > 0:
                # Soma a última coluna numérica (geralmente onde fica o valor/total)
                total_soma = df[cols_num[-1]].sum()
                st.metric("Valor Total", f"R$ {total_soma:,.2f}")
            else:
                st.metric("Valor Total", "R$ 0,00")
        with m3:
            st.metric("Eficiência", "99.9%", "+0.2%")
        with m4:
            st.metric("Sincronização", "Real-time")

        st.markdown("<br>", unsafe_allow_html=True)

        # --- LINHA 2: GRÁFICOS ---
        tab1, tab2 = st.tabs(["📊 VISÃO ESTRATÉGICA", "🔍 ANÁLISE DE DADOS"])

        with tab1:
            c1, c2 = st.columns(2)
            
            with c1:
                if len(cols_txt) > 0:
                    # Gráfico de Rosca usando a primeira coluna de texto
                    fig_donut = px.pie(df, names=cols_txt[0], hole=0.7,
                                     color_discrete_sequence=[CONFIG[setor]['cor'], '#1c1f26', '#2d323d'])
                    fig_donut.update_layout(title="<b>Distribuição</b>", template="plotly_dark",
                                          paper_bgcolor='rgba(0,0,0,0)', showlegend=True)
                    st.plotly_chart(fig_donut, use_container_width=True)

            with c2:
                if len(cols_txt) > 0 and len(cols_num) > 0:
                    # Gráfico de Barras comparando Texto vs Último Número
                    fig_bar = px.bar(df, x=cols_num[-1], y=cols_txt[0], orientation='h')
                    fig_bar.update_traces(marker_color=CONFIG[setor]['cor'])
                    fig_bar.update_layout(title="<b>Ranking Performance</b>", template="plotly_dark",
                                        paper_bgcolor='rgba(0,0,0,0)', xaxis=dict(showgrid=False))
                    st.plotly_chart(fig_bar, use_container_width=True)
