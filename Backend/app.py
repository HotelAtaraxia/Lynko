import sys
import os

# Asegurar rutas
RAIZ_PROYECTO = os.path.dirname(os.path.abspath(__file__))
if RAIZ_PROYECTO not in sys.path:
    sys.path.insert(0, RAIZ_PROYECTO)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


from typing import Optional
from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware


# IMPORTANTE: Importamos el objeto templates ya configurado
from config_templates import templates 
# Importación de funciones controladoras desde la capa de Modelos (Auth)
from models.estudiantes import obtener_perfil_estudiante, obtener_logros_estudiante


from models.auth import verificar_credenciales_login, registrar_nuevo_estudiante
from routers import estudiantes, admin

app = FastAPI(title="Lynko API - Ecosistema Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar estáticos usando la ruta absoluta desde la raíz
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "..", "Frontend", "static")), name="static")

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
        content=f"<h2>⚠️ Error en Lynko: {str(exc)}</h2>", 
        status_code=500
    )

# --- Rutas Públicas ---

@app.get("/", response_class=HTMLResponse)
def index_landing(request: Request):
    return templates.TemplateResponse(request=request, name="landing.html")

@app.get("/login", response_class=HTMLResponse)
def vista_login(request: Request, error: Optional[str] = None, msg: Optional[str] = None):
    return templates.TemplateResponse(request=request, name="login.html", context={"request": request, "error": error, "msg": msg})

@app.get("/registro", response_class=HTMLResponse)
def vista_registro(request: Request, error: Optional[str] = None):
    return templates.TemplateResponse(request=request, name="registro.html", context={"request": request, "error": error})

@app.post("/login")
def procesar_login(correo: str = Form(...), contrasena: str = Form(...)):
    usuario = verificar_credenciales_login(correo, contrasena)
    if usuario:
        id_u, _, rol = usuario
        if str(rol).strip().lower() == "admin":
            return RedirectResponse(url="/admin", status_code=303)
        return RedirectResponse(url=f"/inicio-estudiante/{id_u}", status_code=303)
    return RedirectResponse(url="/login?error=Credenciales incorrectas", status_code=303)

@app.post("/registro")
def procesar_registro(nombre: str = Form(...), correo: str = Form(...), contrasena: str = Form(...)):
    exito, resultado = registrar_nuevo_estudiante(nombre, correo, contrasena)
    if exito:
        return RedirectResponse(url=f"/inicio-estudiante/{resultado}", status_code=303)
    return RedirectResponse(url=f"/registro?error={resultado}", status_code=303)
