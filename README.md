# Proyecto: Proceso ETL para Integración de Datos sobre Hoteles en Madrid

🚀📊 **Descripción del Proyecto** 📝
Este proyecto tiene como objetivo implementar un proceso de Extracción, Transformación y Carga (ETL) para procesar datos de dos fuentes principales. Una pagina de hoteles en madrid y otra sobre la comunidad de Madrid donde se indican eventos para el publico. Luego de la extraccion, lo conveniente fue almacenarlos en un destino estructurado. Se utilizan diversas herramientas y tecnologías para garantizar la eficiencia y escalabilidad del flujo de datos.

El proceso incluye:
- Extracción de datos desde diferentes fuentes (API, Scraping con Selenium y archivos CSV, etc.).
- Transformación y limpieza de datos aplicando reglas de negocio.
- Carga de datos en un destino estructurado (base de datos relacional en PostgreSQL).

🗂️ **Estructura del Proyecto**
```
    ├── data/ 
        ├──raw
            ├──reservas_hoteles.parquet           # Archivos de datos
        ├──eventos_relevantes.pkl                 #archivo de los eventos en madrid filtrado por las fecha de analisis
        ├──hoteles_competencia.csv                #hoteles de la competencia que tienen reservas
        ├──reservas_hoteles_final.pkl             #archivo de reservas limpio
    ├── notebooks/                                # Scripts ETL
    │   ├── 01.Carga_EDA_Transform.ipynb                    # Carga de datos, EDA y limpieza
    │   ├── 02.Scrapeo_selenium.ipynb             # Extracción de datos mediante Selenium
    │   ├── 03.Scrapeo_API.ipynb                  # Extracción de datos mediante API
    │   ├── 04.LoadSQL.ipynb                      # Carga de datos
    │   ├── 05.Bonus2_Analisis.ipynb              # Analisis BONUS
    ├── Querys_SQL/
    │   ├── Bonus1_QuerysSQL.sql                  # Querys de ejercicio Bonus            
    ├── src/                                      # Scripts ETL
    │   ├── LoadSQL.py                            # Carga de datos
    │   ├── Extract.py                            # Extracción de datos mediante API y Selenium
    │   ├── Transform.py                          # Limpieza de bbdd
    ├── README.md                                 # Descripción del proyecto
```

🔍 **Tecnologías Utilizadas**
- **Lenguaje**: Python, SQL
- **Librerías**: Pandas, Numpy, Psycopg2, Matplotlib, Seaborn
- **Base de Datos**: PostgreSQL 
   ```

📌 **Conclusiones y Resultados**
Se logro llegar al objetivo de Extraccion, Transformacion y Carga de los datos, pero el objetivo para proximos proyectos, es ordenar mejor el tema de definicion de funciones en .py y comenzar a utilizar menos los notebooks.

🤝 **Contribuciones**
Las contribuciones son bienvenidas para mejorar este análisis. Puedes proponer mejoras abriendo un pull request o creando una issue para discutir nuevas ideas.

✒️ **Autor**

**Agustin Salomon**

📌 **Contacto**
https://github.com/aSalomon96

mi LinkedIn https://www.linkedin.com/in/agustin-salomon/


Este proyecto es un ejercicio práctico para mejorar habilidades en ETL y procesamiento de datos. 🚀

