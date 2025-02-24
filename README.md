# Proyecto: Proceso ETL para Integración de Datos sobre Hoteles en Madrid

🚀📊 **Descripción del Proyecto** 📝
Este proyecto tiene como objetivo implementar un proceso de Extracción, Transformación y Carga (ETL) para procesar datos de diversas fuentes y almacenarlos en un destino estructurado. Se utilizan diversas herramientas y tecnologías para garantizar la eficiencia y escalabilidad del flujo de datos.

El proceso incluye:
- Extracción de datos desde diferentes fuentes (API, Scraping con Selenium y archivos CSV, etc.).
- Transformación y limpieza de datos aplicando reglas de negocio.
- Carga de datos en un destino estructurado (base de datos relacional).

🗂️ **Estructura del Proyecto**
```
    ├── data/ 
        ├──eventos_relevantes.pkl           #archivo de los eventos en madrid filtrado por las fecha de analisis
        ├──hoteles_competencia.csv          #hoteles de la competencia que tienen reservas
        ├──reservas_hoteles_final.pkl       #archivo de reservas limpio
        ├──raw
            ├──reservas_hoteles.parquet     # Archivos de datos
    ├── notebooks/                                # Scripts ETL
    │   ├── 01.Carga_EDA.ipynb                    # Carga de datos, EDA y limpieza
    │   ├── 02.Scrapeo_selenium.ipynb             # Extracción de datos mediante Selenium
    │   ├── 03.Scrapeo_API.ipynb                  # Extracción de datos mediante API
    │   ├── 04.LoadSQL.ipynb                      # Carga de datos 
    ├── src/                                # Scripts ETL
    │   ├── LoadSQL.py                    # Carga de datos
    │   ├── scrap_api.py                    # Extracción de datos mediante API
    │   ├── selenium.py                     # Extracción de datos mediante Selenium
    ├── README.md                           # Descripción del proyecto
```

🔍 **Tecnologías Utilizadas**
- **Lenguaje**: Python, SQL
- **Librerías**: Pandas, Numpy, Psycopg2, Matplotlib, Seaborn
- **Base de Datos**: PostgreSQL 
   ```

📌 **Conclusiones y Resultados**
El desarrollo de este proceso ETL permite una integración eficiente y estructurada de datos. Se lograron los siguientes beneficios:
- **Automatización**: Reducción del esfuerzo manual en la recolección y transformación de datos.
- **Eficiencia**: Mejora en los tiempos de procesamiento y carga de datos.
- **Escalabilidad**: Posibilidad de adaptar el pipeline a nuevas fuentes y formatos de datos.

🤝 **Contribuciones**
Las contribuciones son bienvenidas para mejorar este análisis. Puedes proponer mejoras abriendo un pull request o creando una issue para discutir nuevas ideas.

✒️ **Autor**
[Nombre del equipo/desarrollador]

📌 **Contacto**
- [LinkedIn](#)
- [GitHub](#)

Este proyecto es un ejercicio práctico para mejorar habilidades en ETL y procesamiento de datos. 🚀

