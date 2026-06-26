# 🐾 Lynko Backend

Este es el núcleo lógico de la plataforma educativa **Lynko**. Se encarga de gestionar la API, la lógica de negocio, las validaciones de usuario y la comunicación con la base de datos.

## 🏗️ Arquitectura del Backend

El backend sigue una estructura modular para facilitar el mantenimiento y la escalabilidad:

*   **`main.py`**: Punto de entrada de la aplicación FastAPI.
*   **`app.py`**: Configuración de la aplicación y montaje del router principal.
*   **`database.py`**: Gestión centralizada de la conexión con la base de datos PostgreSQL.
*   **`routers/`**: Contiene los endpoints divididos por funcionalidad (estudiantes, materias, autenticación, etc.).
*   **`admin.py`**: Lógica de control para la gestión administrativa del sistema.

---

## 🛠️ Requisitos Técnicos (`requirements.txt`)

Para ejecutar este backend, asegúrate de tener instaladas las siguientes dependencias:

*   `fastapi==0.111.0`: Motor de la API y manejo de rutas.
*   `uvicorn==0.30.1`: Servidor ASGI para ejecutar la aplicación.
*   `jinja2==3.1.4`: Renderizado de plantillas HTML para el frontend.
*   `pydantic==2.7.2`: Validación de esquemas de datos.
*   `pydantic-settings==2.3.0`: Gestión de configuraciones.
*   `psycopg2-binary==2.9.9`: Driver para la conexión con PostgreSQL.
*   `python-multipart==0.0.9`: Procesamiento de formularios web.

---

## 🚀 Ejecución

Para iniciar el servidor de desarrollo, sigue estos pasos desde la carpeta `/Backend`:

1. **Activa tu entorno virtual**:
   ```bash
   # Windows
   venv\Scripts\activate
