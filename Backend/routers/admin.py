from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import os

from models.admin import obtener_metricas_dashboard
from config.database import obtener_conexion

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=BASE_DIR)

router = APIRouter(prefix="/admin")

@router.get("")
def panel_inicio(request: Request):
    total_est, total_preg, prom_exp, ult_preg, mejores_est = obtener_metricas_dashboard()
    return templates.TemplateResponse(
        request=request,
        name="Admin.html",
        context={
            "total_estudiantes": total_est,
            "total_preguntas": total_preg,
            "promedio_exp": prom_exp,
            "ultimas_preguntas": ult_preg,
            "mejores_estudiantes": mejores_est
        }
    )

@router.get("/preguntas/borrar/{id_pregunta}")
def borrar_pregunta(id_pregunta: int):
    conn = obtener_conexion()
    msg = ""
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM preguntas WHERE id_pregunta = %s;", (id_pregunta,))
                conn.commit()
            msg = "Pregunta eliminada del sistema"
        except Exception as e:
            msg = "No se pudo eliminar la pregunta"
        finally:
            conn.close()
    return RedirectResponse(url=f"/admin?msg={msg}", status_code=303)
