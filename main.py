# main.py
# Autores: Gabriela Guevara Murcia, Leidy Zapata Hoyos, Isabela López Patiño, Isabella Arrieta Pacheco
# Descripción: Archivo principal de ejecución. Gestiona el ciclo de vida de la aplicación,
#              incluyendo el arranque automático (bootstrapping), autenticación y navegación por roles.

import os
import time
import sys
from modules import auth_manager, sql_manager, mongo_manager, analytics, utils
import setup_db 

def auto_setup_inicial():
    """
    Función: auto_setup_inicial
    Descripción: Verifica la integridad del entorno de ejecución al iniciar el programa.
                 Implementa el patrón de 'Bootstrapping' para asegurar que las bases de datos
                 estén configuradas antes de permitir el acceso.

    Proceso:
        1. Busca el archivo maestro de credenciales ('data/passwords.csv').
        2. Si no existe, asume una instalación limpia y ejecuta 'setup_db.setup()'.
        3. Provisiona tablas MySQL y colecciones MongoDB Atlas con datos semilla.
    """
    archivo_clave = 'data/passwords.csv'
    
    if not os.path.exists(archivo_clave):
        utils.limpiar_pantalla()
        print("\n" + "█"*60)
        print("█  DETECTANDO ENTORNO NUEVO - INICIANDO INSTALACIÓN...     █")
        print("█"*60 + "\n")
        print(">> Configurando Bases de Datos y cargando semillas...")
        
        try:
            setup_db.setup()
            
            print("\n" + "="*60)
            print("✅ INSTALACIÓN COMPLETADA EXITOSAMENTE.")
            print("   - MySQL: Tablas creadas y datos cargados.")
            print("   - MongoDB: Conectado a Atlas y datos cargados.")
            print("   - Sistema: CSV de seguridad generado.")
            print("="*60)
            print("\nIniciando aplicación en 3 segundos...")
            time.sleep(3)
        except Exception as e:
            print(f"\n❌ ERROR CRÍTICO DURANTE LA INSTALACIÓN AUTOMÁTICA: {e}")
            print("Por favor, revise la conexión a Internet (para Atlas) o MySQL.")
            input("Presione Enter para salir...")
            sys.exit()

def menu_admin():
    """
    Función: menu_admin
    Descripción: Interfaz de línea de comandos para el perfil de Administrador.
                 Permite la gestión de usuarios en la base de datos SQL.
    """
    while True:
        utils.limpiar_pantalla()
        print("\n--- MENÚ ADMINISTRADOR ---")
        print("1. Crear Nuevo Usuario")
        print("2. Ver Usuarios (SQL)")
        print("3. Salir")
        op = input("Seleccione: ")
        
        if op == '1':
            id_u = input("ID: ")
            nom = input("Nombre: ")
            edad = input("Edad: ")
            rol = input("Rol (admin/usuario): ")
            pwd = input("Contraseña: ")
            
            if sql_manager.crear_usuario(id_u, nom, int(edad), f"{id_u}@mail.com", rol):
                auth_manager.registrar_password(id_u, pwd)
                print("Usuario creado exitosamente.")
                time.sleep(1.5)
        
        elif op == '2':
            print("Funcionalidad pendiente de visualización masiva.")
            input("Enter para volver...")
            
        elif op == '3':
            break

def menu_usuario(usuario):
    """
    Función: menu_usuario
    Descripción: Interfaz principal para el usuario estándar. Integra las funcionalidades
                 híbridas de SQL (registros diarios) y MongoDB (notas/fotos).

    Argumentos:
        usuario (dict): Diccionario con la información del usuario autenticado.
    """
    id_usr = usuario['id']
    nombre = usuario['nombre']
    
    while True:
        utils.limpiar_pantalla()
        print(f"\n--- BIENVENIDO {nombre} ---")
        print("1. Registrar día (Salud)")
        print("2. Nueva Nota Personal / Foto (Mongo)")
        print("3. Ver mi Historial")
        print("4. Generar Reporte y Análisis")
        print("5. Salir")
        
        op = input("Seleccione: ")
        
        if op == '1':
            fecha = input("Fecha (YYYY-MM-DD): ")
            if not utils.validar_fecha(fecha): 
                print("Fecha inválida")
                time.sleep(1)
                continue
            
            sueno = input("Horas sueño: ") or "0"
            animo = input("Ánimo (1-10): ") or "5"
            act = input("Actividad física: ")
            sint = input("Síntomas: ")
            
            if sql_manager.insertar_registro_diario(id_usr, fecha, float(sueno), int(animo), act, sint):
                print("✅ Registro guardado en SQL.")
                time.sleep(1.5)
                
        elif op == '2':
            texto = input("Escribe tu nota del día: ")
            tags = input("Etiquetas (sep. por coma): ").split(',')
            
            # Inserción en MongoDB Atlas
            if mongo_manager.insertar_nota(id_usr, texto, tags, 5):
                print("✅ Nota guardada en MongoDB Atlas.")
            
            foto = input("¿Adjuntar foto? (s/n): ")
            if foto.lower() == 's':
                ruta = input("Ruta del archivo (ej: foto.jpg): ")
                mongo_manager.insertar_archivo_adjunto(id_usr, ruta, "imagen", "Foto adjunta")
                print("✅ Metadatos de archivo guardados en Atlas.")
            time.sleep(1.5)
            
        elif op == '3':
            # Recuperación y visualización híbrida de datos
            historial = sql_manager.obtener_historial_salud(id_usr)
            notas = mongo_manager.leer_notas(id_usr)
            
            print("\n" + "-"*30)
            print("   TUS REGISTROS SQL")
            print("-"*30)
            for h in historial: 
                print(f"Fecha: {h['fecha']} | Ánimo: {h['estado_animo']} | Síntomas: {h['sintomas']}")
            
            print("\n" + "-"*30)
            print("   TUS NOTAS MONGO ATLAS")
            print("-"*30)
            for n in notas: 
                print(f"{n['fecha']}: {n['texto']}")
            
            input("\nPresione Enter para volver...")
            
        elif op == '4':
            msg = analytics.generar_reporte_json(id_usr)
            print(msg)
            input("Presione Enter para volver...")
            
        elif op == '5':
            break

def main():
    """
    Función: main
    Descripción: Punto de entrada de la aplicación.
                 1. Ejecuta la validación de entorno (bootstrapping).
                 2. Inicializa gestores de autenticación.
                 3. Ejecuta el bucle principal de Login.
    """
    # 1. Validación de instalación
    auto_setup_inicial()
    
    # 2. Inicialización de seguridad
    auth_manager.inicializar_csv()
    
    while True:
        utils.limpiar_pantalla()
        print("=== SISTEMA DE BITÁCORA DE SALUD - BIOINGENIERÍA ===")
        print("1. Iniciar Sesión")
        print("2. Salir")
        
        opcion = input("Opción: ")
        
        if opcion == '1':
            user = input("Usuario (ID): ")
            pwd = input("Contraseña: ")
            
            datos_usuario, mensaje = auth_manager.verificar_login(user, pwd)
            
            if datos_usuario:
                rol = datos_usuario['rol']
                if rol == 'admin':
                    menu_admin()
                else:
                    menu_usuario(datos_usuario)
            else:
                print(f"Error: {mensaje}")
                time.sleep(2)
                
        elif opcion == '2':
            print("Saliendo...")
            break

if __name__ == "__main__":
    main()