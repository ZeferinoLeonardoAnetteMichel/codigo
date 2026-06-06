from models.userModel import UsuarioModel
class AuthController:

    def __init__(self):
        self.user_model = UsuarioModel()
        self.codigos_recuperacion = {}

    def registrar(self, matricula, nombre, apellido_paterno, apellido_materno, grado, grupo, correo, password):
        try:
            if hasattr(self.user_model, "correo_existe") and self.user_model.correo_existe(correo):
                return False, "El correo electrónico ya está registrado."
            self.user_model.registrar_alumno(
                matricula=matricula,
                nombre=nombre,
                correo=correo,
                password=password,
                grupo=grupo,
                grado=grado,
                apellido_paterno=apellido_paterno,
                apellido_materno=apellido_materno
            )
            return True, "Usuario registrado exitosamente"
        except Exception as e:
            return False, f"Error en registro: {str(e)}"

    def login(self, correo, password, page):
        try:
            user = self.user_model.login_alumno(correo, password)
            if user:
                return user, "Correcto"
            return None, "Correo o contraseña incorrectos"
        except Exception as e:
            return None, f"Error en login: {str(e)}"

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

    def registrar_asistencia_qr(self, matricula):
        try:
            ya_asistio = self.user_model.verificar_asistencia_existente(matricula)
            if ya_asistio:
                return False, "Ya registraste tu asistencia el día de hoy."
            exito = self.user_model.insertar_asistencia(matricula)            
            if exito:
                return True, "Asistencia registrada con éxito."
            else:
                return False, "Error al guardar en la base de datos."
        except Exception as e:
            print(f"Error en controlador de asistencia: {e}")
            return False, "Error interno del sistema."
        
    def obtener_qr_activo(self):
        return self.user_model.obtener_qr_activo()

    def obtener_alumnos_presentes(self, nombre_grupo):
        try:
            if hasattr(self.user_model, "consultar_presentes_hoy"):
                datos = self.user_model.consultar_presentes_hoy(nombre_grupo)                
                print(f"DEBUG: Datos recibidos del modelo para grupo {nombre_grupo}:")
                if datos:
                    print(f"Tipo de dato: {type(datos)}")
                    print(f"Contenido del primer registro: {datos[0]}")
                    print(f"Claves disponibles: {datos[0].keys() if isinstance(datos[0], dict) else 'No es un diccionario'}")
                else:
                    print("DEBUG: El modelo devolvió una lista vacía.")                
                return datos
            return []
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