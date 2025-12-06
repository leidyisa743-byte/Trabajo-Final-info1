# modules/sql_manager.py
# Autores: Gabriela Guevara Murcia, Leidy Zapata Hoyos, Isabela López Patiño, Isabella Arrieta Pacheco
# Descripción: Módulo encargado de las operaciones CRUD (Crear, Leer, Actualizar, Borrar) 
#              en la base de datos relacional MySQL.

from .db_config import get_mysql_connection

def crear_usuario(id_usr, nombre, edad, correo, rol):
    """
    Función: crear_usuario
    Descripción: Registra un nuevo usuario en la tabla 'usuarios' de MySQL.
                 Esta función da soporte a la gestión de usuarios por parte del administrador.
    
    Argumentos:
        id_usr (str): Identificación única del usuario.
        nombre (str): Nombre completo.
        edad (int): Edad del usuario.
        correo (str): Correo electrónico de contacto.
        rol (str): Rol asignado en el sistema ('admin' o 'usuario').
        
    Proceso:
        1. Establece conexión con MySQL.
        2. Ejecuta una sentencia INSERT parametrizada para prevenir inyección SQL.
        3. Confirma los cambios (commit).
        
    Retorna:
        bool: True si el registro fue exitoso, False si ocurrió un error (ej. ID duplicado).
    """
    conn = get_mysql_connection()
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO usuarios (id, nombre, edad, correo, rol) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (id_usr, nombre, edad, correo, rol))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error SQL al crear usuario: {e}")
        return False
    finally:
        conn.close()

def obtener_usuario_por_id(id_usr):
    """
    Función: obtener_usuario_por_id
    Descripción: Busca y retorna la información completa de un usuario específico.
                 Utilizada principalmente durante el proceso de Login para validar existencia y rol.
    
    Argumentos:
        id_usr (str): ID del usuario a buscar.
        
    Retorna:
        dict: Diccionario con los datos del usuario (id, nombre, edad, rol) si existe.
        None: Si el usuario no se encuentra en la base de datos.
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id_usr,))
        res = cursor.fetchone()
        conn.close()
        return res
    except Exception as e:
        print(f"Error SQL al obtener usuario: {e}")
        return None

def insertar_registro_diario(id_usr, fecha, sueno, animo, actividad, sintomas):
    """
    Función: insertar_registro_diario
    Descripción: Almacena el reporte diario de salud de un usuario en la tabla 'registros_diarios'.
                 Captura métricas cuantitativas (sueño, ánimo) y cualitativas (síntomas).
    
    Argumentos:
        id_usr (str): ID del usuario que reporta.
        fecha (str): Fecha del registro (YYYY-MM-DD).
        sueno (float): Horas de sueño dormidas.
        animo (int): Calificación del estado de ánimo (1-10).
        actividad (str): Descripción de la actividad física realizada.
        sintomas (str): Descripción de síntomas presentados.
        
    Retorna:
        bool: True si se guardó correctamente, False en caso de error.
    """
    conn = get_mysql_connection()
    cursor = conn.cursor()
    try:
        sql = """INSERT INTO registros_diarios 
                 (id_usuario, fecha, horas_sueno, estado_animo, actividad_fisica, sintomas) 
                 VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, (id_usr, fecha, sueno, animo, actividad, sintomas))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error SQL al insertar registro diario: {e}")
        return False
    finally:
        conn.close()

def obtener_historial_salud(id_usr):
    """
    Función: obtener_historial_salud
    Descripción: Recupera todos los registros de salud históricos de un usuario,
                 ordenados cronológicamente de más reciente a más antiguo.
                 
    Argumentos:
        id_usr (str): ID del usuario a consultar.
        
    Retorna:
        list: Lista de diccionarios con los registros de salud para su visualización o análisis.
    """
    try:
        conn = get_mysql_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM registros_diarios WHERE id_usuario = %s ORDER BY fecha DESC", (id_usr,))
        res = cursor.fetchall()
        conn.close()
        return res
    except Exception as e:
        print(f"Error SQL al obtener historial: {e}")
        return []