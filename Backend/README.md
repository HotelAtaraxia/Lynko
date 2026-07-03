# 🚀 Lynko Backend

El motor de backend para la plataforma educativa **Lynko**, desarrollado con **FastAPI**. Este sistema gestiona el progreso, retos, logros y actividades de los estudiantes con una arquitectura modular y eficiente.

---

## 🏗 Arquitectura del Proyecto

El proyecto sigue un patrón de diseño **Router-Model-Database** para separar la lógica de negocio de la gestión de rutas:

- **`app.py`**: Punto de entrada principal. Configura la aplicación FastAPI, middlewares de rastreo y rutas base.
- **`routers/`**: Capa de presentación. Recibe peticiones HTTP, valida parámetros y prepara el contexto para las plantillas.
- **`models/`**: Capa de lógica de negocio. Contiene funciones que interactúan con la base de datos, realizan cálculos (niveles, rachas) y procesan datos.
- **`config/`**: Gestión de infraestructura. Contiene la lógica para la conexión segura a PostgreSQL.



---

## 🛠 Tecnologías y Dependencias

Para el funcionamiento del entorno, el proyecto utiliza:

| Librería | Propósito en el Proyecto |
| :--- | :--- |
| **`fastapi`** | Framework principal para la creación de endpoints y arquitectura REST. |
| **`uvicorn`** | Servidor ASGI de alta velocidad para ejecutar la aplicación. |
| **`pydantic`** | Validación automática de tipos de datos y esquemas de entrada/salida. |
| **`pydantic-settings`** | Gestión centralizada de configuraciones y variables de entorno. |
| **`psycopg2-binary`** | Conector nativo para interactuar con bases de datos PostgreSQL. |
| **`jinja2`** | Motor de renderizado para inyectar datos del backend en plantillas HTML. |
| **`python-multipart`** | Procesamiento de formularios y subida de archivos desde el frontend. |


---

## 📂 Estructura de Directorios

```text
Backend/
├── app.py              # Configuración global y Middleware
├── config/
│   └── database.py     # Lógica de conexión a PostgreSQL
├── models/
│   ├── estudiantes.py  # Funciones SQL para perfiles, logros y retos
│   └── (otros modelos) # Módulos especializados de lógica
├── routers/
│   └── estudiantes.py  # Endpoints de la interfaz del estudiante
└── templates/          # Archivos HTML y assets de UI
```
## ⚙️ Configuración y Despliegue
1. Instalación
Asegúrate de tener Python 3.14+ instalado y ejecuta:

```Bash
pip install fastapi uvicorn psycopg2-binary jinja2
```
2. Ejecución
Para iniciar el servidor en modo de desarrollo con recarga automática:

```Bash
uvicorn app:app --reload
```
---
##🧩 Funcionalidades Clave
Gestión de Datos
La lógica de base de datos está centralizada en los modelos, utilizando el patrón with...as para garantizar que las conexiones se cierren automáticamente, optimizando así el rendimiento.

## Gamificación
El backend incluye lógica integrada para:

Cálculo de niveles: Basado en puntaje_total.

Logros: Sistema de filtrado alcanzados/pendientes.

Retos semanales: Exclusión de exámenes ya aprobados usando NOT IN en consultas SQL.

###🔒 Consideraciones de Seguridad
SQL Injection: Todas las consultas utilizan parámetros tipados (%s) para evitar vulnerabilidades de inyección.

Sesiones: Implementación de un sistema de tokens para validar el acceso de los usuarios.

Manejo de Errores: Middleware centralizado para el rastreo y registro de errores críticos 500.
