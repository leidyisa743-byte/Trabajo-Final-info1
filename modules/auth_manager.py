# modules/auth_manager.py
# Autores: Gabriela Guevara Murcia, Leidy Zapata Hoyos, Isabela López Patiño, Isabella Arrieta Pacheco
# Descripción: Módulo encargado de la autenticación mediante archivo CSV y verificación de roles en SQL.

import csv
import os
from . import sql_manager

CSV_FILE = 'data/passwords.csv'

def inicializar_csv():
    """
    Función: inicializar_csv
    Descripción: Verifica la existencia del directorio de datos y del archivo CSV.
                 Si no existen, los crea e inicializa con la cabecera y un usuario admin por defecto.
    
    Proceso:
        1. Valida si existe la carpeta 'data'.
        2. Valida si existe 'passwords.csv'.
        3. Escribe la cabecera ['id_usuario', 'password'] si el archivo es nuevo.
    """
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id_usuario', 'password'])
            # Usuario Admin por defecto para configuración inicial
            writer.writerow(['1', 'admin123']) 

def registrar_password(id_usuario, password):
    """
    Función: registrar_password
    Descripción: Almacena una nueva credencial de acceso en el archivo CSV.
    
    Argumentos:
        id_usuario (str): Identificador único del usuario.
        password (str): Contraseña a registrar.
        
    Proceso:
        Abre el archivo CSV en modo 'append' (agregar al final) y escribe una nueva fila.
    """
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([id_usuario, password])

def verificar_login(id_usuario, password_input):
    """
    Función: verificar_login
    Descripción: Valida las credenciales ingresadas y obtiene la información del usuario.
    
    Argumentos:
        id_usuario (str): ID ingresado por el usuario.
        password_input (str): Contraseña ingresada para validar.
        
    Proceso:
        1. Recorre el archivo CSV buscando coincidencia de ID y password[cite: 161].
        2. Si la credencial es válida, consulta la base de datos SQL para obtener el rol y nombre[cite: 162].
        
    Retorna:
        tuple: (usuario_dict, mensaje)
            - usuario_dict: Diccionario con datos del usuario si es exitoso, o None si falla.
            - mensaje: String indicando "OK" o la causa del error.
    """
    try:
        # 1. Verificar Password en CSV
        login_valido = False
        with open(CSV_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['id_usuario'] == str(id_usuario) and row['password'] == password_input:
                    login_valido = True
                    break
        
        if not login_valido:
            return None, "Credenciales inválidas."

        # 2. Obtener Rol y Datos desde MySQL si la contraseña es correcta
        usuario = sql_manager.obtener_usuario_por_id(id_usuario)
        if usuario:
            return usuario, "OK" 
        else:
            return None, "Usuario existe en CSV pero no en SQL (Inconsistencia de datos)."
            
    except Exception as e:
        return None, str(e)