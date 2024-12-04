import sqlite3

# Conectar a la base de datos SQLite (se creará si no existe)
conn = sqlite3.connect('liga_espanyola_gps.db')  # Aquí se crea la base de datos
cursor = conn.cursor()

# Crear la tabla de estadísticas GPS para jugadores
cursor.execute('''
    CREATE TABLE IF NOT EXISTS jugadores_gps (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        partido TEXT NOT NULL,
        distancia_recorrida REAL,
        velocidad_media REAL,
        tiempo_jugado INTEGER,
        sprints INTEGER,
        calorias_quemadas REAL,
        pasos_totales INTEGER,
        zona_1 INTEGER,
        zona_2 INTEGER,
        zona_3 INTEGER
    )
''')

# Insertar los datos de los 15 jugadores (ejemplo ficticio)
jugadores_data = [
    ('Karim Benzema', 'Partido 1', 10800, 9.5, 90, 12, 750, 12000, 25, 35, 30),
    ('Lionel Messi', 'Partido 1', 11000, 10.0, 90, 15, 800, 12500, 20, 40, 30),
    ('Antoine Griezmann', 'Partido 1', 9500, 8.7, 88, 10, 600, 11500, 30, 45, 15),
    ('Sergio Ramos', 'Partido 1', 10500, 8.9, 90, 8, 700, 10000, 20, 30, 40),
    ('Gerard Piqué', 'Partido 1', 10200, 8.4, 85, 7, 650, 9500, 25, 30, 35),
    ('Joan Laporta', 'Partido 1', 9800, 8.2, 85, 9, 620, 10000, 28, 32, 40),
    ('Sergio Busquets', 'Partido 1', 10400, 8.5, 90, 6, 680, 9800, 22, 33, 35),
    ('César Azpilicueta', 'Partido 1', 10700, 9.0, 92, 13, 700, 11000, 20, 30, 50),
    ('David Alaba', 'Partido 1', 11050, 9.7, 90, 14, 780, 12050, 25, 35, 45),
    ('Vinícius Jr.', 'Partido 1', 11100, 9.9, 90, 16, 850, 13000, 22, 33, 50),
    ('Karim Benzema', 'Partido 2', 10900, 9.6, 91, 12, 760, 12200, 30, 35, 40),
    ('Frenkie de Jong', 'Partido 2', 10250, 8.8, 88, 10, 700, 11000, 18, 32, 45),
    ('Thibaut Courtois', 'Partido 2', 9300, 8.0, 85, 4, 500, 8000, 15, 22, 30),
    ('Luis Suárez', 'Partido 2', 10850, 9.3, 90, 13, 760, 11900, 23, 38, 45),
    ('Eden Hazard', 'Partido 2', 10400, 8.6, 87, 11, 720, 10700, 26, 35, 40),
]

# Insertar los datos en la tabla
cursor.executemany('''
    INSERT INTO jugadores_gps (nombre, partido, distancia_recorrida, velocidad_media, tiempo_jugado, sprints, calorias_quemadas, pasos_totales, zona_1, zona_2, zona_3)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
''', jugadores_data)

# Guardar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("Base de datos")
