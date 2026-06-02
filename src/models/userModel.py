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
                    str(matricula).strip(),
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
    # ACCIÓN: ACTUALIZAR CONTRASEÑA
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
            # Añadido .strip() para limpiar cualquier espacio en blanco invisible del QR
            cursor.execute(query, (str(matricula).strip(),))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al registrar asistencia en BD: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

    # =========================================================================
    # CONSULTAR PRESENTES DE HOY (Filtrado y Reparado) 🚀
    # =========================================================================
    def consultar_presentes_hoy(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # CORREGIDO: '%h:%i %p' genera de manera correcta el formato 'Hora:Minuto AM/PM'
        query = """
        SELECT a.matricula, al.nombre, DATE_FORMAT(a.hora, '%%h:%%i %%p') AS hora 
        FROM asistencias a
        INNER JOIN alumnos al ON STRIP(a.matricula) = STRIP(al.matricula)
        WHERE a.fecha = CURDATE() AND al.matricula != 'DOCENTE'
        ORDER BY a.hora DESC
        """
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al consultar alumnos presentes: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    # =========================================================================
    # CONSULTAR AUSENTES DE HOY (Filtrado) 🚀
    # =========================================================================
    # =========================================================================
    # CONSULTAR PRESENTES DE HOY (Filtrado y Corregido con TRIM) 🚀
    # =========================================================================
    def consultar_presentes_hoy(self):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # SOLUCIÓN: Usamos un string normal y dejamos los % simples para MySQL
        query = (
            "SELECT a.matricula, al.nombre, DATE_FORMAT(a.hora, '%h:%i %p') AS hora "
            "FROM asistencias a "
            "INNER JOIN alumnos al ON TRIM(a.matricula) = TRIM(al.matricula) "
            "WHERE a.fecha = CURDATE() AND al.matricula != 'DOCENTE' "
            "ORDER BY a.hora DESC"
        )
        try:
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"Error al consultar alumnos presentes: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    def verificar_asistencia_existente(self, matricula):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Busca si la matrícula ya tiene un registro con la fecha del día de hoy
        query = "SELECT COUNT(*) FROM asistencias WHERE TRIM(matricula) = TRIM(%s) AND fecha = CURDATE()"
        try:
            cursor.execute(query, (matricula,))
            resultado = cursor.fetchone()
            return resultado[0] > 0  # Devuelve True si ya existe, False si está limpio
        except Exception as e:
            print(f"Error al verificar duplicados: {e}")
            return False
        finally:
            cursor.close()
            conn.close()