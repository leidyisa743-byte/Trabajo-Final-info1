# modules/db_config.py
# Autores: Gabriela Guevara Murcia, Leidy Zapata Hoyos, Isabela López Patiño, Isabella Arrieta Pacheco
# Descripción: Módulo de configuración centralizada para las credenciales de bases de datos (SQL y NoSQL).

import mysql.connector

# --- CONSTANTES DE CONFIGURACIÓN SQL (Local) ---
# Parámetros requeridos explícitamente en el PDF [cite: 121-124]
# Se utilizan para establecer la conexión con el servidor MySQL local.
DB_HOST = "localhost"
DB_USER = "informatica1"
DB_PASS = "info2025_2"
DB_NAME_SQL = "FP_Info1_2025_2"

# --- CONSTANTES DE CONFIGURACIÓN MONGO (Atlas Nube) ---
# Cadena de conexión (URI) para el clúster de MongoDB Atlas.
# Contiene el usuario 'leidyisa743_db_user' y la contraseña cifrada para acceso remoto.
MONGO_URI = "mongodb+srv://leidyisa743_db_user:2U8OJGpMv7RNNHrd@cluster0.ykqyrie.mongodb.net/?appName=Cluster0"

def get_mysql_connection():
    """
    Función: get_mysql_connection
    Descripción: Establece y retorna una conexión activa con la base de datos MySQL 
                 utilizando las credenciales globales definidas en este módulo.
    
    Proceso:
        Utiliza la librería mysql.connector para conectar al host local con el usuario
        y base de datos específicos del proyecto.
        
    Retorna:
        mysql.connector.connection.MySQLConnection: Objeto de conexión si es exitoso.
        (Lanza excepción mysql.connector.Error si falla la autenticación).
    """
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME_SQL
    )