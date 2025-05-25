import streamlit as st
import numpy as np
import altair as alt

def configuracion_page():
    st.markdown(
        """
        <style>
            .block-container {
                padding-left: 2rem !important;
                padding-right: 2rem !important;
                max-width: 90% !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )


def configurar_grafico(fig, x1, p):
    """ Configuracion de la grafica usando Plotly"""
    fig.update_layout(
        title_text='EPS - ' + p, 
        title_x=0.5,
        title_subtitle_text='Este grafico es interactivo SabaEvents',
        title_font_color="red",
        title_subtitle_font_color="blue",
        xaxis_tickangle=-45,
        xaxis_title='Dates',
        yaxis_title='Events',
        xaxis=dict(
            tickmode='array',
            tickvals=np.arange(0, len(x1) + 1, 10000),
            ticktext=[str(i) for i in x1[::10000]]
        )
    )
    return fig


import altair as alt
import pandas as pd

def configurar_grafico_altair(
    df,
    col_x,
    col_y,
    col_z,
    promedio,
    maximo,
    titulo_grafico=None,
    color_linea='red',
    estilo_linea='dash',  # opciones: 'solid', 'dash', etc.
    tamano_titulo=16,
    alineacion_titulo='start',  # opciones: 'start', 'middle', 'end'
    subtitulo_eje_x=None,
    tamano_subtitulo=12,
    etiqueta_eje_x=None, 
    etiqueta_eje_y=None,
    scala_log_y="linear" # opciones: 'linear', 'log', 'pow','sqrt', 'symlog' ,'time','utc','ordinal', 'band', 'point', 'quantile', 'quantize', 'threshold' 
    ):
    
    # Título principal del gráfico
    titulo = titulo_grafico or [f"Max EPS: {maximo:,}", f"Average EPS: {promedio:,.2f}"] 

    #print(f"El valor del maximo es: {maximo}")
    #print(f"El valor del promedio es: {promedio}")

    # Etiquetas de ejes
    label_x = etiqueta_eje_x or col_x
    label_y = etiqueta_eje_y or col_y


    # Subtítulo debajo del eje X
    subtitulo = subtitulo_eje_x or col_x

    # Gráfico de barras
    barras = alt.Chart(df).mark_bar().encode(
        x=alt.X(col_x, sort=None, title=label_x),
        y=alt.Y(col_y, title=label_y, scale=alt.Scale(type=scala_log_y)),
        color=alt.Color(col_z, legend=alt.Legend(title=col_z))
    ).properties(
        title=alt.TitleParams(
            text=titulo,
            anchor=alineacion_titulo,
            fontSize=tamano_titulo
        )
    )

    # Línea del promedio
    linea_promedio = alt.Chart(pd.DataFrame({col_y: [promedio]})).mark_rule(
        color=color_linea,
        #strokeDash=[5, 5] if estilo_linea == 'dash' else None
        **({"strokeDash": [5, 5]} if estilo_linea == 'dash' else {})
    ).encode(
        y=col_y
    )

    return barras + linea_promedio


