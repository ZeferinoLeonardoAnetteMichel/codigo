import smtplib
import random
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

from models.userModel import UsuarioModel
class AuthController:
    
    def __init__(self):
        self.usuario_model = UsuarioModel()
        self.codigos_recuperacion = {}
    def enviar_correo_recuperacion(self, correo):
        try:
            print("INICIANDO ENVIO")
            load_dotenv(override=True)
            codigo = str(random.randint(100000, 999999))
            print("CODIGO GENERADO:", codigo)
            self.codigos_recuperacion[correo] = codigo
            remitente = os.getenv("EMAIL_USER")
            password = os.getenv("EMAIL_PASS")
            print("REMITENTE DETECTADO:", remitente)
            if password:
                print("LONGITUD CONTRASEÑA EN MEMORIA:", len(password.strip()))
            if not remitente or not password:
                return False, "Faltan variables del archivo .env"
            mensaje = MIMEText(
                f"""
Hola.
Tu código de recuperación es:
{codigo}
Este código vence en 5 minutos.
"""
            )
            mensaje["Subject"] = "Recuperación de contraseña"
            mensaje["From"] = remitente
            mensaje["To"] = correo
            servidor = smtplib.SMTP("smtp.gmail.com", 587)
            servidor.starttls()
            servidor.login(remitente.strip(), password.strip())
            servidor.sendmail(remitente.strip(), correo, mensaje.as_string())
            servidor.quit()
            print("CORREO ENVIADO CON ÉXITO")
            return True, "Código enviado correctamente"
        except Exception as e:
            print("ERROR SMTP DETECTADO:", e)
            return False, f"Error enviando correo: {e}"
    def login(self, email, password, page):

        try:
            user_db = self.usuario_model.validar_login(
                email,
                password
            )
            if not user_db:
                return None, "Correo o contraseña incorrectos"
            user = {
                "id_usuario": user_db["id_usuario"],
                "nombre": user_db["nombre"],
                "apellido": user_db["apellido"],
                "email": user_db["email"],
                "ultimo_acceso": user_db.get(
                    "ultimo_acceso",
                    "Reciente"
                ),
            }
            self.guardar_perfil_en_historial(page,user)
            return user, "Login exitoso"
        except Exception as e:
            return None, f"Error en login: {str(e)}"
    def guardar_perfil_en_historial(self,page,user_data):
        try:
            cuentas = page.client_storage.get(
                "perfiles_activos"
            ) or []
            nuevo_perfil = {
                "id": user_data['id_usuario'],
                "nombre": user_data['nombre'],
                "correo": user_data['correo'],
                "fecha": user_data['ultimo_acceso'],
                "foto": user_data.get(
                    'foto_perfil',
                    ""
                )
            }
            if not any(
                p['id'] == nuevo_perfil['id']
                for p in cuentas
            ):
                cuentas.append(nuevo_perfil)
                page.client_storage.set("perfiles_activos",cuentas)
        except Exception as e:
            print(f"No se pudo guardar el perfil local: {e}")
    def registrar(self, usuario_data):
        try:
            if self.usuario_model.correo_existe(
                usuario_data.correo
            ):
                return False, (
                    "El correo electrónico "
                    "ya está registrado"
                )
            exito = self.usuario_model.registrar(
                usuario_data
            )
            if exito:
                return (True,"Usuario registrado exitosamente")
            else:
                return (False,"Error al registrar usuario")
        except Exception as e:
            return (False,f"Error en registro: {str(e)}")
    def verificar_codigo_recuperacion(self,correo,codigo_ingresado):
        try:
            codigo_guardado = self.codigos_recuperacion.get(correo)
            if not codigo_guardado:
                return (False, "No se ha solicitado un código "
                    "para este correo o ya venció.")
            if codigo_guardado == codigo_ingresado.strip():
                del self.codigos_recuperacion[correo]
                return (True,"Código verificado con éxito.")
            else:
                return (False,"El código introducido es incorrecto.")
        except Exception as e:
            return (
                False,
                f"Error al verificar código: {str(e)}"
            )
    def cambiar_password(
        self,
        correo,
        nueva_password
    ):
        try:
            return self.usuario_model.actualizar_password(
                correo,
                nueva_password
            )
        except Exception as e:
            print("ERROR CAMBIANDO PASSWORD:",e)
            return False
def login_exitoso(page, user_data):
    page.user_data = user_data
    page.go("/dashboard")
