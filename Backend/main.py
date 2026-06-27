from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os

from routers import estudiantes, admin
from config.database import obtener_conexion

app = FastAPI(title="Lynko API - Ecosistema Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=BASE_DIR)

# Inyección de Controladores divididos bajo el patrón MVC
app.include_router(admin.router)
app.include_router(estudiantes.router)

@app.get("/", response_class=HTMLResponse)
def index_landing(request: Request):
    return templates.TemplateResponse(request=request, name="landing.html")

@app.get("/login", response_class=HTMLResponse)
def vista_login(request: Request, error: Optional[str] = None, msg: Optional[str] = None):
    return templates.TemplateResponse(request=request, name="Login.html", context={"error": error, "msg": msg})
