from models.databaseModel import Database
import bcrypt

class UsuarioModel:

    def __init__(self):
        self.db = Database()

    # REGISTRAR
    def registrar_alumno(
        self,
        matricula,
        nombre,
        correo,
        password
    ):

        conn = self.db.get_connection()
        cursor = conn.cursor()

        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        )

        query = """
        INSERT INTO alumnos
        (
            matricula,
            nombre,
            correo,
            password
        )
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(
            query,
            (
                matricula,
                nombre,
                correo,
                password_hash
            )
        )

        conn.commit()

        cursor.close()
        conn.close()

    # LOGIN
    def login_alumno(self, correo, password):

        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT *
        FROM alumnos
        WHERE correo = %s
        """

        cursor.execute(query, (correo,))

        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user:

            password_correcta = bcrypt.checkpw(
                password.encode("utf-8"),
                user["password"].encode("utf-8")
            )

            if password_correcta:
                return user

        return None