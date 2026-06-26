# 🐾 Proyecto Lynko

¡Bienvenido al repositorio oficial de **Lynko**! Este es una plataforma educativa interactiva diseñada para fomentar el aprendizaje dinámico y divertido.

##  Estructura del Proyecto

El proyecto está organizado para mantener una separación clara entre la lógica del servidor y la interfaz de usuario:

*   **`/Backend`**: Contiene la lógica del servidor, routers de la API, conexión a base de datos y modelos de datos.
*   **`/Frontend`**: Contiene toda la interfaz visual, incluyendo archivos estáticos (CSS) y las plantillas HTML.

---

##  Requisitos Técnicos

Para ejecutar Lynko, necesitas tener instalado en tu equipo:

1.  **Python 3.12 o superior**.
2.  **Un servidor de base de datos** (PostgreSQL/MySQL configurado en `database.py`).
3.  **Gestor de paquetes `pip`**.

---

## Cómo ejecutar el proyecto

Sigue estos pasos en tu terminal para poner en marcha la plataforma:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/HotelAtaraxia/Lynko.git](https://github.com/HotelAtaraxia/Lynko.git)
cd Lynko

### 2. Configurar el entorno virtual
Es vital para aislar las dependencias y evitar errores de librerías:

En Windows:

Bash
python -m venv venv
venv\Scripts\activate
### 3. Instalar dependencias
Dentro de la carpeta raíz, ejecuta:

Bash
pip install fastapi uvicorn pydantic pydantic-settings psycopg2-binary jinja2
### 4. Ejecución del servidor
Navega a la carpeta /Backend y ejecuta el servidor con Uvicorn:

Bash
cd Backend
uvicorn main:app --reload
La aplicación estará disponible en http://127.0.0.1:8000.

### Conexión a Base de Datos
La comunicación con los datos se centraliza en el archivo database.py ubicado en /Backend:

El sistema utiliza un gestor de conexiones invocado dinámicamente por los distintos routers del proyecto.

Importante: Asegúrate de que tus credenciales de acceso a la base de datos (usuario, host, password) en database.py coincidan exactamente con tu entorno local.

### Frontend y Diseño
La interfaz ha sido construida siguiendo estándares de desarrollo web moderno, como se visualiza en image_27c784.png:

Estructura CSS: Implementación del modelo de cajas (border-box) para asegurar que el diseño no se deforme al escalar.

Modularidad: Uso de selectores de ID para bloques únicos y clases para componentes reutilizables (tarjetas de materias, alertas, botones).

Flexbox: Sistema principal para garantizar que la plataforma sea responsiva y se adapte a cualquier pantalla.

### Solución de Problemas
ModuleNotFoundError: Si el servidor no inicia, asegúrate de que tu entorno virtual (venv) esté activado antes de ejecutar pip install o uvicorn.

Errores de ruta: El proyecto depende de la estructura mostrada en image_27c4a0.png. Si mueves archivos de lugar, recuerda actualizar los imports en app.py y los archivos dentro de la carpeta routers/.

Desarrollado con ❤️ para el aprendizaje.
