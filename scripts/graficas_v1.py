import streamlit as st
import pandas as pd
import plotly.express as px
from scripts import procesador as proc
st.title("Visualizador de Gráficas")

archivo = st.file_uploader("Selecciona un archivo Excel", type=["xlsx", "xls"])

if archivo is not None:
    xls = proc.cargar_excel(archivo)
    hojas = xls.sheet_names
    hoja = st.selectbox("Selecciona una hoja", hojas)

    if hoja:
        df = proc.leer_hoja(archivo, hoja)
        columnas = proc.obtener_columnas(df)

        col_x = st.selectbox("Selecciona la variable X", columnas)
        col_y = st.selectbox("Selecciona la variable Y", columnas)

        #if st.button('Cargar Datos:')
        

        if col_x and col_y:
            promedio, maximo = proc.calcular_estadisticas(df[col_y])
            st.write(f"Promedio de: {promedio}")
            st.write(f"Máximo de: {maximo}")

            # Botón para mostrar la gráfica
            if st.button("Mostrar gráfica"):
                fig = px.bar(df, x=col_x, y=col_y, title=f"{col_y} vs {col_x}")
                st.plotly_chart(fig)

                # Botón para guardar la gráfica
                if st.button("Guardar gráfica como imagen"):
                    fig.write_image("grafica.png")
                    st.success("Gráfica guardada como 'grafica.png'")

