import pandas as pd
import streamlit as st

@st.cache_resource
def cargar_excel(archivo):
    return pd.ExcelFile(archivo)

@st.cache_data
def leer_hoja(nombre_archivo, hoja):
    print("Leyendo la hoja de Calculo")
    df = pd.read_excel(nombre_archivo, sheet_name=hoja)
    return df


@st.cache_data
def obtener_columnas(df):
    print("Obteniendo las columnas de la Hoja de Calculo")
    return df.columns.to_list()

@st.cache_data
def calcular_estadisticas(serie):
    return serie.mean(), serie.max()


def filtrar_datos(df,x, y,  filter_condition):
    # Inicializa un vector con los DataFrame filtrados
    df_final = []

    # Obtener el nombre de la primera columna
    first_col = df.columns[0]

    # Convertir esa columna a datetime
    df[first_col] = pd.to_datetime(df[first_col])

    # Ordenar el DataFrame por esa columna
    df = df.sort_values(by=first_col)

    # Agrega el df ordenado y total a la variable df_final
    df_final.append(pd.DataFrame({
        x: df[x],
        y : df[y], 
        filter_condition : df[filter_condition]
    }))

    # Elimina los duplicados y devuelve un vector con los valores
    filtros = df[filter_condition].drop_duplicates().values.flatten()
    
    # recorro el vector
    for filtro in filtros:
        vector = {}
        # Filtro
        df_filtrado = df[df[filter_condition] == filtro]

        vector = {
            x : df_filtrado[x],
            y : df_filtrado[y],
            filter_condition : filtro
        }
        df_final.append(pd.DataFrame(vector))
    return df_final

def detectar_columnas_mixtas(df):
    columnas_mixtas = []
    for col in df.columns:
        tipos = df[col].apply(type).nunique()
        if tipos > 1:
            columnas_mixtas.append(col)
    return columnas_mixtas

def convertir_columnas_a_str(df, columnas):
    for col in columnas:
        df[col] = df[col].astype(str)
    return df

    
