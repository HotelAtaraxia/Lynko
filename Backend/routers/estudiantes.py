import os
import re
from datetime import datetime
from fastapi import Query
from typing import Optional
from fastapi import APIRouter, Request, Form, HTTPException, Query, status, responses
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field, field_validator
from config.database import obtener_conexion

# Importaciones semánticas desde la capa del Modelo
from models.estudiantes import (
    obtener_datos_base_estudiante,
    registrar_sesion_db,
    obtener_preguntas_landing_db,
    obtener_progreso_dashboard,
    consultar_dashboard_estudiante,
    obtener_materias_y_progreso,
    obtener_lista_examenes,
    insertar_intento_examen,
    obtener_listado_actividades,
    obtener_reto_semanal_activo,
    obtener_logros_estudiante,
    actualizar_perfil_db,
    eliminar_estudiante_permanente
)

# Configuración del directorio base subiendo un nivel desde /routers
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "..", "Frontend", "templates"))

# Inicializamos el router independiente
router = APIRouter()


# --- Esquemas de Validación Pydantic ---
class EstudianteActualizar(BaseModel):
    nombre: str = Field(..., min_length=2, description="El nombre debe tener al menos 2 letras")
    correo: str = Field(..., description="Correo electrónico del estudiante")
    contrasena: str = Field(..., min_length=8, description="La contraseña debe tener mínimo 8 caracteres")

    @field_validator('contrasena')
    @classmethod
    def validar_complejidad_contrasena(cls, v: str) -> str:
        if not re.search(r"[a-zA-Z]", v) or not re.search(r"[0-9]", v):
            raise ValueError("La contraseña debe combinar letras y números.")
        if len(set(v)) < 4:
            raise ValueError("La contraseña debe tener más variedad de caracteres diferentes.")
        return v

    @field_validator('correo')
    @classmethod
    def validar_formato_correo(cls, v: str) -> str:
        if "@" not in v or "." not in v:
            raise ValueError("El correo electrónico no es válido. ¡Revisa el formato!")
        return v


# --- Funciones Internas de Soporte / Wrappers ---
def registrar_sesion(id_usuario: int, token: str):
    """
    Registra el inicio de sesión llamando al controlador de base de datos.
    """
    registrar_sesion_db(id_usuario, token)


# --- API Pública de la Landing Page ---
@router.get("/api/preguntas-landing")
def obtener_preguntas_landing():
    conn = obtener_conexion()
    preguntas_data = []
    
    if conn:
        try:
            # Usamos dos cursores distintos para evitar conflictos de lectura
            with conn.cursor() as cursor_preguntas:
                # 1. Buscamos las preguntas
                query = """
                    SELECT DISTINCT ON (p.id_materia) 
                        p.id_pregunta, m.nombre AS materia, p.pregunta, p.puntos_recompensa
                    FROM preguntas p
                    JOIN materias m ON p.id_materia = m.id_materia
                    ORDER BY p.id_materia, RANDOM();
                """
                cursor_preguntas.execute(query)
                filas = cursor_preguntas.fetchall()
                
                # 2. Abrimos el segundo cursor dentro del bloque para las opciones
                with conn.cursor() as cursor_opciones:
                    for fila in filas:
                        id_preg = fila[0]
                        
                        cursor_opciones.execute("""
                            SELECT opcion, es_correcta
                            FROM opciones
                            WHERE id_pregunta = %s
                            ORDER BY RANDOM();
                        """, (id_preg,))
                        
                        filas_opciones = cursor_opciones.fetchall()
                        opciones = [{"opcion": o[0], "es_correcta": bool(o[1])} for o in filas_opciones]
                        
                        preguntas_data.append({
                            "id_pregunta": id_preg,
                            "materia": fila[1].upper(),
                            "pregunta": fila[2],
                            "puntos": fila[3],
                            "opciones": opciones
                        })
        except Exception as e:
            print(f"⚠️ Error en la API de la landing: {e}")
        finally:
            conn.close()
            
    # Respuesta de respaldo si la base de datos no retorna datos
    if not preguntas_data:
        return [
            {
                "id_pregunta": 0,
                "materia": "MATEMÁTICAS",
                "pregunta": "Si el lince Lynko recolecta 5 manzanas por la mañana y 7 por la tarde, ¿cuántas manzanas tiene en total? 🍎",
                "puntos": 15,
                "opciones": [
                    {"opcion": "A) 10 manzanas", "es_correcta": False},
                    {"opcion": "B) 12 manzanas", "es_correcta": True},
                    {"opcion": "C) 15 manzanas", "es_correcta": False},
                    {"opcion": "D) 9 manzanas", "es_correcta": False}
                ]
            }
        ]
        
    return preguntas_data



@router.get("/inicio-estudiante/{id_usuario}", response_class=HTMLResponse)
def dashboard_estudiante_logeado(id_usuario: int, request: Request):
    # Usamos la función que SÍ consulta la base de datos completa
    datos_usuario, progreso, imagenes = consultar_dashboard_estudiante(id_usuario)
    
    return templates.TemplateResponse(
        request=request, 
        name="inicio_lynko.html", 
        context={
            "request": request,
            "id_usuario": id_usuario,
            "nombre": datos_usuario["nombre"],
            "puntos": datos_usuario["puntaje_total"],
            "nivel": datos_usuario["nivel"],
            "racha": datos_usuario["dias_racha"],
            "progreso": progreso,
            "imagenes": imagenes
        }
    )

