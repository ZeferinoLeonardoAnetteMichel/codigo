from models.userModel import UsuarioModel


class AuthController:
    def __init__(self):
        self.user_model = UsuarioModel()
        self.usuario_actual_id = None
    def registrar(self, rol, matricula, nombre, apellido_paterno, apellido_materno, grado, grupo, correo, password):
        try:
            if self.user_model.correo_existe(correo):
                return False, "El correo ya está registrado."

            if rol == "alumno":
                self.user_model.registrar_alumno(matricula, nombre, apellido_paterno, apellido_materno, grado, grupo, correo, password)
            else:
                nombre_completo = f"{nombre} {apellido_paterno}".strip()
                self.user_model.registrar_docente(nombre_completo, correo, password)
            return True, "Registrado exitosamente"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def login(self, correo, password, page):
        user = self.user_model.login_usuario(correo, password)
        if user:
            # Intentamos obtener el ID, buscando primero por 'id_usuario' y luego por 'id_alumno'
            id_real = user.get("id_usuario") or user.get("id_alumno")
            
            if id_real:
                self.set_usuario_actual(id_real)
                return user, "Correcto"
            else:
                return None, "Error: El usuario no tiene un ID válido."
        return None, "Correo o contraseña incorrectos"

    def verificar_codigo_recuperacion(self, correo, codigo_ingresado):
        try:
            codigo_guardado = self.codigos_recuperacion.get(correo)
            if not codigo_guardado:
                return False, "No se ha solicitado un código para este correo o ya venció."
            
            if str(codigo_guardado) == str(codigo_ingresado).strip():
                del self.codigos_recuperacion[correo]
                return True, "Código verificado con éxito."
            else:
                return False, "El código introducido es incorrecto."
        except Exception as e:
            return False, f"Error al verificar código: {str(e)}"
        

    def cambiar_password(self, correo, nueva_password):
        try:
            if hasattr(self.user_model, "actualizar_password"):
                return self.user_model.actualizar_password(correo, nueva_password)
            
            print(f"[Simulación] Contraseña de {correo} cambiada a {nueva_password}")
            return True
        except Exception as e:
            print(f"Error al cambiar password: {e}")
            return False

    def registrar_asistencia_qr(self,matricula,id_maestro,grupo):
        try:
            if self.user_model.verificar_asistencia_existente(matricula):
                    return False, "Ya registraste tu asistencia el día de hoy."
            exito = self.user_model.insertar_asistencia(matricula, id_maestro, grupo)     
            if exito:
                return True, "Asistencia registrada con éxito."
            else:
                return False, "Error al guardar en la base de datos."
        except Exception as e:
            print(f"Error en controlador de asistencia: {e}")
            return False, "Error interno del sistema."
        
    def obtener_qr_activo(self):
        return self.user_model.obtener_qr_activo()
    def rotar_codigo_qr(self):
        return self.user_model.rotar_codigo_qr()

    def obtener_alumnos_presentes(self, nombre_grupo, id_maestro):
        try:
            datos = self.user_model.consultar_presentes_hoy(nombre_grupo, id_maestro)
            print(f"DEBUG: Datos recibidos para {nombre_grupo}: {datos}")
            return datos if datos else []
        except Exception as e:
            print(f"Error en obtener_alumnos_presentes: {e}")
        return []

    def obtener_alumnos_ausentes(self):
        try:
            if hasattr(self.user_model, "consultar_ausentes_hoy"):
                return self.user_model.consultar_ausentes_hoy()
            return [
                {"matricula": "2026089", "nombre": "Diana Laura Martínez"},
                {"matricula": "2026112", "nombre": "Jorge Alberto Ríos"},
            ]
        except Exception as e:
            print(f"Error en obtener_alumnos_ausentes: {e}")
            return []
    # --- MÉTODOS PARA GESTIÓN DE SESIÓN Y GRUPOS ---

    def set_usuario_actual(self, id_usuario):
        """Guarda el ID del maestro que acaba de iniciar sesión."""
        self.usuario_actual_id = id_usuario

    def get_usuario_actual_id(self):
        """Retorna el ID del maestro actual."""
        return self.usuario_actual_id

    def obtener_grupos_de_maestro(self, id_maestro):
        """Consulta la base de datos para traer solo los grupos de este maestro."""
        # Asegúrate de que tu UsuarioModel tenga acceso a la DB o haz la consulta aquí directamente
        # Ejemplo usando self.user_model (ajusta según tu estructura real)
        conn = self.user_model.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        query = "SELECT nombre_grupo FROM maestro_grupo WHERE id_maestro = %s"
        cursor.execute(query, (id_maestro,))
        resultados = cursor.fetchall()
        cursor.close()
        conn.close()
        return [r['nombre_grupo'] for r in resultados]

    def guardar_nuevo_grupo(self, id_maestro, nombre_grupo):
        """Guarda un nuevo grupo asociado al maestro en la base de datos."""
        conn = self.user_model.db.get_connection()
        cursor = conn.cursor()
        try:
            query = "INSERT INTO maestro_grupo (id_maestro, nombre_grupo) VALUES (%s, %s)"
            cursor.execute(query, (id_maestro, nombre_grupo))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al guardar grupo: {e}")
            return False
        finally:
            cursor.close(); conn.close()

    def eliminar_asignacion_grupo(self, id_maestro, nombre_grupo):
        """Elimina la relación grupo-maestro de la base de datos."""
        conn = self.user_model.db.get_connection()
        cursor = conn.cursor()
        try:
            query = "DELETE FROM maestro_grupo WHERE id_maestro = %s AND nombre_grupo = %s"
            cursor.execute(query, (id_maestro, nombre_grupo))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar grupo: {e}")
            return False
        finally:
            cursor.close(); conn.close()