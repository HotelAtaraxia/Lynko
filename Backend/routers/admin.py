from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from config_templates import templates 

# Importación de funciones controladoras desde la capa del Modelo
from models.admin import (
    obtener_datos_panel_admin,
    crear_nueva_pregunta_db,
    obtener_listado_preguntas_completo,
    eliminar_pregunta_db,
    editar_datos_estudiante_db,
    obtener_todos_los_estudiantes,
    dar_baja_estudiante_db,
    obtener_ranking_top_10
)

# Inicializamos el router con el prefijo /admin
router = APIRouter(prefix="/admin")

@router.get("", response_class=HTMLResponse)
def panel_inicio(request: Request):
    """
    Muestra el dashboard principal del administrador recopilando métricas generales
    y tablas rápidas de mejores estudiantes y últimas preguntas.
    """
    preguntas, usuarios, metricas_materias, mejores_examenes = obtener_datos_panel_admin()
    
    total_estudiantes = len(usuarios)
    total_preguntas = len(preguntas)
    
    exp_totales = [u[3] for u in usuarios] 
    promedio_exp = round(sum(exp_totales) / total_estudiantes, 1) if total_estudiantes > 0 else 0.0
    
    ultimas_preguntas = preguntas[-5:]
    ultimas_preguntas.reverse()
    
    mejores_estudiantes_raw = sorted(usuarios, key=lambda x: x[3], reverse=True)[:5]
    mejores_estudiantes = [(u[0], u[1], u[2], u[3], u[4]) for u in mejores_estudiantes_raw]

    return templates.TemplateResponse(
        request=request,
        name="Admin.html", # Asegúrate de que el archivo se llame así
        context={
            "total_estudiantes": total_estudiantes,
            "total_preguntas": total_preguntas,
            "promedio_exp": promedio_exp,
            "ultimas_preguntas": ultimas_preguntas,
            "mejores_estudiantes": mejores_estudiantes
        }
    )

@router.post("/nuevas-preguntas")
def crear_pregunta(
    pregunta: str = Form(...), 
    id_materia: int = Form(...), 
    nivel: int = Form(...), 
    puntos: int = Form(...), 
    opcion1: str = Form(...), 
    opcion2: str = Form(...), 
    opcion3: str = Form(...), 
    correcta: str = Form(...)
):
    exito, msg = crear_nueva_pregunta_db(
        pregunta, id_materia, nivel, puntos, 
        opcion1, opcion2, opcion3, correcta
    )
    return RedirectResponse(url=f"/admin?msg={msg}", status_code=303)

@router.get("/preguntas", response_class=HTMLResponse)
def vista_admin_preguntas(request: Request):
    lista_preguntas = obtener_listado_preguntas_completo()
    return templates.TemplateResponse(
        request=request,
        name="admin-preguntas.html",
        context={"preguntas": lista_preguntas}
    )

@router.get("/preguntas/borrar/{id_pregunta}")
def borrar_pregunta(id_pregunta: int):
    exito, msg = eliminar_pregunta_db(id_pregunta)
    return RedirectResponse(url=f"/admin?msg={msg}", status_code=303)

