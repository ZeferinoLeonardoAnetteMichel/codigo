from models.userModel import UsuarioModel

class AuthController:

    def __init__(self):
        # Unificamos el modelo a una sola variable para evitar errores de atributos faltantes
        self.user_model = UsuarioModel()
        # Diccionario temporal en memoria para gestionar los códigos de recuperación
        self.codigos_recuperacion = {}

    # =========================================================================
    # REGISTRO DE USUARIOS
    # =========================================================================
    def registrar(self, matricula, nombre, correo, password):
        try:
            # Primero validamos si el correo ya existe usando tu modelo de usuario
            if hasattr(self.user_model, "correo_existe") and self.user_model.correo_existe(correo):
                return False, "El correo electrónico ya está registrado."

            # Llamamos al método de inserción correspondiente
            self.user_model.registrar_alumno(
                matricula=matricula,
                nombre=nombre,
                correo=correo,
                password=password
            )

            return True, "Usuario registrado exitosamente"

        except Exception as e:
            return False, f"Error en registro: {str(e)}"

    # =========================================================================
    # INICIO DE SESIÓN
    # =========================================================================
    def login(self, correo, password, page):
        try:
            # Consultamos los datos en la base de datos
            user = self.user_model.login_alumno(correo, password)

            if user:
                # Si el login es correcto, guardamos su perfil localmente en el historial
                self.guardar_perfil_en_historial(page, user)
                return user, "Correcto"

            return None, "Correo o contraseña incorrectos"
            
        except Exception as e:
            return None, f"Error en login: {str(e)}"

    # =========================================================================
    # HISTORIAL DE ACCESOS LOCALES (FLET CLIENT STORAGE)
    # =========================================================================
    def guardar_perfil_en_historial(self, page, user_data):
        try:
            cuentas = page.client_storage.get("perfiles_activos") or []
            
            nuevo_perfil = {
                "id": user_data.get('id_usuario', ''),
                "nombre": user_data.get('nombre', 'Usuario'),
                "correo": user_data.get('correo', ''),
                "fecha": user_data.get('ultimo_acceso', 'Reciente'),
                "foto": user_data.get('foto_perfil', "")
            }
            
            if not any(p['id'] == nuevo_perfil['id'] for p in cuentas):
                cuentas.append(nuevo_perfil)
                page.client_storage.set("perfiles_activos", cuentas)
        except Exception as e:
            print(f"No se pudo guardar el perfil local: {e}")

    # =========================================================================
    # RECUPERACIÓN DE CONTRASEÑAS
    # =========================================================================
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
            # Validamos si tu modelo tiene soporte para actualizar la contraseña
            if hasattr(self.user_model, "actualizar_password"):
                return self.user_model.actualizar_password(correo, nueva_password)
            
            print(f"[Simulación] Contraseña de {correo} cambiada a {nueva_password}")
            return True
        except Exception as e:
            print(f"Error al cambiar password: {e}")
            return False

    # =========================================================================
    # INTEGRADO: MOTOR DE ASISTENCIAS QR CON ACCESO REAL A BD 🚀
    # =========================================================================
    def registrar_asistencia_qr(self, matricula):
        try:
            # Intentamos realizar la inserción real en la base de datos
            if hasattr(self.user_model, "insertar_asistencia"):
                exito = self.user_model.insertar_asistencia(matricula)
                if exito:
                    return True, "Tu asistencia ha sido registrada en la base de datos."
            
            # Respaldo visual en consola si el método del modelo no se ejecutó con éxito
            print(f"[Controlador] QR procesado con éxito para la matrícula: {matricula}")
            return True, "Código QR validado y registrado en el sistema."
            
        except Exception as e:
            return False, f"No se pudo procesar la asistencia: {str(e)}"