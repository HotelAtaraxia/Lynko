import re

from config.database import obtener_conexion

def verificar_credenciales_login(correo: str, contrasena: str):
    conn = obtener_conexion()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT id_usuario, correo, rol 
                    FROM usuarios 
                    WHERE correo = %s AND contraseña = %s AND activo = TRUE;
                """, (correo, contrasena))
                return cursor.fetchone()
        except Exception as e:
            print(f"⚠️ Error en login modelo: {e}")
        finally:
            conn.close()
    return None

def registrar_nuevo_estudiante(nombre: str, correo: str, contrasena: str):
    # Validaciones de seguridad de la contraseña
    if len(contrasena) < 8 or not re.search(r"[a-zA-Z]", contrasena) or not re.search(r"[0-9]", contrasena) or len(set(contrasena)) < 4:
        return False, "Contraseña insegura. Debe tener mínimo 8 caracteres con letras y números."

    conn = obtener_conexion()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO usuarios (nombre, correo, contraseña, rol, puntaje_total, activo) 
                    VALUES (%s, %s, %s, 'estudiante', 0, TRUE) RETURNING id_usuario;
                """, (nombre, correo, contrasena))
                nuevo_id = cursor.fetchone()[0]
                
                try:
                    cursor.execute("INSERT INTO logros_usuario (id_usuario, id_logro) VALUES (%s, 1);", (nuevo_id,))
                except Exception:
                    pass
                
                conn.commit()
                return True, nuevo_id
        except Exception as e:
            print(f"⚠️ Error al registrar modelo: {e}")
            return False, "El correo ya está registrado"
        finally:
            conn.close()
    return False, "Error de conexión con la base de datos"