@router.get("/materias-estudiante/{id_usuario}", response_class=HTMLResponse)
def vista_materias(request: Request, id_usuario: int):
    datos_base = obtener_datos_base_estudiante(id_usuario) # Datos para la cabecera
    resultado = obtener_materias_y_progreso(id_usuario)
    
    datos_usuario, materias_lista = resultado if isinstance(resultado, tuple) and len(resultado) == 2 else ({"nombre": "Estudiante"}, [])
    
    return templates.TemplateResponse(
        request=request, name="Materias.html", 
        context={"request": request, "id_usuario": id_usuario, **datos_base, **datos_usuario, "materias": materias_lista}
    )

@router.get("/examenes-estudiante/{id_usuario}", response_class=HTMLResponse)
def listar_examenes(id_usuario: int, request: Request, materia_id: Optional[int] = Query(None)):
    datos_base = obtener_datos_base_estudiante(id_usuario)
    examenes_lista = obtener_lista_examenes(id_usuario) or []
    
    return templates.TemplateResponse(
        request=request, name="Examenes.html",
        context={"request": request, "id_usuario": id_usuario, **datos_base, "examenes": examenes_lista}
    )

@router.get("/actividades-estudiante/{id_usuario}", response_class=HTMLResponse)
def vista_actividades(id_usuario: int, request: Request, materia_filter: Optional[str] = Query("Todas")):
    datos_base = obtener_datos_base_estudiante(id_usuario)
    resultado = obtener_listado_actividades(id_usuario)
    
    datos_user, actividades_lista = resultado if isinstance(resultado, tuple) and len(resultado) == 2 else ({"nombre": "Estudiante"}, [])
    
    return templates.TemplateResponse(
        request=request, name="Actividades.html", 
        context={"request": request, "id_usuario": id_usuario, **datos_base, **datos_user, "actividades": actividades_lista, "filtro_actual": materia_filter}
    )

@router.get("/progreso-estudiante/{id_usuario}", response_class=HTMLResponse)
def reto_semanal_estudiante(id_usuario: int, request: Request):
    datos_base = obtener_datos_base_estudiante(id_usuario)
    reto_datos = obtener_reto_semanal_activo() or {}
    
    return templates.TemplateResponse(
        request=request, name="Reto_semanal.html", 
        context={"request": request, "id_usuario": id_usuario, **datos_base, "reto": reto_datos}
    )

@router.get("/recompensas-estudiante/{id_usuario}", response_class=HTMLResponse)
def vista_recompensas(id_usuario: int, request: Request):
    datos_base = obtener_datos_base_estudiante(id_usuario)
    resultado = obtener_logros_estudiante(id_usuario)
    
    datos_user, logros_lista = resultado if isinstance(resultado, tuple) and len(resultado) == 2 else ({"nombre": "Estudiante"}, [])
        
    return templates.TemplateResponse(
        request=request, name="Recompensas.html", 
        context={"request": request, "id_usuario": id_usuario, **datos_base, **datos_user, "logros": logros_lista}
    )

@router.get("/perfil-estudiante/{id_usuario}", response_class=HTMLResponse)
def vista_perfil(id_usuario: int, request: Request):
    # Obtenemos los datos base (incluye nombre, puntos, nivel, etc.)
    datos_user = obtener_datos_base_estudiante(id_usuario) or {"nombre": "Estudiante", "correo": ""}
    print(f"DEBUG: Datos enviados al HTML: {datos_user}")
    
    return templates.TemplateResponse(
        request=request, 
        name="Perfil.html", 
        context={
            "request": request, 
            "id_usuario": id_usuario, 
            **datos_user
        }
    )

@router.get("/ajustes-estudiante/{id_usuario}", response_class=HTMLResponse)
def vista_ajustes(id_usuario: int, request: Request):
    
    datos_user = obtener_datos_base_estudiante(id_usuario) or {"nombre": "Estudiante", "correo": ""}
    
    return templates.TemplateResponse(
        request=request, 
        name="Ajustes.html", 
        context={
            "request": request, 
            "id_usuario": id_usuario, 
            **datos_user  # Desempaqueta nombre, puntos, nivel, etc.[cite: 1]
        }
    )
    

@router.post("/ajustes-estudiante/{id_usuario}/guardar")
def actualizar_perfil_estudiante(id_usuario: int, nombre: str = Form(...), correo: str = Form(...), contrasena: str = Form(...)):
    actualizar_perfil_db(id_usuario, nombre, correo, contrasena)
    return responses.RedirectResponse(url=f"/perfil-estudiante/{id_usuario}", status_code=303)


# --- Rutas API Puras (Retorno JSON) ---

@router.put("/api/estudiantes/{id_usuario}", status_code=status.HTTP_200_OK)
def actualizar_perfil_estudiante_api(id_usuario: int, datos: EstudianteActualizar):
    """
    Punto de acceso API REST con validación Pydantic estricta para actualizar perfiles.
    """
    filas_afectadas = actualizar_perfil_db(id_usuario, datos.nombre, datos.correo, datos.contrasena)
    if filas_afectadas == 0:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado.")
        
    return {"status": "success", "message": "¡Tus datos de perfil han sido modificados con éxito!"}


@router.post("/api/iniciar-examen/{id_usuario}/{id_examen}")
def iniciar_examen(id_usuario: int, id_examen: int):
    """
    Crea e inicializa transaccionalmente una instancia o intento de evaluación.
    """
    try:
        id_intento = insertar_intento_examen(id_usuario, id_examen)
        return {"status": "success", "id_intento": id_intento}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/api/usuarios/{id_usuario}", status_code=status.HTTP_200_OK)
def dar_de_baja_usuario(id_usuario: int):
    """
    Elimina físicamente y de forma permanente todos los registros del usuario indicado.
    """
    try:
        eliminar_estudiante_permanente(id_usuario)
        return {"status": "success", "message": "Borrado permanentemente."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
