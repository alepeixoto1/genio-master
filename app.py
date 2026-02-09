# ==============================
# CONTROLADOR DE TELAS
# ==============================

if pagina == "📊 Financeiro":
    setor = "Financeiro"

elif pagina == "📦 Ativos":
    setor = "Ativos"

elif pagina == "🌱 ESG":
    setor = "Esg"

elif pagina == "⏱️ SLAs":
    setor = "Slas"

elif pagina == "📄 Relatórios":

    st.title("📄 Central de Relatórios")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Gerar Relatório"):
            st.success("Relatório gerado")

    with col2:
        if st.button("Exportar PDF"):
            st.success("PDF exportado")

    st.stop()


elif pagina == "⚙️ Configurações":

    st.title("⚙️ Configurações do Sistema")

    st.toggle("Modo Escuro", value=True)
    st.toggle("Atualização Automática", value=True)

    st.stop()



