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

st.write("""
# Mi súper Dashboard
Empieza el viaje 🚀🚀🚀
""")


ciudad1 = st.sidebar.text_input(

    "Selecciona una ciudad de salida"
)
ciudad1 = str(ciudad1)
ciudad2 = st.sidebar.text_input(

    "Selecciona una ciudad de vuelta"
)
ciudad2 = str(ciudad2)


fecha_ida = st.sidebar.text_input(

    "Selecciona que día vas a salir (yy-mm-dd)"
)
st.sidebar.write("Fecha salida", fecha_ida)

fecha_vuelta = st.sidebar.text_input(

    "Selecciona que día vas a volver (yy-mm-dd)"
)
st.sidebar.write("Fecha vuelta", fecha_vuelta)

fecha_ida = str(fecha_ida)
fecha_vuelta = str(fecha_vuelta)

if  ciudad1 != "" and ciudad2 != "" and fecha_ida != "" and fecha_vuelta != "":
    
    time.sleep(3)
    st.dataframe(dat.tiempazo(ciudad2))
    tiempo = dat.tiempazo(ciudad2)
    fig = px.line(tiempo, x=tiempo.date, y=tiempo.columns[1:3],template= "ggplot2")
    st.plotly_chart(fig)


    st.dataframe(dat.vuelazos(ciudad1,ciudad2,fecha_ida,fecha_vuelta))

    st.dataframe(dat.hotelazo(ciudad2,"17","18"))

