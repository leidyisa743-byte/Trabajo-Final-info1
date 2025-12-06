# modules/mongo_manager.py
# Autores: Gabriela Guevara Murcia, Leidy Zapata Hoyos, Isabela López Patiño, Isabella Arrieta Pacheco
# Descripción: Módulo para la gestión de datos no estructurados en MongoDB Atlas (Notas y Archivos).

from pymongo import MongoClient
from datetime import datetime
from .db_config import DB_NAME_SQL, MONGO_URI 

def get_db():
    """
    Función: get_db
    Descripción: Establece la conexión con el clúster de MongoDB Atlas utilizando
                 la URI de configuración global.
    
    Proceso:
        Utiliza el cliente MongoClient con la cadena de conexión remota para
        acceder a la base de datos definida en el proyecto.
        
    Retorna:
        Database: Objeto de base de datos de MongoDB si la conexión es exitosa.
        None: Si ocurre un error de conexión.
    """
    try:
        client = MongoClient(MONGO_URI)
        return client[DB_NAME_SQL]
    except Exception as e:
        print(f"Error conectando a Atlas: {e}")
        return None

def insertar_nota(id_usr, texto, etiquetas, animo, ubicacion="Medellín"):
    """
    Función: insertar_nota
    Descripción: Inserta un documento de nota personal en la colección 'notas_personales'.
                 Cumple con el requisito de almacenamiento de datos no estructurados[cite: 82].
    
    Argumentos:
        id_usr (str): ID del usuario propietario de la nota.
        texto (str): Contenido textual de la nota.
        etiquetas (list): Lista de palabras clave (tags).
        animo (int): Calificación del estado de ánimo (1-10).
        ubicacion (str): Lugar del registro (por defecto 'Medellín').
        
    Proceso:
        1. Construye un diccionario con la estructura JSON requerida.
        2. Inserta el documento usando insert_one().
        
    Retorna:
        bool: True si la inserción fue exitosa, False en caso de error.
    """
    db = get_db()
    if db is None: return False

    nota = {
        "id_usuario": str(id_usr),
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "texto": texto,
        "etiquetas": etiquetas, 
        "estado_animo": int(animo),
        "ubicacion": ubicacion
    }
    try:
        db.notas_personales.insert_one(nota)
        return True
    except Exception as e:
        print(f"Error Mongo al insertar nota: {e}")
        return False

def insertar_archivo_adjunto(id_usr, ruta, tipo, descripcion, metadatos=None):
    """
    Función: insertar_archivo_adjunto
    Descripción: Registra los metadatos de un archivo adjunto en la colección 'archivos_adjuntos'.
                 Permite almacenar rutas y descripciones de fotos o documentos[cite: 100].
    
    Argumentos:
        id_usr (str): ID del usuario.
        ruta (str): Ruta local o URL del archivo.
        tipo (str): Tipo de archivo (ej. 'imagen', 'pdf').
        descripcion (str): Breve descripción del contenido.
        metadatos (dict, opcional): Diccionario con datos extra (ej. calorías, fuente).
        
    Proceso:
        1. Valida si existen metadatos adicionales.
        2. Estructura el documento JSON incluyendo la fecha actual.
        3. Realiza la inserción en la colección correspondiente.
        
    Retorna:
        bool: True si la operación es exitosa, False si falla.
    """
    db = get_db()
    if db is None: return False

    if metadatos is None:
        metadatos = {}
        
    archivo = {
        "id_usuario": str(id_usr),
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "ruta_archivo": ruta,
        "tipo": tipo,
        "descripcion": descripcion,
        "metadatos": metadatos
    }
    try:
        db.archivos_adjuntos.insert_one(archivo)
        return True
    except Exception as e:
        print(f"Error Mongo al insertar archivo: {e}")
        return False

def leer_notas(id_usr):
    """
    Función: leer_notas
    Descripción: Recupera el historial de notas personales asociadas a un usuario específico.
    
    Argumentos:
        id_usr (str): ID del usuario a consultar.
        
    Retorna:
        list: Lista de diccionarios (documentos JSON) encontrados en MongoDB.
              Retorna una lista vacía [] si no hay conexión o no hay datos.
    """
    db = get_db()
    if db is None: return []
    try:
        return list(db.notas_personales.find({"id_usuario": str(id_usr)}))
    except Exception as e:
        print(f"Error leyendo notas: {e}")
        return []