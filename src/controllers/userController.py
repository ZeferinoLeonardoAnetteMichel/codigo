from models.userModel import UsuarioModel

class AuthController:

    def __init__(self):
        self.user_model = UsuarioModel()

    def registrar(
        self,
        matricula,
        nombre,
        correo,
        password
    ):

        try:

            self.user_model.registrar_alumno(
                matricula,
                nombre,
                correo,
                password
            )

            return True, "Usuario registrado"

        except Exception as e:

            return False, str(e)

    def login(
        self,
        correo,
        password,
        page
    ):

        user = self.user_model.login_alumno(
            correo,
            password
        )

        if user:
            return user, "Correcto"

        return None, "Correo o contraseña incorrectos"