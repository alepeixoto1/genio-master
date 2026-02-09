# GRÁFICOS PROFISSIONAIS
st.markdown("#### PERFORMANCE ANALYTICS")

g1, g2 = st.columns(2)

cor_principal = "#3b82f6"
cor_secundaria = "#10b981"

with g1:

    if len(cols_num) > 0:

        fig_area = px.area(
            df,
            x=df.index,
            y=cols_num[0],
        )

        fig_area.update_traces(
            line=dict(width=3, color=cor_principal),
        )

        fig_area.update_layout(
            height=340,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=10, b=10),

            xaxis=dict(
                showgrid=False,
                showline=False,
                zeroline=False
            ),

            yaxis=dict(
                showgrid=True,
                gridcolor='rgba(0,0,0,0.05)',
                zeroline=False
            ),

            hovermode="x unified",

            font=dict(
                family="Plus Jakarta Sans",
                size=13,
                color="#0f172a"
            )
        )

        st.plotly_chart(
            fig_area,
            width="stretch",
            config={
                'displayModeBar': False,
                'responsive': True
            }
        )

with g2:

    cols_txt = df.select_dtypes(include=['object']).columns

    if len(cols_txt) > 0:

        fig_pie = px.pie(
            df,
            names=cols_txt[0],
            hole=0.75,
        )

        fig_pie.update_traces(
            textinfo='percent+label',
            pull=[0.03] * len(df[cols_txt[0]].unique())
        )

        fig_pie.update_layout(

            height=340,

            paper_bgcolor='rgba(0,0,0,0)',

            margin=dict(l=10, r=10, t=10, b=10),

            showlegend=False,

            font=dict(
                family="Plus Jakarta Sans",
                size=13,
                color="#0f172a"
            ),

            annotations=[dict(
                text="GENIO",
                x=0.5,
                y=0.5,
                font_size=18,
                showarrow=False
            )]
        )

        st.plotly_chart(
            fig_pie,
            width="stretch",
            config={
                'displayModeBar': False,
                'responsive': True
            }
        )

