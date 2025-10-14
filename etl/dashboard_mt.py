# =============== Librerías
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from etl.reviewdata import consultar_tblmaternas_mt
import yaml
import pydeck as pdk
import folium
from streamlit_folium import st_folium

# ================ Configuración
with open("config/settings.yaml") as f:
    config = yaml.safe_load(f)

# ================ Estilos
st.title("Tablero de Información Muerte de Maternas")

st.markdown(
    """
    <div style="Text-align: center;"> Grupo 2 bootcamp: Yoly Maurello / Javier Sierra/ Jose Palacio</div> 
    <style>
    body {
        background-color: #b0a690;
        }
    </style>
    """,
    unsafe_allow_html=True
)

#=========== Configuración de la página
st.set_page_config(
    page_title="Tablero de Información Muerte de Maternas",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# ================ Carga de datos
df = consultar_tblmaternas_mt(config["db_connection"], "SELECT id_registro,fecha_evento,edad,rangos_edades,codigo_prestacion,nacionalidad,ocupacion,etnia,semanas,pais,departamento,municipio,causa,latitud,longitud,categoria_causa FROM tbl_maternas_mt;")
# ================ Filtros
# 
pr_anno = consultar_tblmaternas_mt(config["db_connection"], """
    SELECT DISTINCT EXTRACT(YEAR FROM fecha_evento) AS año_evento FROM tbl_maternas_mt;
""")
pr_departamentos = df["departamento"].dropna().unique().tolist()
pr_edades = df["edad"].dropna().unique().tolist()
pr_causas = df["causa"].dropna().unique().tolist()
pr_categoria = df["categoria_causa"].dropna().unique().tolist()

st.sidebar.header("Filtros")

rango_años = st.sidebar.slider(
    "Selecciona el rango de años",
    int(pr_anno["año_evento"].min()),
    int(pr_anno["año_evento"].max()),
    (int(pr_anno["año_evento"].min()), int(pr_anno["año_evento"].max()))
)


#st.write("Primeros datos:", df.head())

df_filtrado = pr_anno[(pr_anno["año_evento"] >= rango_años[0]) & (pr_anno["año_evento"] <= rango_años[1])]

if pr_categoria:
    categoria_seleccionados = st.sidebar.multiselect(
        "Selecciona los categorias de causas",
        options=pr_categoria,
        default=pr_categoria
    )
    df = df[df["categoria_causa"].isin(categoria_seleccionados)]


if pr_departamentos:
    departamentos_seleccionados = st.sidebar.multiselect(
        "Selecciona los departamentos",
        options=pr_departamentos,
        default=pr_departamentos
    )
    df = df[df["departamento"].isin(departamentos_seleccionados)]

if pr_edades:
    edades_seleccionadas = st.sidebar.multiselect(
        "Selecciona las edades",
        options=pr_edades,
        default=pr_edades
    )
    df = df[df["edad"].isin(edades_seleccionadas)]

if pr_causas:
    causas_seleccionadas = st.sidebar.multiselect(
        "Selecciona las causas básicas",
        options=pr_causas,
        default=pr_causas
    )
    df = df[df["causa"].isin(causas_seleccionadas)]

capa_seleccionada = st.sidebar.selectbox(
    "Selecciona la capa a visualizar en el mapa",
    options=["Marcadores", "Círculos proporcionales", "Heatmap", "Todas las anteriores"]
)


# ================ Etiquietas
c1,c2,c3,c4 = st.columns(4)
with c1:
               
    st.markdown(
        f"""
        <div style='background-color:#080807; padding:8px; border-radius:6px; text-align:center;'>
            <h4 style='color:#DCCCAA;'>Total casos</h4>
            <p style='font-size:26px; font-weight:bold; color:#DCCCAA;'>{len(df):,}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div style='background-color:#b0a690; padding:8px; border-radius:6px; text-align:center;'>
            <h4 style='color:#080807;'>Edad mínima</h4>
            <p style='font-size:26px; font-weight:bold; color:#080807;'>{df['edad'].min()} años</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div style='background-color:#b0a690; padding:8px; border-radius:6px; text-align:center;'>
            <h4 style='color:#080807;'>Edad máxima</h4>
            <p style='font-size:26px; font-weight:bold; color:#080807;'>{df['edad'].max()} años</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        f"""
        <div style='background-color:#f0eadd; padding:8px; border-radius:6px; text-align:center;'>
            <h4 style='color:#080807;'>Edad promedio</h4>
            <p style='font-size:26px; font-weight:bold; color:#080807;'>{round(df['edad'].mean())} años</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ================ Graficas
grf1,grf2,grf0 = st.columns([40,30,30])
with grf1:
    #
    if "fecha_evento" in df.columns:
        df["fecha_evento"] = pd.to_datetime(df["fecha_evento"], errors="coerce")
        df["año_evento"] = df["fecha_evento"].dt.year

    # Aplicar filtro por año
    df_filtrado = df[
        (df["año_evento"] >= rango_años[0]) &
        (df["año_evento"] <= rango_años[1])
    ]
    
    # ================ Gráfica de muertes por año
    st.subheader("Muertes por Año")
    df_ano = df_filtrado["año_evento"].value_counts().sort_index().reset_index()
    df_ano.columns = ["año_evento", "muertes"]

    fig_ano = go.Figure()
    fig_ano.add_trace(go.Bar(
        x=df_ano["año_evento"],
        y=df_ano["muertes"],
        name="Muertes",
        marker_color="#730000",
        text=df_ano["muertes"],  # Mostrar el total encima de cada barra
        textposition="outside"
  ))

    if len(df_ano) > 1:
        z = np.polyfit(df_ano["año_evento"], df_ano["muertes"], 1)
        p = np.poly1d(z)
        fig_ano.add_trace(go.Scatter(
            x=df_ano["año_evento"],
            y=p(df_ano["año_evento"]),
            mode="lines",
            name="Tendencia",
            line=dict(color='white', dash="dash")         
        ))

    fig_ano.update_layout(xaxis_title="Año", yaxis_title="Muertes")
    st.plotly_chart(fig_ano)

with grf2:
    if "causa" in df_filtrado.columns:
        st.subheader("Top 10 Causas Más Frecuentes")
        top_causas = df_filtrado["causa"].value_counts().nlargest(10).reset_index()
        top_causas.columns = ["Causa", "Número de Casos"]

        fig_causa_top10 = px.bar(
            top_causas,
            x="Causa",
            y="Número de Casos",
            color="Número de Casos",
            color_continuous_scale="Reds",
            text="Número de Casos"
        )

    fig_causa_top10.update_traces(textposition="outside")
    st.plotly_chart(fig_causa_top10)
with grf0:
    if "categoria_causa" in df_filtrado.columns:
        st.subheader("Categoria por Causas")
        cat_causas = df_filtrado["categoria_causa"].value_counts().nlargest(10).reset_index()
        cat_causas.columns = ["Categoria Causa", "Número de Casos"]

        fig_cat_causa = px.bar(
            cat_causas,
            x="Categoria Causa",
            y="Número de Casos",
            color="Número de Casos",
            color_continuous_scale="Reds",
            text="Número de Casos"
        )

        fig_cat_causa.update_traces(textposition="outside")
        st.plotly_chart(fig_cat_causa)


#Mapa 
# Agrupar por departamento y contar muertes
from folium.plugins import HeatMap

grf3,grf4,grf5 = st.columns([40,30,30])
# Agrupar datos filtrados
with grf3:
    if "causa" in df_filtrado.columns:
            st.subheader("Distribución de Muertes por Causas")

            df_causa = df_filtrado["causa"].value_counts().nlargest(10).reset_index()
            df_causa.columns = ["Causa", "Número de Muertes"]

            fig_causa = px.pie(
                df_causa,
                names="Causa",
                values="Número de Muertes",
                title="Muertes por Causas(Top 10)",
                color_discrete_sequence=px.colors.sequential.RdBu
            )

            st.plotly_chart(fig_causa)

with grf4:
        
    if "etnia" in df_filtrado.columns:
        st.subheader("Distribución de Muertes por Etnia")

        df_etnia = df_filtrado["etnia"].value_counts().reset_index()
        df_etnia.columns = ["Etnia", "Número de Muertes"]

        fig_etnia = px.pie(
            df_etnia,
            names="Etnia",
            values="Número de Muertes",
            title="Muertes por Etnia",
            color_discrete_sequence=px.colors.sequential.RdBu
        )

        st.plotly_chart(fig_etnia)
with grf5:
        if "rangos_edades" in df_filtrado.columns:
            st.subheader("Distribución de Muertes por Edades")

            df_etnia = df_filtrado["rangos_edades"].value_counts().reset_index()
            df_etnia.columns = ["Rangos_edades", "Número de Muertes"]

            fig_etnia = px.pie(
                df_etnia,
                names="Rangos_edades",
                values="Número de Muertes",
                title="Muertes por Edades",
                color_discrete_sequence=px.colors.sequential.RdBu
            )

            st.plotly_chart(fig_etnia)



df_grouped = df_filtrado.groupby(['departamento', 'latitud', 'longitud']).size().reset_index(name='muertes')

# Crear mapa base
mapa = folium.Map(location=[4.5709, -74.2973], zoom_start=6)

# Capa: Marcadores
if capa_seleccionada in ["Marcadores", "Todas las anteriores"]:
    for _, row in df_grouped.iterrows():
        tooltip = f"{row['departamento']}: {row['muertes']} muertes"
        folium.Marker(
            location=[row['latitud'], row['longitud']],
            popup=tooltip,
            tooltip=tooltip,
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(mapa)

# Capa: Círculos proporcionales
if capa_seleccionada in ["Círculos proporcionales", "Todas las anteriores"]:
    for _, row in df_grouped.iterrows():
        folium.Circle(
            location=[row['latitud'], row['longitud']],
            radius=row['muertes'] * 1000,
            color='crimson',
            fill=True,
            fill_opacity=0.4,
            popup=f"{row['departamento']}: {row['muertes']} muertes"
        ).add_to(mapa)

# Capa: Heatmap
if capa_seleccionada in ["Heatmap", "Todas las anteriores"]:
    heat_data = [[row['latitud'], row['longitud'], row['muertes']] for _, row in df_grouped.iterrows()]
    HeatMap(heat_data).add_to(mapa)

# Mostrar mapa
st_folium(mapa, width=700, height=500,)
# ================ Vista previa
#st.write("Vista previa de los datos filtrados:")
#st.dataframe(df_filtrado.head())
