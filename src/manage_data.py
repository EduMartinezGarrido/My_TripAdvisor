import requests
import re
import pandas as pd
import numpy as np
import time
import os
from dotenv import load_dotenv
load_dotenv()
import requests 
import json
from pandas import json_normalize
from geopy.geocoders import Nominatim
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def tiempazo(ciudad):
    
    #sacamos coordenadas
    geolocator = Nominatim(user_agent="edu")
    location = geolocator.geocode(f'{ciudad}')
    lat = location.latitude
    lon = location.longitude
    
    #usamos api
    api_key = os.getenv("Api_key")
    url_tiempo = f"https://api.tutiempo.net/json/?lan=es&apid={api_key}&ll={lat},{lon}"
    response = requests.get (url =  url_tiempo).json()
    
    dias_lista = ["day1","day2","day3","day4","day5","day6","day7"]
    dias = []
    for k,v in response.items():
        if k in dias_lista:
            dias.append(v)
            
    df =json_normalize(dias)
    df = df.drop(["moonrise","moonset","moon_phases_icon"], axis = 1)
    
    #añadimos emojis
    dicc = {1:"☀️",2:"🌤",4:"⛅️",6:"🌥",7:"☁️",9:"☁️",11:"💨",18:"🌧",19:"🌧",21:"⛈",22:"⛈",24:"🌧",25:"🌪",28:"🌨",29:"🌨",30:"🌨",33:"🌦",51:"🌦",54:"🌫"}

    df["icon"] = df["icon"].astype(int)
    df["icon"] = df["icon"].map(dicc)

    return df


def provincias():
    provincias= ["Álava", "Albacete", "Alicante", "Almería", "Asturias", "Ávila", "Badajoz", "Barcelona", "Burgos", "Cáceres", "Cádiz", "Cantabria", "Castellón", "Ciudad Real", "Córdoba", "Cuenca", "Gerona", "Granada", "Guadalajara", "Guipúzcoa", "Huelva", "Huesca", "Islas Baleares", "Jaén", "La Coruña", "La Rioja", "Las Palmas", "León", "Lérida", "Lugo", "Madrid", "Málaga", "Murcia", "Navarra", "Orense", "Palencia", "Pontevedra", "Salamanca", "Santa Cruz de Tenerife", "Segovia", "Sevilla", "Soria", "Tarragona", "Teruel", "Toledo", "Valencia", "Valladolid", "Vizcaya", "Zamora", "Zaragoza"]
    return provincias

def vuelazos(ciudad_ida,ciudad_vuelta,fecha_ida,fecha_vuelta):
    
    dicc = {"Alicante":"ALC","Almeria":"LEI","Badajoz":"BJZ","Barcelona":"BCN","Bilbao":"BIO","Burgos":"RGS","Castellon":"CDT",
    "Cordoba":"ODB","San_Sebastián":"EAS","Gerona":"GRO","Granada":"GRX","Fuerteventura":"FUE","Huesca":"HSK","Ibiza":"IBZ","Jerez":"XRZ",
    "Lanzarote":"ACE","Gran_Canaria":"LPA","La_Coruña":"LCG","La_Gomera":"GMZ","Leon":"LEN","Logroño":"RJL","Albacete":"ABC",
    "Madrid":"MAD","Malaga":"AGP","Melilla":"MLN","Menorca":"MAH","Murcia":"MJV","Asturias":"OVD","Mallorca":"PMI","La_Palma":"SPC",
    "Pamplona":"PNA","Reus":"REU","Sabadell":"QSA","Salamanca":"SLM","Santiago_de_Compostela":"SCQ","Santander":"SDR","Sevilla":"SVQ","Tenerife_Norte":"TFN",
    "Tenerife_Sur":"TFS","Valencia":"VLC","Valladolid":"VLL","El_Hierro":"VDE","Vigo":"VGO","Vitoria":"VIT","Zaragoza":"ZAZ"
           }
    
    options =  webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')

    driver = webdriver.Chrome("./chromedriver")
    URL = 'https://www.vuelosbaratos.es/Buscar/'
    driver.get(URL + dicc.get(f'{ciudad_ida}')+'-'+dicc.get(f'{ciudad_vuelta}')+'/'+ f'{fecha_ida}'+'/'+f'{fecha_vuelta}'+'/ES/')
    time.sleep(3)
    
    # Precio Vuelos
    precio = driver.find_elements_by_class_name("ResultPrice")

    precios = []
    for i in precio[::2]:
        precios.append(i.text)

    precios[:3]

    ## Salida Vuelos

    fecha = driver.find_elements_by_class_name("groupDetailsCell")
    fechass = []
    for i in fecha:
        fechass.append(i.text)
    
    fechas = []
    for i in fechass:
        i = i[-5:]
        fechas.append(i)

    salida = []
    for i in fechas[::2]:
        salida.append(i)   

    salida_ida = []
    for i in salida[::2]:
        i = i.replace("\n"," ")
        salida_ida.append(i)

    salida_vuelta = []
    for i in salida[1::2]:
        i = i.replace("\n"," ")
        salida_vuelta.append(i)

    llegada = []
    for i in fechas[1::2]:
        llegada.append(i)

    llegada_ida = []
    for i in llegada[::2]:
        i = i.replace("\n"," ")
        llegada_ida.append(i)

    llegada_vuelta = []
    for i in llegada[1::2]:
        i = i.replace("\n"," ")
        llegada_vuelta.append(i)
    
    driver.quit()
    
    df = pd.DataFrame(list(zip(precios,salida_ida,llegada_ida,salida_vuelta,llegada_vuelta)), columns = ['Precio',f'Salida_{ciudad_ida}',f'Llegada_{ciudad_vuelta}',f'Salida_{ciudad_vuelta}',f'Llegada_{ciudad_ida}'])
    
    return df

