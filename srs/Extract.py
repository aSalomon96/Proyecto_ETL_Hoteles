import requests
import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC #para esperar a que ciertos eventos ocurran en la página web antes de continuar con la ejecución del script
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

######################################### APIS ###################################################
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

######################################### APIS ###################################################

################################### SCRAPING ######################################################
# Abrir la página
url = "https://all.accor.com/ssr/app/ibis/hotels/madrid-spain/open/index.en.shtml?compositions=1&stayplus=false&snu=false&hideWDR=false&accessibleRooms=false&hideHotelDetails=false&dateIn=2025-03-01&nights=1&destination=madrid-spain"

# Función para extraer información de los hoteles
def dictio_scrap_hotels(url):
    """_summary_
            Esta función extrae información de los hoteles de la página web de Accor.
            La información que extrae son los nombres de los hoteles, las estrellas y los precios.
    Args:
        url (_type_): _description_
    """
    dictio_hoteles = {
        "nombre_hotel": [],
        "estrellas": [],
        "precio_noche": []
    }
    # Configurar Selenium
    options = Options()
    options.add_argument("--no-sandbox")  # Evita errores en algunos entornos
    options.add_argument("--disable-dev-shm-usage")  # Mejora estabilidad
    service = Service(ChromeDriverManager().install())  # Webdriver automático
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url) # Esperar a que carguen los hoteles

    try:    #WebDriverWait(driver, 10) crea una instancia de WebDriverWait que esperará hasta 10 segundos para que se cumpla la condición especificada. 
            #La condición EC.presence_of_all_elements_located((By.CLASS_NAME, "xxx")) espera a que todos los elementos con la clase xxx estén presentes en el DOM.

        # Extraer información de los nombres de los hoteles
        titulo_hoteles = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "title")))
        
        for titulo in titulo_hoteles:
            dictio_hoteles["nombre_hotel"].append(titulo.text.split('\n')[0]) # INDICE 0 DE LA LISTA DE TITULOS

        # Extraer información de las reviews que seran las estrellas
        review_hoteles = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ratings__score")))
        
        for review in review_hoteles:
            dictio_hoteles["estrellas"].append(review.text.split('\n')[0].replace('/', '')) # INDICE 0 DE LA LISTA DE TITULOS

        # Extraer información de los precios
        precio_hoteles = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "rate-details__price-wrapper")))
        
        for precio in precio_hoteles:
            dictio_hoteles["precio_noche"].append(precio.text.split('\n')[1].replace("€",""))
     
    except Exception as e:
        print("No se pudo encontrar los elementos:", e)

    driver.quit()

# Asegurarse de que todas las listas tengan la misma longitud
    max_length = max(len(dictio_hoteles["nombre_hotel"]),len(dictio_hoteles["estrellas"]), len(dictio_hoteles["precio_noche"]))
    for key in dictio_hoteles:
        while len(dictio_hoteles[key]) < max_length:
            dictio_hoteles[key].append("N/A")
    
    return dictio_hoteles

    ################################### SCRAPING ######################################################