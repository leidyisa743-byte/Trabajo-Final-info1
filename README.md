# Sistema de Bitácora Personal de Salud y Bienestar - Bioingeniería
**Proyecto Final Informática I - 2025-2**
**Universidad de Antioquia - Facultad de Ingeniería**

### 👥 Autores
* Gabriela Guevara Murcia
* Leidy Zapata Hoyos
*  Isabela López Patiño
*  Isabella Arrieta Pacheco

---

## 📋 Descripción del Proyecto
Aplicación de software híbrida desarrollada en Python para el registro, visualización y análisis de información de salud personal. El sistema implementa una arquitectura de bases de datos mixta:
* **MySQL (Relacional):** Para datos estructurados (Usuarios, Registros diarios de salud, Signos vitales).
* **MongoDB Atlas (NoSQL en la Nube):** Para datos no estructurados (Notas personales, Metadatos de archivos adjuntos/fotos).
* **CSV:** Para la gestión segura de credenciales y autenticación.

El objetivo es fomentar el autocuidado mediante el análisis de tendencias y alertas inteligentes basadas en los datos ingresados.

---

## ⚙️ Requerimientos Técnicos
Para ejecutar este proyecto, asegúrese de tener instalado:

1.  **Python 3.8+**
2.  **MySQL Server** (Corriendo en `localhost` por defecto).
3.  **Conexión a Internet** (Necesaria para conectar con el clúster de MongoDB Atlas).
4.  Librerías de Python (Listadas en `requirements.txt`).

### Instalación de Dependencias
Ejecute el siguiente comando en la terminal:
```bash
pip install -r requirements.txt
