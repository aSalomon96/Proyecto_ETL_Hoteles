import pandas as pd
import numpy as np
import psycopg2

cur = conn.cursor()

cur.execute("SELECT version();")
# Fetch and print the result
print(cur.fetchall())


conn.rollback()

query1 = """
    CREATE TABLE ciudad (
    id_ciudad SERIAL PRIMARY KEY,
    nombre_ciudad TEXT
    );
"""
cur.execute(query1)
conn.commit()  # Commit para saber si se guardan correctamente la tabla


conn.rollback()
query2 = """CREATE TABLE eventos (
    id_evento SERIAL PRIMARY KEY,
    nombre_evento TEXT,
    url_evento TEXT,
    codigo_postal INT,
    direccion TEXT,
    horario TEXT,
    fecha_inicio DATE,
    fecha_fin DATE,
    organizacion TEXT,
    id_ciudad INT REFERENCES ciudad(id_ciudad) ON DELETE CASCADE
);
CREATE TABLE hoteles (
    id_hotel SERIAL PRIMARY KEY, -- Puede ser VARCHAR(5)
    nombre_hotel TEXT,
    competencia BOOL,
    valoracion FLOAT CHECK (valoracion BETWEEN 1 AND 5),
    id_ciudad INT REFERENCES ciudad(id_ciudad) ON DELETE CASCADE
);
CREATE TABLE clientes (
    id_cliente VARCHAR(50) PRIMARY KEY,
    nombre TEXT,
    apellido TEXT,
    mail TEXT UNIQUE CHECK (mail LIKE '%@%')
);
CREATE TABLE reservas (
    id_reserva VARCHAR(50) PRIMARY KEY,
    fecha_reserva DATE,
    inicio_estancia DATE,
    final_estancia DATE,
    precio_noche FLOAT CHECK (precio_noche >= 0),
    id_cliente VARCHAR(50) REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    id_hotel INT REFERENCES hoteles(id_hotel) ON DELETE CASCADE
    
);"""

cur.execute(query2)
conn.commit()  # Ahora que sabemos que se guarda la primer tabla guardamos el resto

#importamos los datos que insertaremos en la base de datos
df_reservas = pd.read_pickle("../data/reservas_hoteles_final.pkl")
df_eventos = pd.read_pickle("../data/eventos_relevantes.pkl")

############################################################################################################
# para la tabla de eventos agregamos un id de evento serial 
df_eventos["id_evento"] = np.arange(1, len(df_eventos) + 1)

conn.rollback()
# insertamos los datos en la tabla de ciudad 
cur.execute("INSERT INTO ciudad (nombre_ciudad) VALUES ('Madrid')")
conn.commit()

conn.rollback()

data_eventos = []
for _, row in df_eventos.iterrows():
    id_evento = row["id_evento"]
    nombre_evento = row["nombre_evento"]
    url_evento = row["url_evento"]
    codigo_postal = int(row["codigo_postal"]) if pd.notna(row["codigo_postal"]) else None
    direccion = row["direccion"]
    horario = row["horario"]
    fecha_inicio = pd.to_datetime(row["inicio_evento"])
    fecha_fin = pd.to_datetime(row["fin_evento"])
    organizacion = row["organizacion"]
    ciudad = row["ciudad"]
    id_ciudad = 2

    # Mueve el append dentro del bucle
    data_eventos.append([id_evento, nombre_evento, url_evento, codigo_postal, direccion, horario, fecha_inicio, fecha_fin, organizacion, id_ciudad]) 

# Verifica que la lista no esté vacía
if not data_eventos:
    raise ValueError("La lista data_eventos está vacía. Verifica df_eventos.")

# Crear DataFrame
tabla_eventos = pd.DataFrame(data_eventos, columns=["id_evento", "nombre_evento", "url_evento", "codigo_postal", "direccion", "horario", "inicio_evento", "fin_evento", "organizacion", "id_ciudad"])
print(tabla_eventos.head())  # Para depuración

# Query de inserción
insert_query = """
INSERT INTO eventos (id_evento, nombre_evento, url_evento, codigo_postal, direccion, horario, fecha_inicio, fecha_fin, organizacion, id_ciudad)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (id_evento) DO NOTHING;
                """

# Verifica que haya datos antes de la inserción
if data_eventos:
    cur.executemany(insert_query, data_eventos)
    conn.commit()
else:
    print("No hay datos para insertar en la tabla eventos.")

############################################################################################################
# Data frame hoteles y tabla SQL hoteles
#separamos el df de hoteles propios para hacer el average de valoracion que tienen
df_propios = df_reservas[df_reservas['competencia'] == False]

df_propios_agrupados = df_propios.groupby(['id_hotel','nombre_hotel', 'competencia']).agg({'estrellas':'mean'}).round(2).reset_index()
df_propios_agrupados

