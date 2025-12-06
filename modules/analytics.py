# modules/analytics.py
# Autores: Gabriela Guevara Murcia, Leidy Zapata Hoyos, Isabela López Patiño, Isabella Arrieta Pacheco
# Descripción: Módulo para el análisis de datos de salud y generación de reportes.

import json
import os
from . import sql_manager
from datetime import datetime

def generar_reporte_json(id_usr):
    """
    Genera y exporta un reporte de salud semanal/mensual en formato JSON.

    Argumentos:
        id_usr (str): Identificación del usuario del que se generará el reporte.

    Proceso:
        1. Consulta el historial de registros en la base de datos SQL.
        2. Calcula estadísticas de tendencia (promedios) para sueño y estado de ánimo.
        3. Genera un archivo JSON con el resumen estadístico y el detalle de registros.

    Retorna:
        str: Mensaje indicando el éxito de la operación y la ruta del archivo generado,
             o un mensaje de error si falla.
    """
    # 1. Recuperación de información histórica desde MySQL
    datos = sql_manager.obtener_historial_salud(id_usr)
    
    if not datos:
        return "No hay suficientes datos para generar reporte."

    # 2. Inicialización de variables para cálculo de tendencias [cite: 59]
    total_sueno = 0
    total_animo = 0
    count = 0
    
    # 3. Procesamiento de datos y conversión de tipos
    historial_limpio = []
    for reg in datos:
        # Conversión de objetos 'date' a string para serialización JSON
        reg_fix = reg.copy()
        if 'fecha' in reg_fix:
            reg_fix['fecha'] = str(reg_fix['fecha'])
        
        historial_limpio.append(reg_fix)
        
        # Acumulación de valores para promedios
        total_sueno += reg.get('horas_sueno', 0)
        total_animo += reg.get('estado_animo', 0)
        count += 1
    
    # Cálculo de promedios (Estadísticas) [cite: 73]
    prom_sueno = total_sueno / count if count > 0 else 0
    prom_animo = total_animo / count if count > 0 else 0

    # 4. Estructuración del reporte (Resumen + Detalle) [cite: 72]
    reporte = {
        "usuario": id_usr,
        "fecha_generacion": str(datetime.now()),
        "resumen_estadistico": {
            "total_dias_registrados": count,
            "promedio_horas_sueno": round(prom_sueno, 2),
            "promedio_estado_animo": round(prom_animo, 2)
        },
        "historial_detalle": historial_limpio
    }

    # 5. Exportación del archivo a la carpeta 'reportes'
    if not os.path.exists('reportes'):
        os.makedirs('reportes')
        
    # Generación de nombre único usando fecha y hora
    filename = f"reportes/reporte_{id_usr}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(reporte, f, indent=4, ensure_ascii=False)
        return f"Reporte generado exitosamente: {filename}"
    except Exception as e:
        return f"Error generando reporte: {e}"