def hotelazo(ciudad,check_in,check_out):
    opciones=Options()

    opciones.add_experimental_option('excludeSwitches', ['enable-automation'])
    opciones.add_experimental_option('useAutomationExtension', False)

    opciones.headless=False    # si True, no aperece la ventana (headless=no visible)

    opciones.add_argument('--start-maximized')         # comienza maximizado

    #opciones.add_argument('--incognito')              # incognito

    url='https://www.atrapalo.com/'
    PATH= './chromedriver'
    driver = webdriver.Chrome(PATH, options=opciones)


    driver.get(url)
    time.sleep(3)

    cookies=driver.find_element_by_xpath('//*[@id="CybotCookiebotDialogBodyButtonAccept"]')
    cookies.click()

    hoteles=driver.find_element_by_xpath('//*[@id="content"]/section[1]/div/ul/li[5]/a/span')
    hoteles.click()

    time.sleep(3)

    buscar=driver.find_element_by_xpath('//*[@id="search_engine_HOT_destiny"]')
    buscar.send_keys(ciudad)
    buscar.submit()

    time.sleep(3)

    fecha=driver.find_element_by_xpath('//*[@id="searchDates"]')
    fecha.click()

    entrada=driver.find_element_by_xpath('//*[@id="finderContainer"]/div/form/div/div[1]/div[2]/div/div[1]/label')
    entrada.click()

    mes_1=driver.find_element_by_class_name('month1')

    for m in mes_1.find_elements_by_tag_name('td'):

        if m.text== check_in:
            m.click()

        elif m.text== check_out:
            m.click()


    aceptar=driver.find_element_by_xpath('//*[@id="submitFormButton"]')
    aceptar.click()

    texto_columnas = driver.find_element_by_class_name('hotels-list.box-resultados')

    #Sacamos nombre hotel
    nombre = []
    while range(2):
        time.sleep(5)
        texto_hoteles = driver.find_elements_by_class_name('openFontSemiBold')
        time.sleep(5)
        texto_hoteles = texto_hoteles[:4]
        for i in texto_hoteles:
                nombre.append(i.text)
        break

    ## Sacar Precio

    time.sleep(6)
    texto_precio = texto_columnas.find_elements_by_class_name('value')
    texto_precio = texto_precio[0:4]

    precio = []
    for i in texto_precio:
        precio.append(i.text)

    ## Sacar dirección

    hotel = driver.find_elements_by_class_name('product-name')

    direcc = []
    for i in hotel:
        primero = i.get_attribute("href")
        direcc.append(primero)

    direcc = direcc[0:4]

    driver.quit()

    time.sleep(5)
    address = []
    for link in direcc:
        driver = webdriver.Chrome("./chromedriver")
        driver.get(link)
        time.sleep(3)
        calle = driver.find_element_by_css_selector("span.app-address")
        calle = calle.text
        address.append(calle)
        driver.quit()
    '''
    latitud = []
    longitud = []
    for i in address:
        geolocator = Nominatim(user_agent="edu", timeout=5)
        location = geolocator.geocode(i)
        lat = location.latitude
        lon = location.longitude
        latitud.append(lat)
        longitud.append(lon)'''

    
    df = pd.DataFrame(list(zip(nombre,precio,address)), columns = ['Nombre','Precio','Direccion'])
    return df