@router.post("/preguntas/editar")
def procesar_edicion_pregunta(
    id_pregunta: int = Form(...), 
    id_materia: int = Form(...), 
    pregunta: str = Form(...), 
    puntos: int = Form(...)
):
    from models.admin import obtener_conexion
    conn = obtener_conexion()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE preguntas 
                    SET id_materia = %s, pregunta = %s, puntos_recompensa = %s 
                    WHERE id_pregunta = %s;
                """, (id_materia, pregunta, puntos, id_pregunta))
                conn.commit()
        except Exception as e:
            print(f"⚠️ Error al actualizar pregunta: {e}")
        finally:
            conn.close()
            
    return RedirectResponse(url="/admin/preguntas?msg=Pregunta+actualizada+con+éxito", status_code=303)

@router.post("/estudiantes/editar")
def editar_estudiante(
    id_usuario: int = Form(...), 
    nombre: str = Form(...), 
    correo: str = Form(...), 
    puntaje_total: int = Form(...)
):
    exito, msg = editar_datos_estudiante_db(id_usuario, nombre, correo, puntaje_total)
    return RedirectResponse(url="/admin/estudiantes", status_code=303)

@router.get("/estudiantes")
def lista_estudiantes(request: Request, q: str = None):
    if q and q.strip():
        from models.admin import obtener_conexion
        conn = obtener_conexion()
        lista_usuarios = []
        if conn:
            with conn.cursor() as cursor:
                termino = f"%{q.strip()}%"
                if q.strip().isdigit():
                    cursor.execute("""
                        SELECT id_usuario, nombre, correo, puntaje_total, nivel 
                        FROM usuarios WHERE rol = 'estudiante' 
                        AND (nombre LIKE %s OR id_usuario = %s OR puntaje_total = %s)
                        ORDER BY puntaje_total DESC;
                    """, (termino, int(q.strip()), int(q.strip())))
                else:
                    cursor.execute("""
                        SELECT id_usuario, nombre, correo, puntaje_total, nivel 
                        FROM usuarios WHERE rol = 'estudiante' 
                        AND nombre LIKE %s
                        ORDER BY puntaje_total DESC;
                    """, (termino,))
                lista_usuarios = cursor.fetchall()
            conn.close()
    else:
        estudiantes_raw = obtener_todos_los_estudiantes()
        lista_usuarios = [(e["id_usuario"], e["nombre"], e["correo"], e["puntaje_total"], e["nivel"]) for e in estudiantes_raw]
    
    return templates.TemplateResponse(
        request=request,
        name="Ver-estudiantes.html",
        context={"usuarios": lista_usuarios, "query_busqueda": q}
    )

@router.get("/estudiantes/eliminar/{id_usuario}")
def dar_baja_estudiante(id_usuario: int):
    exito, msg = dar_baja_estudiante_db(id_usuario)
    return RedirectResponse(url=f"/admin?msg={msg}", status_code=303)

@router.get("/nuevas-preguntas", response_class=HTMLResponse)
def vista_nuevas_preguntas(request: Request):
    return templates.TemplateResponse(request=request, name="Nuevas_preguntas.html")

@router.get("/ranking", response_class=HTMLResponse)
def ver_ranking(request: Request):
    estudiantes_ranking = obtener_ranking_top_10()
    return templates.TemplateResponse(
        request=request, 
        name="Ver-estudiantes.html", 
        context={"estudiantes": estudiantes_ranking}
    )

@router.get("/estudiantes/ver/{id_usuario}", response_class=HTMLResponse)
def ver_expediente_estudiante(id_usuario: int, request: Request):
    from models.admin import obtener_conexion
    conn = obtener_conexion()
    estudiante = None
    historial_respuestas = []
    logros_ganados = []

    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT id_usuario, nombre, correo, puntaje_total, nivel, dias_racha, fecha_registro 
                    FROM usuarios WHERE id_usuario = %s AND rol = 'estudiante';
                """, (id_usuario,))
                usuario_db = cursor.fetchone()
                
                if usuario_db:
                    estudiante = {
                        "id": usuario_db[0], "nombre": usuario_db[1], "correo": usuario_db[2],
                        "puntos": usuario_db[3], "nivel": usuario_db[4], "racha": usuario_db[5],
                        "registro": usuario_db[6]
                    }
                    cursor.execute("""
                        SELECT m.nombre, p.pregunta, ru.es_correcta, ru.fecha_respuesta
                        FROM respuestas_usuario ru
                        JOIN preguntas p ON ru.id_pregunta = p.id_pregunta
                        JOIN materias m ON p.id_materia = m.id_materia
                        WHERE ru.id_usuario = %s ORDER BY ru.fecha_respuesta DESC;
                    """, (id_usuario,))
                    for row in cursor.fetchall():
                        historial_respuestas.append({"materia": row[0], "pregunta": row[1], "correcta": row[2], "fecha": row[3]})
                    cursor.execute("""
                        SELECT l.nombre, l.descripcion, l.imagen_medalla, lu.fecha_ganado
                        FROM logros_usuario lu
                        JOIN logros l ON lu.id_logro = l.id_logro
                        WHERE lu.id_usuario = %s ORDER BY lu.fecha_ganado DESC;
                    """, (id_usuario,))
                    for row in cursor.fetchall():
                        logros_ganados.append({"nombre": row[0], "descripcion": row[1], "icono": row[2], "fecha": row[3]})
        except Exception as e:
            print(f"⚠️ Error al consultar expediente: {e}")
        finally:
            conn.close()

    if not estudiante:
        return RedirectResponse(url="/admin/estudiantes?msg=Estudiante no encontrado", status_code=303)

    return templates.TemplateResponse(
        request=request,
        name="admin-ver-mas.html", 
        context={"estudiante": estudiante, "respuestas": historial_respuestas, "logros": logros_ganados}
    )