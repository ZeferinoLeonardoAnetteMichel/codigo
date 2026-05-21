import bcrypt
from .databaseModel import Database
class UsuarioModel:
    
    def __init__(self):
        self.db = Database()
        
    def correo_existe(self, correo):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id_usuario FROM usuario WHERE correo = %s",(correo,))
        existe = cursor.fetchone() is not None
        conn.close()
        return existe
    def registrar(self, usuario_data):
        salt = bcrypt.gensalt()
        hashed_pw = bcrypt.hashpw(
            usuario_data.password.encode("utf-8"),
            salt
        )
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""INSERT INTO usuario (nombre,apellido,correo,password,fecha_registro) VALUES ( %s,%s,%s,%s,NOW())""",
                (
                    usuario_data.nombre,
                    usuario_data.apellido,
                    usuario_data.correo,
                    hashed_pw.decode("utf-8")
                )
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error en registro: {e}")
            return False
        finally:
            conn.close()
    def validar_login(self, correo, password):
        conn = self.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM usuario WHERE correo = %s",
            (correo,)
        )
        user = cursor.fetchone()
        conn.close()
        if user and bcrypt.checkpw(
            password.encode("utf-8"),
            user["password"].encode("utf-8")
        ):
            return user
        return None
    def actualizar_password(
        self,
        correo,
        nueva_password
    ):
        try:
            salt = bcrypt.gensalt()
            hashed_pw = bcrypt.hashpw(
                nueva_password.encode("utf-8"),
                salt
            )
            conn = self.db.get_connection()
            cursor = conn.cursor()
            sql = """UPDATE usuario SET password = %s WHERE correo = %s"""
            cursor.execute(
                sql,
                (hashed_pw.decode("utf-8"),correo)
            )
            conn.commit()
            return cursor.rowcount > 0
        except Exception as e:
            print("ERROR ACTUALIZANDO PASSWORD:",e)
            return False
        finally:
            conn.close()