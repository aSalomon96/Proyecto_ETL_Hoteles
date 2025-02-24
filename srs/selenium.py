import pandas as pd 
import numpy as np  
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC #para esperar a que ciertos eventos ocurran en la página web antes de continuar con la ejecución del script
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

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

# Ensure all lists in the dictionary have the same length
    max_length = max(len(dictio_hoteles["nombre_hotel"]),len(dictio_hoteles["estrellas"]), len(dictio_hoteles["precio_noche"]))
    for key in dictio_hoteles:
        while len(dictio_hoteles[key]) < max_length:
            dictio_hoteles[key].append("N/A")
    
    return dictio_hoteles