from fastapi import APIRouter, Request, Form, HTTPException, Query, status, responses
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
import os

from models.estudiante import (
    consultar_preguntas_landing, 
    consultar_dashboard_estudiante, 
    obtener_datos_base_estudiante,
    obtener_conexion
)
from schemas.estudiante import EstudianteActualizar

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=BASE_DIR)

router = APIRouter()

@router.get("/api/preguntas-landing")
def obtener_preguntas_landing():
    preguntas = consultar_preguntas_landing()
    if not preguntas:
        return [
            {
                "id_pregunta": 0,
                "materia": "MATEMÁTICAS",
                "pregunta": "Si el lince Lynko recolecta 5 manzanas por la mañana y 7 por la tarde... 🍎",
                "puntos": 15,
                "opciones": [{"opcion": "B) 12 manzanas", "es_correcta": True}]
            }
        ]
    return preguntas

@router.get("/inicio-estudiante/{id_usuario}", response_class=HTMLResponse)
def dashboard_estudiante_logeado(id_usuario: int, request: Request, vista_rapida: Optional[bool] = Query(None)):
    datos, progreso, imagenes = consultar_dashboard_estudiante(id_usuario)
    return templates.TemplateResponse(
        request=request, name="inicio_lynko.html",
        context={"request": request, "id_usuario": id_usuario, "vista_rapida": vista_rapida, "progreso": progreso, "imagenes": imagenes, **datos}
    )

@router.put("/api/estudiantes/{id_usuario}", status_code=status.HTTP_200_OK)
def actualizar_perfil_estudiante_api(id_usuario: int, datos: EstudianteActualizar):
    conn = obtener_conexion()
    if not conn: raise HTTPException(status_code=500, detail="No hay conexión")
    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE usuarios SET nombre = %s, correo = %s, contraseña = %s WHERE id_usuario = %s AND rol = 'estudiante';", (datos.nombre, datos.correo, datos.contrasena, id_usuario))
            if cursor.rowcount == 0: raise HTTPException(status_code=404, detail="Estudiante no encontrado.")
            conn.commit()
            return {"status": "success", "message": "¡Tus datos de perfil han sido modificados con éxito!"}
    except Exception as e:
        if conn: conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    finally: conn.close()
