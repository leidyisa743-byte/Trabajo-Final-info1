# modules/utils.py
# Autores: Gabriela Guevara Murcia, Leidy Zapata Hoyos, Isabela López Patiño, Isabella Arrieta Pacheco
# Descripción: Módulo de utilidades transversales encargado de las validaciones de entrada de datos 
#              y funciones de interfaz de usuario.

import os
from datetime import datetime

def validar_fecha(fecha_str):
    """
    Función: validar_fecha
    Descripción: Verifica si una cadena de texto cumple con el formato de fecha estándar (YYYY-MM-DD)
                 requerido para los registros SQL.
    
    Argumentos:
        fecha_str (str): Cadena de texto con la fecha a validar.
        
    Proceso:
        Intenta convertir el string a un objeto datetime usando el formato '%Y-%m-%d'.
        Si la conversión falla (ValueError), se considera inválida.
        
    Retorna:
        bool: True si la fecha es válida y tiene el formato correcto, False en caso contrario.
    """
    try:
        datetime.strptime(fecha_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validar_numero(valor, min_val=0, max_val=None):
    """
    Función: validar_numero
    Descripción: Valida que una entrada sea numérica y opcionalmente verifica que se encuentre
                 dentro de un rango específico. Útil para validar horas de sueño, edad, ánimo, etc.
    
    Argumentos:
        valor (str/int/float): El valor a validar.
        min_val (float): Valor mínimo permitido (por defecto 0).
        max_val (float, opcional): Valor máximo permitido (ej. 10 para escala de ánimo).
        
    Proceso:
        1. Intenta convertir el valor a float.
        2. Verifica si es menor que min_val.
        3. Si existe max_val, verifica si es mayor que max_val.
        
    Retorna:
        bool: True si es un número válido dentro del rango, False si no es número o está fuera de rango.
    """
    try:
        val = float(valor)
        if val < min_val: return False
        if max_val is not None and val > max_val: return False
        return True
    except ValueError:
        return False

def limpiar_pantalla():
    """
    Función: limpiar_pantalla
    Descripción: Ejecuta el comando del sistema operativo para limpiar la consola,
                 mejorando la experiencia de usuario en los menús.
    
    Proceso:
        Detecta el sistema operativo (Windows='nt' o Unix/Linux/Mac) y ejecuta
        el comando correspondiente ('cls' o 'clear').
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def mostrar_error(e):
    """
    Función: mostrar_error
    Descripción: Estandariza la visualización de errores en la consola.
    
    Argumentos:
        e (Exception/str): El objeto de error o mensaje a mostrar.
        
    Proceso:
        Imprime el mensaje con un formato de etiqueta [ERROR] para alertar al usuario.
    """
    print(f"\n[ERROR] Ha ocurrido un problema: {e}")