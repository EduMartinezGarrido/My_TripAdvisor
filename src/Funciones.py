import requests 
import json
import os
import pandas as pd
from dotenv import load_dotenv
from functools import reduce
import operator

def get_data (latitude, longitude, url_query, *args):
    d = {}
    tok1= os.getenv("Client_Id")
    tok2= os.getenv("Client_Secret")
    
    for i in args: 
        parametros = {"client_id" : tok1,
                  "client_secret" : tok2,
                  "v": "20180323",
                  "ll": f"{latitude},{longitude}", 
                  "query":i,
                  "limit": 100}  

        response = requests.get(url= url_query, params=parametros)
        data = json.loads(response.text)        
        d[i] = data
        
    return d

def getFromDict(diccionario,mapa):
    return reduce (operator.getitem,mapa,diccionario)

def crear_dataframe(diccionario):
    mapa_nombre =  ["venue", "name"]
    mapa_latitud = ["venue", "location", "lat"]
    mapa_longitud = ["venue", "location", "lng"]
    lista = []
    for dic in diccionario:
        paralista = {}
        paralista["name"] = getFromDict(dic, mapa_nombre)
        paralista["latitud"]= getFromDict(dic, mapa_latitud)
        paralista["longitud"] = getFromDict(dic,mapa_longitud)
        lista.append(paralista)
        df = pd.DataFrame(lista)
    return df