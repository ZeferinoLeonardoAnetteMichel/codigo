from models.databaseModel import Database
import bcrypt
import uuid
from datetime import datetime, timedelta

class UsuarioModel:
    def __init__(self):
        self.db = Database()

    # --- MÉTODO CORREGIDO Y UNIFICADO ---
    def login_usuario(self, correo, password):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Intentar en alumnos
            cursor.execute("SELECT *, 'alumno' AS rol FROM alumnos WHERE correo = %s", (correo,))
            user = cursor.fetchone()
            
            # Si no, buscar en usuarios (docentes)
            if not user:
                cursor.execute("SELECT *, 'maestro' AS rol FROM usuarios WHERE correo = %s", (correo,))
                user = cursor.fetchone()

            if user:
                # Asegurar que el hash almacenado sea bytes antes de comparar
                stored_password = user["password"]
                if isinstance(stored_password, str):
                    stored_password = stored_password.encode("utf-8")
                
                if bcrypt.checkpw(password.encode("utf-8"), stored_password):
                    user["id_usuario"] = user.get("id_usuario") or user.get("id_alumno")                
                    return user
        except Exception as e:
            print("ERROR LOGIN:", e)
            return None
        finally:
            cursor.close(); conn.close()

    # --- MÉTODO QUE FALTABA (evita el error 'no attribute') ---
    def correo_existe(self, correo):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        query = "SELECT correo FROM alumnos WHERE correo = %s UNION SELECT correo FROM usuarios WHERE correo = %s"
        try:
            cursor.execute(query, (correo, correo))
            return cursor.fetchone() is not None
        finally:
            cursor.close(); conn.close()

    def registrar_alumno(self, matricula, nombre, apellido_paterno, apellido_materno, grado, grupo, correo, password):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        # Generar hash y DECODIFICAR a string (importante)
        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        query = "INSERT INTO alumnos (matricula, nombre, apellido_paterno, apellido_materno, grado, grupo, correo, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        try:
            cursor.execute(query, (matricula, nombre, apellido_paterno, apellido_materno, grado, grupo, correo, password_hash))
            conn.commit()
            return True
        finally:
            cursor.close(); conn.close()

    def registrar_docente(self, nombre, correo, password):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        # Generar hash y DECODIFICAR a string (importante)
        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        query = "INSERT INTO usuarios (nombre, correo, password, rol) VALUES (%s, %s, %s, 'DOCENTE')"
        try:
            cursor.execute(query, (nombre, correo, password_hash))
            conn.commit()
            return True
        finally:
            cursor.close(); conn.close()
    # ... (Mantén aquí tus otros métodos: actualizar_password, insertar_asistencia, consultar_presentes_hoy, rotar_codigo_qr, obtener_qr_activo)
        
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
            
    # En tu AuthController
    def obtener_grupos_de_maestro(self, id_maestro):
    # Debug: Imprime para ver si el id_maestro llega bien
        print(f"DEBUG: Consultando grupos para maestro ID: {id_maestro}")
    
        conn = self.user_model.db.get_connection()
        cursor = conn.cursor(dictionary=True)
    # Asegúrate de que esta tabla y columnas existan
        cursor.execute("SELECT nombre_grupo FROM maestro_grupo WHERE id_maestro = %s", (id_maestro,))
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
    
        grupos = [r['nombre_grupo'] for r in resultados]
        print(f"DEBUG: Grupos encontrados: {grupos}")
        return grupos

    def insertar_asistencia(self, matricula, id_maestro, grupo): 
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id_alumno FROM alumnos WHERE matricula = %s", (matricula,))
            res = cursor.fetchone()
            if not res: return False, "Alumno no encontrado."
            id_alumno = res[0]
            cursor.execute("SELECT id_qr FROM codigos_qr WHERE activo = 1 LIMIT 1")
            res_qr = cursor.fetchone()
            if not res_qr: return False, "No hay QR activo. Genera uno primero."
            id_qr = res_qr[0]
            query = """INSERT INTO asistencia (id_alumno, id_qr, matricula, fecha, hora, estado, id_maestro) 
        VALUES (%s, %s, %s, CURDATE(), CURTIME(), 'PRESENTE', %s)"""
            cursor.execute(query, (id_alumno, id_qr, matricula, id_maestro))
            conn.commit()
            return True, "Asistencia registrada con éxito."
        except Exception as e:
            print(f"DEBUG ERROR DB: {e}")
            return False, "Error de base de datos."
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

    def consultar_presentes_hoy(self, nombre_grupo, id_maestro):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Filtramos por maestro, por la fecha y por el grupo específico
        query = """
        SELECT a.matricula, al.nombre, a.fecha, a.hora, a.estado
        FROM asistencia a
        INNER JOIN alumnos al ON TRIM(a.matricula) = TRIM(al.matricula)
        WHERE a.id_maestro = %s 
        AND a.fecha = CURDATE()
        AND CONCAT(CAST(al.grado AS CHAR), '-', TRIM(al.grupo)) = %s
        """
        try:
            # Imprimimos los filtros para confirmar qué estamos buscando
            print(f"DEBUG: Buscando para Maestro: {id_maestro}, Grupo: {nombre_grupo}")
            cursor.execute(query, (id_maestro, nombre_grupo))
            return cursor.fetchall()
        finally:
            cursor.close(); conn.close()

    def rotar_codigo_qr(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE codigos_qr SET activo = 0")
            nuevo_codigo = str(uuid.uuid4())
            fecha_exp = datetime.now() + timedelta(minutes=1)
            cursor.execute("""
            INSERT INTO codigos_qr
            (codigo, fecha_expiracion, activo)
            VALUES (%s, %s, 1)
        """, (nuevo_codigo, fecha_exp))
            conn.commit()
            return True
        except Exception as e:
            print("Error rotando QR:", e)
            return False
        finally:
            cursor.close()
            conn.close()
            
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