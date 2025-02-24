import requests
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from datetime import datetime

# Cargar las variables de entorno
load_dotenv()
API_URL = os.getenv("API_URL")

# Función para obtener datos desde la API
def obtener_datos_api(url):
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()  # Lanza un error si la solicitud falla
        return respuesta.json()
    except requests.RequestException as e:
        print(f"Error al obtener datos: {e}")
        return None

datos = obtener_datos_api(API_URL)
if datos:
    print(f"Claves disponibles en la respuesta: {list(datos.keys())}")
    
    # Obtener fecha del primer evento
    eventos = datos.get('@graph', [])
    if eventos:
        fecha_evento = pd.to_datetime(eventos[0].get('dtstart', np.nan))
        print(f"Fecha del primer evento: {fecha_evento}")

# Cargar dataset local
ruta_datos = "../data/reservas_hoteles_final.pkl"
df_reservas = pd.read_pickle(ruta_datos)

fecha_inicio_reserva = pd.to_datetime(df_reservas.loc[0, "inicio_estancia"])
fecha_fin_reserva = pd.to_datetime(df_reservas.loc[0, "final_estancia"])
print(f"Rango de reservas: {fecha_inicio_reserva} - {fecha_fin_reserva}")

# Función para filtrar eventos dentro del rango de reserva
def filtrar_eventos(datos_eventos, fecha_inicio, fecha_fin): 
    eventos_filtrados = [] # Lista para almacenar los eventos filtrados
    
    for evento in datos_eventos.get("@graph", []): # Iterar sobre los eventos
        inicio_evento = pd.to_datetime(evento.get('dtstart', np.nan))
        fin_evento = pd.to_datetime(evento.get('dtend', np.nan))
        
        if inicio_evento <= fecha_inicio and fin_evento >= fecha_fin: # Evento dentro del rango
            eventos_filtrados.append({
                "nombre_evento": evento.get('title', 'Desconocido'), 
                "url_evento": evento.get('link', np.nan),
                "codigo_postal": evento.get("address", {}).get("area", {}).get("postal-code", np.nan),
                "direccion": evento.get("address", {}).get("area", {}).get("street-address", np.nan),
                "horario": evento.get("time", np.nan),
                "organizacion": evento.get('organization', {}).get('organization-name', np.nan),
                "inicio_evento": inicio_evento.date() if not pd.isna(inicio_evento) else np.nan,
                "fin_evento": fin_evento.date() if not pd.isna(fin_evento) else np.nan,
                "ciudad": "Madrid"
            })
    
    return eventos_filtrados

# Filtrar y mostrar eventos
eventos_relevantes = filtrar_eventos(datos, fecha_inicio_reserva, fecha_fin_reserva)
df_eventos = pd.DataFrame(eventos_relevantes)

# Pasar a fecha inicio y fin de evento
df_eventos["inicio_evento"] = pd.to_datetime(df_eventos["inicio_evento"])
df_eventos["fin_evento"] = pd.to_datetime(df_eventos["fin_evento"])

df_eventos.to_pickle("../data/eventos_relevantes.pkl")