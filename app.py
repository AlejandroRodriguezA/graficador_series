import streamlit as st
import pandas as pd
#import numpy as np
import plotly.express as px
import altair as alt
import plotly.graph_objects as go
from scripts import procesador as proc
from scripts import configuration as confg

n = 0


def cargar_datos():
    global n 
    #n += 1
    #print(f"Entro y paso: {n}")

    with st.sidebar.expander("Datos del Archivo:", expanded=True):
        opcion = st.radio("¿Qué datos quieres usar?", ["Usar datos de muestra", "Subir mi propio archivo"])
        

        if opcion == "Usar datos de muestra":
            archivo = "data/muestra.xlsx"
            try:
                xls = proc.cargar_excel(archivo)
                hojas = xls.sheet_names
                hoja = st.selectbox("Selecciona una hoja", hojas, key="hoja_muestra")
                if st.button("Cargar hoja de muestra"):
                    n += 1
                    print(n)
                    st.session_state['df'] = proc.leer_hoja(archivo, hoja)
                    st.session_state['columnas'] = proc.obtener_columnas(st.session_state['df'])
                    st.session_state['mostrar_grafico'] = True
            except Exception as e:
                st.error(f"No se pudo cargar el archivo de muestra: {e}")

        else:
            archivo = st.file_uploader("Selecciona un archivo Excel", type=["xlsx", "xls"])
            if archivo is not None:
                try:
                    xls = proc.cargar_excel(archivo)
                    hojas = xls.sheet_names
                    hoja = st.selectbox("Selecciona una hoja", hojas, key="hoja_usuario")
                    if st.button("Cargar hoja del archivo"):
                        st.session_state['df'] = proc.leer_hoja(archivo, hoja)
                        st.session_state['columnas'] = proc.obtener_columnas(st.session_state['df'])
                        st.session_state['mostrar_grafico'] = True
                except Exception as e:
                    st.error(f"No se pudo cargar el archivo: {e}")


#def cargar_datos():
    #with st.sidebar.expander("Datos del Archivo:", expanded=True):
        #archivo = st.file_uploader("Selecciona un archivo Excel", type=["xlsx", "xls"])
        #if archivo is not None:
            #xls = proc.cargar_excel(archivo)
            #hojas = xls.sheet_names
            #hoja = st.selectbox("Selecciona una hoja", hojas)
            #if st.button("Cargar hoja"):
                #st.session_state['df'] = proc.leer_hoja(archivo, hoja)
                #st.session_state['columnas'] = proc.obtener_columnas(st.session_state['df'])
                #st.session_state['mostrar_grafico'] = True

def configurar_datos_grafico():
    with st.sidebar.expander("Datos del gráfico", expanded=True):
        columnas = st.session_state['columnas']
        st.session_state['col_x'] = st.selectbox("Selecciona la variable X:", columnas, key="col_x_select")
        st.session_state['col_y'] = st.selectbox("Selecciona la variable Y:", columnas, key="col_y_select")
        st.session_state['col_z'] = st.selectbox("Selecciona la variable a agrupar:", columnas, key="col_z_select")
        if st.button("Calcular estadísticas"):
            st.session_state['boton2'] = True


def mostrar_estadisticas(df, col_y):
    promedio, maximo = proc.calcular_estadisticas(df[col_y])
    col1, col2, col3 = st.columns(3)
    with col1:
        st.subheader("Promedios")
        st.write(f"{promedio:,.2f}")
    with col2:
        st.subheader("Máximo")
        st.write(f"{maximo:,}")
    with col3:
        st.subheader("Registros")
        st.write(f"{len(df):,}")
    return promedio, maximo

def mostrar_checkBox(df, check_key):
    if 'ver_muestra' not in st.session_state:
        st.session_state['ver_muestra'] = True
    if 'muestra' not in st.session_state:
        st.session_state['muestra'] = 100

    col4, col5 = st.columns(2)
    with col4:
        st.session_state['ver_muestra'] = st.checkbox("Mostrar solo muestra", value=st.session_state['ver_muestra'], key = check_key)
    with col5:
        st.session_state['muestra'] = st.slider("Muestra:", min_value=10, max_value=len(df), value=st.session_state['muestra'])


    