df_competencia = df_reservas[df_reservas['competencia'] == True]
df_competencia_agrupados = df_competencia.groupby(['id_hotel','nombre_hotel', 'competencia']).agg({'estrellas':'mean'}).round(2).reset_index()

# unificamos los dos dataframes
df_hoteles = pd.concat([df_propios_agrupados, df_competencia_agrupados])

# ahora cambiamos el nombre de la columna estrella por valoracion
df_hoteles.rename(columns = {'estrellas':'valoracion'}, inplace = True)

# bucle para asignar valores a cada columna de la tabla
conn.rollback()

data_hoteles = []
for _, row in df_hoteles.iterrows():
    id_hotel = row["id_hotel"]
    nombre_hotel = row["nombre_hotel"]
    competencia = row["competencia"]
    valoracion = float(row["valoracion"]) if pd.notna(row["valoracion"]) else None

    # Mueve el append dentro del bucle
    data_hoteles.append([id_hotel, nombre_hotel, competencia, valoracion]) 

# Verifica que la lista no esté vacía
if not data_hoteles:
    raise ValueError("La lista data_eventos está vacía. Verifica df_eventos.")

# Crear DataFrame
tabla_hoteles = pd.DataFrame(data_hoteles, columns=["id_hotel", "nombre_hotel", "competencia", "valoracion"])

#subimos a la bbdd
conn.rollback()

# Query de inserción
insert_query = """
INSERT INTO hoteles (id_hotel, nombre_hotel, competencia, valoracion)
VALUES (%s, %s, %s, %s);
                """
# Verifica que haya datos antes de la inserción
if data_hoteles:
    cur.executemany(insert_query, data_hoteles)
    conn.commit()
else:
    print("No hay datos para insertar en la tabla eventos.")


# Data frame hoteles le agregamos la columna id_ciudad
conn.rollback()
# agregamos query de id_ciudad para la tabla de hoteles
query = """
UPDATE hoteles
SET id_ciudad = 2;
"""
cur.execute(query)
conn.commit()
############################################################################################################
## Tabla de clientes
df_clientes = df_reservas[['id_cliente','nombre','apellido','mail']]

#eliminamos los duplicado de "id_cliente" y "mail"
df_clientes_limpio = df_clientes.drop_duplicates(subset=['id_cliente','mail'])

#instanciamos para subir a base de datos
data_clientes = []
for _, row in df_clientes_limpio.iterrows():
    id_cliente = row["id_cliente"]
    nombre = row["nombre"]
    apellido = row["apellido"]
    mail = row["mail"]

    # Mueve el append dentro del bucle
    data_clientes.append([id_cliente, nombre, apellido, mail])

conn.rollback()

 # Query de inserción
insert_query = """
 INSERT INTO clientes (id_cliente, nombre, apellido, mail)
 VALUES (%s, %s, %s, %s);
                """
# Verifica que haya datos antes de la inserción
if data_clientes:
    cur.executemany(insert_query, data_clientes)
    conn.commit()
else:
    print("No hay datos para insertar en la tabla eventos.")

############################################################################################################

# Tabla de reservas
# ahora comenzamos a ordenar los datos para subir las reservas en los hoteles
# agrupamos por reservas
df_reservas_agrupadas = df_reservas.groupby(['id_reserva','fecha_reserva','inicio_estancia','final_estancia','precio_noche','id_cliente','id_hotel']).agg({'competencia':'first'}).reset_index()
# instanciamos para subir a la base de datos
data_reservas = []
for _, row in df_reservas_agrupadas.iterrows():
    id_reserva = row["id_reserva"]
    fecha_reserva = pd.to_datetime(row["fecha_reserva"])
    inicio_estancia = pd.to_datetime(row["inicio_estancia"])
    final_estancia = pd.to_datetime(row["final_estancia"])
    precio_noche = float(row["precio_noche"]) if pd.notna(row["precio_noche"]) else None
    id_cliente = row["id_cliente"]
    id_hotel = row["id_hotel"]

    # Mueve el append dentro del bucle
    data_reservas.append([id_reserva, fecha_reserva, inicio_estancia, final_estancia, precio_noche, id_cliente, id_hotel])
    conn.rollback()

# Query de inserción
insert_query = """
INSERT INTO reservas (id_reserva, fecha_reserva, inicio_estancia, final_estancia, precio_noche, id_cliente, id_hotel)
VALUES (%s, %s, %s, %s, %s, %s, %s);
                """
# Verifica que haya datos antes de la inserción
if data_reservas:
    cur.executemany(insert_query, data_reservas)
    conn.commit()
else:
    print("No hay datos para insertar en la tabla eventos.")