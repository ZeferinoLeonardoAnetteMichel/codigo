from models.databaseModel import Database
import bcrypt

class UsuarioModel:

    def __init__(self):
        self.db = Database()

    # =========================================================================
    # VALIDADOR: ¿EL CORREO YA EXISTE?
    # =========================================================================
    def correo_existe(self, correo):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            # Buscamos en la tabla alumnos
            cursor.execute("SELECT matricula FROM alumnos WHERE correo = %s", (correo,))
            existe = cursor.fetchone() is not None
            return existe
        except Exception as e:
            print(f"Error al verificar correo: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    # =========================================================================
    # ACCIÓN: REGISTRAR ALUMNO O DOCENTE
    # =========================================================================
    def registrar_alumno(self, matricula, nombre, correo, password):
        conn = self.db.get_connection()
        cursor = conn.cursor()

        # Encriptamos la contraseña con bcrypt de forma segura
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        query = """
        INSERT INTO alumnos (matricula, nombre, correo, password)
        VALUES (%s, %s, %s, %s)
        """

        try:
            cursor.execute(
                query,
                (
                    matricula,
                    nombre,
                    correo,
                    password_hash.decode("utf-8") if isinstance(password_hash, bytes) else password_hash
                )
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al registrar en la BD: {e}")
            raise e
        finally:
            cursor.close()
            conn.close()

    # =========================================================================
    # ACCIÓN: INICIAR SESIÓN (LOGIN)
    # =========================================================================
    def login_alumno(self, correo, password):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT * FROM alumnos WHERE correo = %s
        """

        try:
            cursor.execute(query, (correo,))
            user = cursor.fetchone()

            if user:
                # Comparamos la contraseña en texto plano con el hash guardado
                password_correcta = bcrypt.checkpw(
                    password.encode("utf-8"),
                    user["password"].encode("utf-8")
                )
                if password_correcta:
                    return user  # Retorna el diccionario completo del usuario activo

            return None
        except Exception as e:
            print(f"Error en login_alumno: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    # =========================================================================
    # ACCIÓN: ACTUALIZAR CONTRASEÑA (Reparada de la sección rota de Git)
    # =========================================================================
    def actualizar_password(self, correo, nueva_password):
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(nueva_password.encode("utf-8"), salt)
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        sql = """UPDATE alumnos SET password = %s WHERE correo = %s"""
        try:
            cursor.execute(sql, (hashed_pw.decode("utf-8"), correo))
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("ERROR ACTUALIZANDO PASSWORD:", e)
            return False
        finally:
            cursor.close()
            conn.close()

    # =========================================================================
    # NUEVO MÓDULO: INSERTAR ASISTENCIA DESDE EL LECTOR QR 🚀
    # =========================================================================
    def insertar_asistencia(self, matricula):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Sentencia SQL estándar para guardar la matrícula, el día y la hora exacta del escaneo
        query = """
        INSERT INTO asistencias (matricula, fecha, hora, estatus)
        VALUES (%s, CURDATE(), CURTIME(), 'Presente')
        """
        try:
            cursor.execute(query, (matricula,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al registrar asistencia en BD: {e}")
            return False
        finally:
            cursor.close()
            conn.close()