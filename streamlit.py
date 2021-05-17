import streamlit as st
from PIL import Image
import src.manage_data as dat
import plotly.express as px
import pandas as pd
import folium
from streamlit_folium import folium_static
import codecs
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

st.write("""
# Mi súper Dashboard
Empieza el viaje 🚀🚀🚀
""")

ciudad1 = st.text_input(

    "Selecciona una ciudad de salida"
)
ciudad1 = str(ciudad1)
ciudad2 = st.text_input(

    "Selecciona una ciudad de vuelta"
)
ciudad2 = str(ciudad2)


fecha_ida = st.text_input(

    "Selecciona que día vas a salir (yy-mm-dd)"
)
st.write("Fecha salida", fecha_ida)

fecha_vuelta = st.text_input(

    "Selecciona que día vas a volver (yy-mm-dd)"
)
st.write("Fecha vuelta", fecha_vuelta)

st.dataframe(dat.tiempazo(ciudad2))

fecha_ida = str(fecha_ida)
fecha_vuelta = str(fecha_vuelta)


st.dataframe(dat.vuelazos(ciudad1,ciudad2,fecha_ida,fecha_vuelta))

st.dataframe(dat.hotelazo(ciudad2,"17","18"))

