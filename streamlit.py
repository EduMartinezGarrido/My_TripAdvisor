import time
import streamlit as st
from PIL import Image
import src.manage_data as dat
import plotly.express as px
import pandas as pd
import folium
from streamlit_folium import folium_static
import codecs
import streamlit.components.v1 as components
import requests
import json
from dotenv import load_dotenv
import os
load_dotenv()
import src.Funciones as fun
from functools import reduce
import operator
from pandas import json_normalize
import numpy as np
from geopy.geocoders import Nominatim
from folium import Choropleth, Circle, Marker, Icon, Map

st.set_page_config(layout="wide")

HTML_BANNER = """
    <div style="background-color:#464e5f;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">My TripAdvisor </h1>
    </div>
    """

components.html(HTML_BANNER)

st.markdown("<h1 style='text-align: center; color: #464e5f;'>Ready for the holidays 🚀</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.beta_columns([1,2,0.5])

with col1:
    st.write("")

with col2:
    st.markdown("![Alt Text](https://media.giphy.com/media/ehZzdZPnnQFDqNn0MF/giphy.gif)")

with col3:
    st.write("")




ciudad1 = st.sidebar.text_input(

    "Selecciona una ciudad de salida"
)
ciudad1 = str(ciudad1)
ciudad2 = st.sidebar.text_input(

    "Selecciona una ciudad de vuelta"
)
ciudad2 = str(ciudad2)


fecha_ida = st.sidebar.text_input(

    "Selecciona que día vas a salir (yyyy-mm-dd)"
)
st.sidebar.write("Fecha salida", fecha_ida)

fecha_vuelta = st.sidebar.text_input(

    "Selecciona que día vas a volver (yyyy-mm-dd)"
)
st.sidebar.write("Fecha vuelta", fecha_vuelta)

fecha_ida = str(fecha_ida)
fecha_vuelta = str(fecha_vuelta)

st.markdown("")
st.markdown("")
st.markdown("")
st.markdown("")
st.markdown("")


if  ciudad1 != "" and ciudad2 != "" and fecha_ida != "" and fecha_vuelta != "":
    
    time.sleep(3)
    st.markdown("<h1 style='text-align: center; color: #464e5f;'>¿Qué tiempo tendré en los próximos días?</h1>", unsafe_allow_html=True)
    st.table(dat.tiempazo(ciudad2))
    tiempo = dat.tiempazo(ciudad2)
    fig = px.line(tiempo, x=tiempo.date, y=tiempo.columns[1:3],template= "ggplot2")
    col1, col2, col3 = st.beta_columns([1,2,0.5])

    with col1:
        st.write("")

    with col2:
        st.plotly_chart(fig)

    with col3:
        st.write("")

    


    st.markdown("<h1 style='text-align: center; color: #464e5f;'>Muéstrame los vuelos</h1>", unsafe_allow_html=True)
    st.table(dat.vuelazos(ciudad1,ciudad2,fecha_ida,fecha_vuelta))

    st.markdown("<h1 style='text-align: center; color: #464e5f;'>Muéstrame hoteles</h1>", unsafe_allow_html=True)
    dia_ida = fecha_ida.split("-")
    dia_ida = dia_ida[2]
    dia_vuelta = fecha_vuelta.split("-")
    dia_vuelta = dia_vuelta[2]
    st.table(dat.hotelazo(ciudad2,dia_ida,dia_vuelta))
    
    st.markdown("<h1 style='text-align: center; color: #464e5f;'>¿Qué puedo hacer en la ciudad?</h1>", unsafe_allow_html=True)
    x = ["","historic site","hotels","museum", "food","nightclub"]
    respuesta = st.selectbox('',x)
    respuesta = str(respuesta)
    df_planazos = dat.planazos(ciudad2)
    df_planazos = df_planazos[df_planazos["categoria"] == respuesta]
    df_planazos1 = df_planazos[["name","Address"]]
    st.table(df_planazos1)

    geolocator = Nominatim(user_agent="edu")
    location = geolocator.geocode(ciudad2)
    lat = location.latitude
    lon = location.longitude
    lat = str(lat)
    lon = str(lon)

    mapa = dat.folium_planes(df_planazos,lat,lon)
    col1, col2, col3 = st.beta_columns([1,2,0.5])

    with col1:
        st.write("")

    with col2:
        folium_static(mapa)

    with col3:
        st.write("")

    if st.button("Party"):
            st.balloons()
