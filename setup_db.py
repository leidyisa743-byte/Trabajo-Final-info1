# setup_db.py
# Autores: Gabriela Guevara Murcia, Leidy Zapata Hoyos, Isabela López Patiño, Isabella Arrieta Pacheco
# Descripción: Script de configuración inicial (Bootstrapping). 
#              Se encarga de provisionar la base de datos SQL, cargar datos semilla desde JSON
#              y sincronizar datos iniciales con MongoDB Atlas.

import mysql.connector
import csv
import os
import json
import getpass 
from modules.db_config import DB_HOST, DB_USER, DB_PASS, DB_NAME_SQL
from modules.mongo_manager import insertar_nota, insertar_archivo_adjunto

def cargar_datos_desde_json(archivo):
    """
    Función: cargar_datos_desde_json
    Descripción: Lee archivos de datos semilla ubicados en la carpeta 'data_seed'.
    
    Argumentos:
        archivo (str): Nombre del archivo JSON a leer.
        
    Retorna:
        list: Lista de diccionarios con los datos cargados, o lista vacía si falla.
    """
    ruta = os.path.join("data_seed", archivo)
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️ Advertencia: No se encontró {ruta}")
        return []

def crear_usuario_si_no_existe():
    """
    Función: crear_usuario_si_no_existe
    Descripción: Verifica la existencia del usuario de base de datos requerido por el proyecto.
                 Si no existe (Error 1045), solicita credenciales de ROOT temporalmente para crearlo.
    
    Proceso:
        1. Intenta conexión con las credenciales del proyecto.
        2. Si falla por acceso denegado, solicita password de root mediante getpass.
        3. Ejecuta sentencias DCL (CREATE USER, GRANT ALL) para configurar el entorno.
        
    Retorna:
        bool: True si el usuario existe o fue creado exitosamente, False si falla.
    """
    try:
        # Validación de conexión inicial
        test_conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASS)
        test_conn.close()
        print(f"✅ Usuario '{DB_USER}' detectado. Continuando...")
        return True
    except mysql.connector.Error as err:
        # Manejo de error 1045: Acceso denegado (Usuario no existe)
        if err.errno == 1045:
            print(f"\n⚠️ El usuario '{DB_USER}' no existe o la contraseña es incorrecta.")
            print("   Se requiere acceso temporal de ROOT para la configuración inicial.")
            
            # Solicitud segura de credenciales
            root_pass = getpass.getpass("🔑 Por favor, ingrese su contraseña de MySQL ROOT: ")
            
            try:
                # Elevación de privilegios para creación de usuario
                root_conn = mysql.connector.connect(host=DB_HOST, user="root", password=root_pass)
                cursor = root_conn.cursor()
                
                print(f"⚙️ Creando usuario '{DB_USER}'...")
                cursor.execute(f"CREATE USER IF NOT EXISTS '{DB_USER}'@'localhost' IDENTIFIED BY '{DB_PASS}';")
                cursor.execute(f"GRANT ALL PRIVILEGES ON *.* TO '{DB_USER}'@'localhost';")
                cursor.execute("FLUSH PRIVILEGES;")
                
                root_conn.close()
                print(f"✅ Usuario '{DB_USER}' creado exitosamente con permisos.")
                return True
            except Exception as e:
                print(f"❌ Error al intentar crear usuario con ROOT: {e}")
                return False
        else:
            print(f"❌ Error de conexión desconocido: {err}")
            return False