def main():
    # Configuracion de la pagina, CCS
    confg.configuracion_page()

    if 'mostrar_grafico' not in st.session_state:
        st.session_state['mostrar_grafico'] = False

    cargar_datos()

    if st.session_state.get('mostrar_grafico', False):
        configurar_datos_grafico()

    if st.session_state.get('boton2', False):

        df = st.session_state['df']
        col_x = st.session_state['col_x']
        col_y = st.session_state['col_y']
        col_z = st.session_state['col_z']


        # Ordeno y separo el dataFrame
        lista_de_df = proc.filtrar_datos(df, col_x, col_y, col_z)

        # Asigno a df el dataFrame entero
        df = lista_de_df[0]

        # Actualizo el valor del df en session_state
        st.session_state['df'] = df

        promedio, maximo= mostrar_estadisticas(df, col_y)

        mostrar_checkBox(df, 1)

        #total = mostrar_datos_grafico(df, col_x, col_y, col_z, promedio, maximo)
        #parcial_1 = mostrar_datos_grafico(lista_de_df[1], col_x, col_y, col_z, promedio, maximo, "Gráfico Parcial 1")
        #parcial_2 = mostrar_datos_grafico(lista_de_df[2], col_x, col_y, col_z, promedio, maximo, "Gráfico Parcial 2")

        # Se filtran los datos, para graficar muestra o la totalidad de los graficos
        datos = df.head(st.session_state['muestra']) if st.session_state['ver_muestra'] else df
        datos_1 = lista_de_df[1].head(st.session_state['muestra']) if st.session_state['ver_muestra'] else lista_de_df[1]
        datos_2 = lista_de_df[2].head(st.session_state['muestra']) if st.session_state['ver_muestra'] else lista_de_df[2]

        total = confg.configurar_grafico_altair(
            df=datos,
            col_x=col_x,
            col_y=col_y,
            col_z=col_z,
            promedio=promedio,
            maximo=maximo,
            titulo_grafico=f"",
            color_linea='red',
            estilo_linea='solid',
            tamano_titulo=26,
            alineacion_titulo='start',
            subtitulo_eje_x=f"{col_x} agrupado por {col_z}",
            etiqueta_eje_x=f" Graph: Orizio detailed events per second ",
            etiqueta_eje_y=f" "
        )

        parcial_1 = confg.configurar_grafico_altair(
            df=datos_1,
            col_x=col_x,
            col_y=col_y,
            col_z=col_z,
            promedio=promedio,
            maximo=maximo,
            titulo_grafico=f" ",
            color_linea='red',
            estilo_linea='solid',
            tamano_titulo=16,
            alineacion_titulo='middle',
            subtitulo_eje_x=f"{col_x} agrupado por {col_z}",
            etiqueta_eje_x=f" Graph: Sabena detailed events per second",
            etiqueta_eje_y=f" "
        )

        parcial_2 = confg.configurar_grafico_altair(
            df=datos_2,
            col_x=col_x,
            col_y=col_y,
            col_z=col_z,
            promedio=promedio,
            maximo=maximo,
            titulo_grafico=f" ",
            color_linea='red',
            estilo_linea='solid',
            tamano_titulo=16,
            alineacion_titulo='middle',
            subtitulo_eje_x=f"{col_x} agrupado por {col_z}",
            etiqueta_eje_x=f"Graph: Sabca detailed events  per second",
            etiqueta_eje_y=f"EPS"
        )




        # Concatenar verticalmente
        grafico_concatenado = alt.vconcat(total, parcial_1, parcial_2).resolve_scale(
            y='independent'  # Opcional: permite que cada gráfico tenga su propia escala Y
        )

        # Mostrar en Streamlit
        st.altair_chart(grafico_concatenado, use_container_width=True)



        #alt.vconcat(total, parcial_1, parcial_2)


if __name__ == "__main__":
    main()