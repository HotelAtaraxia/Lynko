from config.database import obtener_conexion

def obtener_datos_panel_admin():
    """
    Recupera todas las métricas, historial de exámenes, listado de preguntas 
    y datos de estudiantes necesarios para renderizar el panel principal.
    """
    conn = obtener_conexion()
    preguntas, usuarios, metricas_materias, mejores_examenes = [], [], [], []
    
    if conn:
        try:
            with conn.cursor() as cursor:
                # 1. Métricas de efectividad por materia
                cursor.execute("""
                    SELECT m.nombre, COUNT(i.id_intento), COALESCE(ROUND(AVG(i.nota_final), 1), 0), COUNT(CASE WHEN i.aprobado THEN 1 END)
                    FROM materias m LEFT JOIN examenes e ON m.id_materia = e.id_materia
                    LEFT JOIN intentos_examen i ON e.id_examen = i.id_examen GROUP BY m.nombre;
                """)
                metricas_materias = cursor.fetchall() or []
                
                # 2. Historial de mejores exámenes rendidos
                cursor.execute("""
                    SELECT u.nombre, e.titulo, m.nombre, i.nota_final FROM intentos_examen i
                    JOIN usuarios u ON i.id_usuario = u.id_usuario JOIN examenes e ON i.id_examen = e.id_examen
                    JOIN materias m ON e.id_materia = m.id_materia ORDER BY i.nota_final DESC;
                """)
                mejores_examenes = cursor.fetchall() or []

                # 3. Listado completo de preguntas del sistema
                cursor.execute("""
                    SELECT p.id_pregunta, p.pregunta, m.nombre, p.nivel_dificultad 
                    FROM preguntas p JOIN materias m ON p.id_materia = m.id_materia 
                    ORDER BY p.id_pregunta ASC;
                """)
                preguntas = cursor.fetchall() or []

                # 4. Listado de estudiantes y suma de sus logros obtenidos
                cursor.execute("""
                    SELECT u.id_usuario, u.nombre, u.correo, u.puntaje_total, COUNT(lu.id_logro) FROM usuarios u
                    LEFT JOIN logros_usuario lu ON u.id_usuario = lu.id_usuario WHERE u.rol = 'estudiante' 
                    GROUP BY u.id_usuario, u.nombre, u.correo, u.puntaje_total
                    ORDER BY u.id_usuario ASC;
                """)
                usuarios = cursor.fetchall() or []
        except Exception as e:
            print(f"⚠️ Error en consultas del Panel Admin (Modelo): {e}")
        finally:
            conn.close()

    # Si falló la conexión o la BD está vacía, se inyectan los valores por defecto
    if not metricas_materias:
        metricas_materias = [("Matemáticas", 0, 0, 0), ("Español", 0, 0, 0), ("Biología", 0, 0, 0)]

    return preguntas, usuarios, metricas_materias, mejores_examenes


def crear_nueva_pregunta_db(pregunta: str, id_materia: int, nivel: int, puntos: int, 
                            opcion1: str, opcion2: str, opcion3: str, correcta: str) -> tuple[bool, str]:
    """
    Inserta de forma transaccional una nueva pregunta y sus opciones asociadas.
    Retorna un booleano indicando el éxito y un mensaje con el estado del proceso.
    """
    conn = obtener_conexion()
    if not conn:
        print("❌ [ERROR DE CONEXIÓN]: No se pudo conectar a PostgreSQL.")
        return False, "Error de conexión con el servidor"
        
    try:
        opcion_correcta_int = int(correcta)
        with conn.cursor() as cursor:
            # 1. Insertamos la pregunta principal
            cursor.execute("""
                INSERT INTO preguntas (id_materia, pregunta, nivel_dificultad, puntos_recompensa) 
                VALUES (%s, %s, %s, %s) 
                RETURNING id_pregunta;
            """, (id_materia, pregunta, nivel, puntos))
            
            id_p = cursor.fetchone()[0]
            
            # 2. Insertamos las opciones evaluando estrictamente la opción correcta
            cursor.execute("INSERT INTO opciones (id_pregunta, opcion, es_correcta) VALUES (%s, %s, %s);", 
                           (id_p, opcion1, True if opcion_correcta_int == 1 else False))
                           
            cursor.execute("INSERT INTO opciones (id_pregunta, opcion, es_correcta) VALUES (%s, %s, %s);", 
                           (id_p, opcion2, True if opcion_correcta_int == 2 else False))
                           
            cursor.execute("INSERT INTO opciones (id_pregunta, opcion, es_correcta) VALUES (%s, %s, %s);", 
                           (id_p, opcion3, True if opcion_correcta_int == 3 else False))
            
            # 3. Confirmamos los cambios de manera persistente
            conn.commit()
            print("✅ [ÉXITO] Pregunta y opciones guardadas correctamente en la base de datos.")
            return True, "Pregunta añadida correctamente al banco"
            
    except Exception as e:
        if conn:
            conn.rollback()  
        print(f"❌ [ERROR CRÍTICO EN BD]: {e}")
        return False, "Error interno al guardar la pregunta"
    finally:
        conn.close()


