from config.database import obtener_conexion
from datetime import datetime

def obtener_datos_base_estudiante(cursor, id_usuario: int):
    cursor.execute("""
        SELECT nombre, COALESCE(puntaje_total, 0), correo, contraseña, COALESCE(nivel, 0), COALESCE(dias_racha, 0)
        FROM usuarios WHERE id_usuario = %s;
    """, (id_usuario,))
    res = cursor.fetchone()
    
    if res:
        nombre_u, puntos_u, correo_u, contra_u, nivel_bd, racha_bd = res[0], res[1], res[2], res[3], res[4], res[5]
        
        if puntos_u >= 1000:
            nivel_calculado = 4
        elif puntos_u >= 500:
            nivel_calculado = 3
        elif puntos_u >= 200:
            nivel_calculado = 2
        elif puntos_u >= 100:
            nivel_calculado = 1
        else:
            nivel_calculado = 0  

        if nivel_calculado != nivel_bd:
            cursor.execute("UPDATE usuarios SET nivel = %s WHERE id_usuario = %s;", (nivel_calculado, id_usuario))

        return {
            "nombre": nombre_u, 
            "puntos": puntos_u, 
            "nivel": nivel_calculado,  
            "racha": racha_bd,          
            "correo": correo_u,
            "contrasena": contra_u,     
            "contraseña": contra_u      
        }
    return {"nombre": "Estudiante", "puntos": 0, "nivel": 0, "racha": 0, "correo": "", "contrasena": "", "contraseña": ""}

def registrar_sesion(id_usuario: int, token: str):
    conn = obtener_conexion()
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO sesiones (id_usuario, token_sesion, fecha_inicio)
            VALUES (%s, %s, CURRENT_TIMESTAMP);
        """, (id_usuario, token))
        conn.commit()
    conn.close()

def consultar_preguntas_landing():
    conn = obtener_conexion()
    preguntas_data = []
    if conn:
        try:
            with conn.cursor() as cursor:
                query = """
                    SELECT DISTINCT ON (p.id_materia) 
                        p.id_pregunta, m.nombre AS materia, p.pregunta, p.puntos_recompensa
                    FROM preguntas p
                    JOIN materias m ON p.id_materia = m.id_materia
                    ORDER BY p.id_materia, RANDOM();
                """
                cursor.execute(query)
                filas = cursor.fetchall()
                for fila in filas:
                    id_preg = fila[0]
                    cursor.execute("""
                        SELECT opcion, es_correcta
                        FROM opciones
                        WHERE id_pregunta = %s
                        ORDER BY RANDOM();
                    """, (id_preg,))
                    filas_opciones = cursor.fetchall()
                    opciones = [{"opcion": o[0], "es_correcta": bool(o[1])} for o in filas_opciones]
                    preguntas_data.append({
                        "id_pregunta": id_preg,
                        "materia": fila[1].upper(),
                        "pregunta": fila[2],
                        "puntos": fila[3],
                        "opciones": opciones
                    })
        finally:
            conn.close()
    return preguntas_data

def consultar_dashboard_estudiante(id_usuario: int):
    conn = obtener_conexion()
    datos = {"nombre": "Estudiante", "puntaje_total": 0, "nivel": 0, "dias_racha": 0}
    progreso_estudiante = {"Matemáticas": 0, "Español": 0, "Biología": 0}
    imagenes_materias = {"Matemáticas": None, "Español": None, "Biología": None}
    
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT nombre, link_imagen FROM materias;")
                for row in cursor.fetchall():
                    if row[0] in imagenes_materias:
                        imagenes_materias[row[0]] = row[1]

                cursor.execute("SELECT nombre, puntaje_total, nivel, dias_racha FROM usuarios WHERE id_usuario = %s AND activo = true", (id_usuario,))
                usuario_db = cursor.fetchone()
                if usuario_db:
                    datos = {"nombre": usuario_db[0], "puntaje_total": usuario_db[1], "nivel": usuario_db[2], "dias_racha": usuario_db[3]}

                query_progreso = """
                    SELECT m.nombre AS materia, COUNT(p.id_pregunta) AS total_preguntas,
                        COUNT(ru.id_intento_respuesta) FILTER (WHERE ru.es_correcta = true) AS correctas
                    FROM materias m
                    LEFT JOIN preguntas p ON m.id_materia = p.id_materia
                    LEFT JOIN respuestas_usuario ru ON p.id_pregunta = ru.id_pregunta AND ru.id_usuario = %s
                    GROUP BY m.id_materia, m.nombre
                """
                cursor.execute(query_progreso, (id_usuario,))
                for fila in cursor.fetchall():
                    total, correctas = fila[1], fila[2]
                    progreso_estudiante[fila[0]] = min(int((correctas / total) * 100), 100) if total > 0 else 0
        finally:
            conn.close()
    return datos, progreso_estudiante, imagenes_materias
 
def registrar_sesion_db(id_usuario: int): 
    return True 
