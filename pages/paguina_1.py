import streamlit as st

st.title("Página 1")
st.write("Página de Prueba")

st.subheader("🔍 Variables en session_state")

if st.session_state:
    for clave, valor in st.session_state.items():
        st.markdown(f"- **{clave}**: `{valor}`")
else:
    st.info("No hay variables en session_state todavía.")


