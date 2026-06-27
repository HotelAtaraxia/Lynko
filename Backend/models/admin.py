from config.database import obtener_conexion

def obtener_metricas_dashboard():
    conn = obtener_conexion()
    total_estudiantes = total_preguntas = promedio_exp = 0
    ultimas_preguntas = mejores_estudiantes = []
    
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM usuarios WHERE rol = 'estudiante';")
                total_estudiantes = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM preguntas;")
                total_preguntas = cursor.fetchone()[0]
                
                cursor.execute("SELECT COALESCE(AVG(puntaje_total), 0) FROM usuarios WHERE rol = 'estudiante';")
                promedio_exp = round(cursor.fetchone()[0], 1)
                
                cursor.execute("""
                    SELECT p.id_pregunta, m.nombre, p.pregunta 
                    FROM preguntas p 
                    JOIN materias m ON p.id_materia = m.id_materia 
                    ORDER BY p.id_pregunta DESC LIMIT 5;
                """)
                ultimas_preguntas = cursor.fetchall()
                
                cursor.execute("""
                    SELECT id_usuario, nombre, correo, puntaje_total, nivel 
                    FROM usuarios 
                    WHERE rol = 'estudiante' 
                    ORDER BY puntaje_total DESC LIMIT 5;
                """)
                mejores_estudiantes = cursor.fetchall()
        finally:
            conn.close()
            
    return total_estudiantes, total_preguntas, promedio_exp, ultimas_preguntas, mejores_estudiantes