def setup():
    """
    Función: setup
    Descripción: Orquestador principal de la instalación. Ejecuta la creación de bases de datos,
                 tablas y la carga masiva de datos (Batch Insert) desde los archivos JSON.
    """
    print(f"--- CONFIGURACIÓN PROFESIONAL DE {DB_NAME_SQL} ---")
    
    # 1. Verificación de privilegios de usuario
    if not crear_usuario_si_no_existe():
        print("❌ No se pudo configurar el usuario de base de datos. Abortando instalación.")
        return

    # 2. Carga de datos semilla en memoria
    usuarios_data = cargar_datos_desde_json("usuarios.json")
    registros_data = cargar_datos_desde_json("registros_sql.json")
    notas_data = cargar_datos_desde_json("notas_mongo.json")

    # ---------------------------------------------------------
    # PROVISIÓN SQL (MySQL)
    # ---------------------------------------------------------
    try:
        # Creación de la Base de Datos (DDL)
        conn_init = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASS)
        cursor_init = conn_init.cursor()
        cursor_init.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME_SQL}")
        conn_init.close()
        print(f"✅ Base de datos '{DB_NAME_SQL}' verificada/creada.")

        # Conexión a la DB y creación de esquema
        conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME_SQL)
        cursor = conn.cursor()
        
        # Reinicio de tablas (DROP/CREATE)
        cursor.execute("DROP TABLE IF EXISTS registros_diarios")
        cursor.execute("DROP TABLE IF EXISTS usuarios")
        
        cursor.execute("""
            CREATE TABLE usuarios (
                id VARCHAR(20) PRIMARY KEY,
                nombre VARCHAR(100),
                edad INT,
                correo VARCHAR(100),
                rol VARCHAR(20)
            )
        """)
        cursor.execute("""
            CREATE TABLE registros_diarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                id_usuario VARCHAR(20),
                fecha DATE,
                horas_sueno FLOAT,
                estado_animo INT,
                actividad_fisica VARCHAR(200),
                sintomas VARCHAR(200),
                FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
            )
        """)

        # Inserción masiva de datos (Usuarios)
        print(f"🔄 Cargando {len(usuarios_data)} usuarios a SQL...")
        sql_user = "INSERT INTO usuarios (id, nombre, edad, correo, rol) VALUES (%s, %s, %s, %s, %s)"
        for u in usuarios_data:
            cursor.execute(sql_user, (u['id'], u['nombre'], u['edad'], u['correo'], u['rol']))

        # Inserción masiva de datos (Registros de Salud)
        print(f"🔄 Cargando {len(registros_data)} registros de salud a SQL...")
        sql_reg = """INSERT INTO registros_diarios 
                     (id_usuario, fecha, horas_sueno, estado_animo, actividad_fisica, sintomas) 
                     VALUES (%s, %s, %s, %s, %s, %s)"""
        for r in registros_data:
            cursor.execute(sql_reg, (r['id_usuario'], r['fecha'], r['horas_sueno'], r['estado_animo'], r['actividad_fisica'], r['sintomas']))
        
        conn.commit()
        conn.close()
        print("✅ MySQL listo (Tablas y Datos).")

        # Generación de archivo de credenciales CSV
        if not os.path.exists('data'): os.makedirs('data')
        with open('data/passwords.csv', 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['id_usuario', 'password'])
            for u in usuarios_data:
                w.writerow([u['id'], u['password']])
        print("✅ CSV de passwords generado.")

    except Exception as e:
        print(f"❌ Error SQL CRÍTICO: {e}")
        raise e 

    # ---------------------------------------------------------
    # PROVISIÓN NOSQL (MongoDB Atlas)
    # ---------------------------------------------------------
    try:
        print(f"🔄 Cargando notas a MongoDB Atlas...")
        count = 0
        for n in notas_data:
            # Reutiliza la lógica del manager para inserción segura en la nube
            if insertar_nota(n['id_usuario'], n['texto'], n['etiquetas'], n['estado_animo'], n.get('ubicacion', 'Medellín')):
                count += 1
        print(f"✅ {count} notas insertadas en Atlas.")
        
        # Inserción de archivo adjunto de prueba
        metadatos_file = {"fuente": "setup", "tamano": "1MB"}
        insertar_archivo_adjunto("123", "/uploads/demo.jpg", "imagen", "Archivo Demo", metadatos_file)
        
    except Exception as e:
        print(f"❌ Error Mongo: {e}")

if __name__ == "__main__":
    setup()