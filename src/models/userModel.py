from models.databaseModel import Database
import bcrypt
class UsuarioModel:

    def __init__(self):
        self.db = Database()

    def correo_existe(self, correo):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT matricula FROM alumnos WHERE correo = %s", (correo,))
            return cursor.fetchone() is not None
        finally:
            cursor.close(); conn.close()
    
    def login_alumno(self, correo, password):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM alumnos WHERE correo = %s"
        try:
            cursor.execute(query, (correo,))
            user = cursor.fetchone()
            if user:
                password_correcta = bcrypt.checkpw(
                    password.encode("utf-8"),
                    user["password"].encode("utf-8")
                )
                if password_correcta:
                    return user
            return None
        except Exception as e:
            print(f"Error en login_alumno: {e}")
            return None
        finally:
            cursor.close(); conn.close()

    def registrar_alumno(self, matricula, nombre, apellido_paterno, apellido_materno, grado, grupo, correo, password):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        query = """
        INSERT INTO alumnos (matricula, nombre, apellido_paterno, apellido_materno, grado, grupo, correo, password) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        try:
            cursor.execute(query, (matricula, nombre, apellido_paterno, apellido_materno, grado, grupo, correo, password_hash))            
            conn.commit()
            return True
        finally:
            cursor.close(); conn.close()
            
    def actualizar_password(self, correo, nueva_password):
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(nueva_password.encode("utf-8"), salt)
        conn = self.db.get_connection()
        cursor = conn.cursor()
        sql = "UPDATE alumnos SET password = %s WHERE correo = %s"
        try:
            cursor.execute(sql, (hashed_pw.decode("utf-8"), correo))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("ERROR ACTUALIZANDO PASSWORD:", e)
            return False
        finally:
            cursor.close(); conn.close()

    def insertar_asistencia(self, matricula):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id_alumno FROM alumnos WHERE TRIM(matricula) = TRIM(%s)", (matricula,))
            res = cursor.fetchone()
            if not res: return False
            id_alumno = res[0]
            cursor.execute("SELECT id_qr FROM codigos_qr WHERE activo = 1 LIMIT 1")
            res_qr = cursor.fetchone()
            id_qr = res_qr[0] if res_qr else 1
            query = """
            INSERT INTO asistencia (id_alumno, id_qr, matricula, fecha, hora, estatus)
            VALUES (%s, %s, %s, CURDATE(), CURTIME(), 'Presente')
            """
            cursor.execute(query, (id_alumno, id_qr, matricula))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error en insertar_asistencia: {e}")
            return False
        finally:
            cursor.close(); conn.close()

    def verificar_asistencia_existente(self, matricula):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = "SELECT COUNT(*) FROM asistencia WHERE TRIM(matricula) = TRIM(%s) AND fecha = CURDATE()"
        try:
            cursor.execute(query, (matricula,))
            return cursor.fetchone()[0] > 0
        finally:
            cursor.close(); conn.close()

    def consultar_presentes_hoy(self, nombre_grupo):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = """
        SELECT
            a.matricula,
            al.nombre,
            DATE_FORMAT(a.fecha, '%Y-%m-%d') AS fecha,
            DATE_FORMAT(a.hora, '%h:%i %p') AS hora,
            a.estatus
        FROM asistencia a
        INNER JOIN alumnos al
            ON TRIM(a.matricula) = TRIM(al.matricula)
        WHERE CONCAT(al.grado, '-', al.grupo) = %s
        AND al.matricula != 'DOCENTE'
        ORDER BY a.fecha DESC, a.hora DESC
        """
        try:
            cursor.execute(query, (nombre_grupo,))
            datos = cursor.fetchall()
            print("DEBUG SQL:", datos)
            return datos
        except Exception as e:
            print(f"Error en consultar_presentes_hoy: {e}")
            return []
        finally:
            cursor.close(); conn.close()
    import uuid 

    def rotar_codigo_qr(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE codigos_qr SET activo = 0")
            nuevo_codigo = str(uuid.uuid4())
            cursor.execute("INSERT INTO codigos_qr (codigo, activo) VALUES (%s, 1)", (nuevo_codigo,))
            conn.commit()
            return True
        finally:
            cursor.close(); conn.close()
            
    def obtener_qr_activo(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("""
            SELECT id_qr, codigo
            FROM codigos_qr
            WHERE activo = 1
            LIMIT 1
        """)
            return cursor.fetchone()
        finally:
            cursor.close()
            conn.close()