def obtener_listado_preguntas_completo() -> list:
    """
    Recupera el catálogo extendido de preguntas estructurando sus respuestas en formato JSON.
    """
    conn = obtener_conexion()
    lista_preguntas = []
    
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT p.id_pregunta, m.nombre AS materia, p.pregunta, p.nivel_dificultad, p.puntos_recompensa,
                           json_agg(json_build_object('opcion', o.opcion, 'es_correcta', o.es_correcta)) AS opciones
                    FROM preguntas p
                    JOIN materias m ON p.id_materia = m.id_materia
                    LEFT JOIN opciones o ON p.id_pregunta = o.id_pregunta
                    GROUP BY p.id_pregunta, m.nombre
                    ORDER BY p.id_pregunta DESC;
                """)
                for row in cursor.fetchall():
                    lista_preguntas.append({
                        "id_pregunta": row[0],
                        "materia": row[1],
                        "pregunta": row[2],
                        "nivel": row[3],
                        "puntos": row[4],
                        "opciones": row[5]
                    })
        except Exception as e:
            print(f"⚠️ Error al listar preguntas y respuestas para el administrador: {e}")
        finally:
            conn.close()
            
    return lista_preguntas


def eliminar_pregunta_db(id_pregunta: int) -> tuple[bool, str]:
    """
    Remueve permanentemente una pregunta del catálogo por su ID.
    """
    conn = obtener_conexion()
    if not conn:
        return False, "Error de conexión"
        
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM preguntas WHERE id_pregunta = %s;", (id_pregunta,))
            conn.commit()
        return True, "Pregunta eliminada del sistema"
    except Exception as e:
        print(f"⚠️ Error al eliminar la pregunta {id_pregunta}: {e}")
        return False, "No se pudo eliminar la pregunta"
    finally:
        conn.close()


def editar_datos_estudiante_db(id_usuario: int, nombre: str, correo: str, puntaje_total: int) -> tuple[bool, str]:
    """
    Actualiza la información principal de un usuario con rol de estudiante.
    """
    conn = obtener_conexion()
    if not conn:
        return False, "Error de conexión"
        
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE usuarios 
                SET nombre = %s, 
                    correo = %s, 
                    puntaje_total = %s 
                WHERE id_usuario = %s AND rol = 'estudiante';
            """, (nombre, correo, puntaje_total, id_usuario))
            conn.commit()
        return True, "Datos del estudiante actualizados correctamente"
    except Exception as e:
        print(f"⚠️ Error al actualizar el estudiante {id_usuario}: {e}")
        return False, "No se pudieron guardar los cambios del alumno"
    finally:
        conn.close()


def obtener_todos_los_estudiantes() -> list:
    """
    Retorna la nómina completa de estudiantes registrados en el sistema.
    """
    conn = obtener_conexion()
    lista_estudiantes = []
    
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT id_usuario, nombre, correo, puntaje_total, nivel, dias_racha
                    FROM usuarios
                    WHERE rol = 'estudiante'
                    ORDER BY id_usuario ASC;
                """)
                for row in cursor.fetchall():
                    lista_estudiantes.append({
                        "id_usuario": row[0],
                        "nombre": row[1],
                        "correo": row[2],
                        "puntaje_total": row[3],
                        "nivel": row[4],
                        "dias_racha": row[5]
                    })
        except Exception as e:
            print(f"⚠️ Error al listar estudiantes para el administrador: {e}")
        finally:
            conn.close()
            
    return lista_estudiantes


def dar_baja_estudiante_db(id_usuario: int) -> tuple[bool, str]:
    """
    Elimina físicamente a un estudiante de la base de datos basándose en su ID.
    """
    conn = obtener_conexion()
    if not conn:
        return False, "Error de conexión"
        
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s AND rol = 'estudiante';", (id_usuario,))
            conn.commit()
        return True, "Estudiante dado de baja correctamente"
    except Exception as e:
        print(f"⚠️ Error al eliminar al usuario {id_usuario}: {e}")
        return False, "No se pudo eliminar al estudiante"
    finally:
        conn.close()


def obtener_ranking_top_10() -> list:
    """
    Consulta los 10 mejores puntajes globales de estudiantes en el ecosistema Lynko.
    """
    conn = obtener_conexion()
    estudiantes_ranking = []
    
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT nombre, nivel, puntaje_total 
                    FROM usuarios 
                    WHERE rol = 'estudiante' 
                    ORDER BY puntaje_total DESC LIMIT 10;
                """)
                estudiantes_ranking = cursor.fetchall()
        except Exception as e:
            print(f"⚠️ Error al obtener el ranking: {e}")
        finally:
            conn.close()
            
    return estudiantes_ranking
