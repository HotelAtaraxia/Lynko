import os
import sys

# Forzamos a Python 3.14 a registrar el directorio raíz de la aplicación de forma absoluta
RAIZ_PROYECTO = os.path.dirname(os.path.abspath(__file__))
if RAIZ_PROYECTO not in sys.path:
    sys.path.insert(0, RAIZ_PROYECTO)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from typing import Optional
from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

# Importación de funciones controladoras desde la capa de Modelos (Auth)
from models.estudiantes import obtener_perfil_estudiante, obtener_logros_estudiante

# Importamos los routers del ecosistema
from routers import estudiantes
from routers import admin

app = FastAPI(title="Lynko API - Ecosistema Backend")

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. CONFIGURACIÓN DE RUTAS Y ASSETS ESTÁTICOS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=BASE_DIR)

# 2. INCLUSIÓN DE ROUTERS
app.include_router(admin.router)
app.include_router(estudiantes.router)


# 3. MIDDLEWARE DE RASTREO
@app.middleware("http")
async def middleware_rastreo_lynko(request: Request, call_next):
    print(f"📡 [Middleware] Petición: {request.method} a {request.url.path}")
    response = await call_next(request)
    return response


# 4. MANEJO DE ERRORES GLOBALES
@app.exception_handler(404)
async def error_404_personalizado(request: Request, exc: HTTPException):
    return RedirectResponse(url="/login?error=La pagina solicitada no existe", status_code=303)


@app.exception_handler(500)
async def error_500_personalizado(request: Request, exc: Exception):
    print(f"🔥 Error Crítico 500: {exc}")
    return HTMLResponse(
        content="<h2>⚠️ Error en Lynko. Verifica tu base de datos o estructura de carpetas.</h2>", 
        status_code=500
    )


# --- Rutas Públicas de Acceso (Vistas HTML) ---

@app.get("/", response_class=HTMLResponse)
def index_landing(request: Request):
    """Renderiza la Landing Page del proyecto Lynko."""
    return templates.TemplateResponse(request=request, name="landing.html")


@app.get("/login", response_class=HTMLResponse)
def vista_login(request: Request, error: Optional[str] = None, msg: Optional[str] = None):
    """Muestra el formulario de inicio de sesión."""
    return templates.TemplateResponse(request=request, name="Login.html", context={"error": error, "msg": msg})


@app.get("/registro", response_class=HTMLResponse)
def vista_registro(request: Request, error: Optional[str] = None):
    """Muestra el formulario de registro para nuevos alumnos."""
    return templates.TemplateResponse(request=request, name="Registro.html", context={"error": error})


@app.post("/login")
def procesar_login(correo: str = Form(...), contrasena: str = Form(...)):
    """
    Procesa las credenciales de acceso delegando la verificación al modelo,
    redireccionando según el rol del usuario (Admin o Estudiante).
    """
    usuario = verificar_credenciales_login(correo, contrasena)
    
    if usuario:
        id_u, _, rol = usuario
        if str(rol).strip().lower() == "admin":
            return RedirectResponse(url="/admin", status_code=303)
        else:
            return RedirectResponse(url=f"/inicio-estudiante/{id_u}", status_code=303)
            
    return RedirectResponse(url="/login?error=Credenciales incorrectas o usuario inactivo", status_code=303)


@app.post("/registro")
def procesar_registro(nombre: str = Form(...), correo: str = Form(...), contrasena: str = Form(...)):
    """
    Gestiona el registro transaccional de un nuevo estudiante y su primera insignia.
    """
    # La validación de complejidad de contraseña en un flujo ideal se maneja mediante Pydantic,
    # pero mantenemos la lógica limpia y segura centralizada en la capa de negocio.
    exito, resultado = registrar_nuevo_estudiante(nombre, correo, contrasena)
    
    if exito:
        # Si el registro es exitoso, 'resultado' contiene el id del nuevo usuario
        return RedirectResponse(url=f"/inicio-estudiante/{resultado}", status_code=303)
    else:
        # Si falla (por ejemplo, correo duplicado o contraseña débil), 'resultado' trae el mensaje de error
        return RedirectResponse(url=f"/registro?error={resultado}", status_code=303)
