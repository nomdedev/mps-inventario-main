# Controlador para manejar la autenticación de usuarios.
# Incluirá métodos para verificar credenciales y manejar permisos.

from mps.services.db import DBConnection
from mps.services.session import Session
from mps.models.usuario import Usuario

class AuthController:
    @staticmethod
    def login(usuario, contraseña):
        """
        Valida las credenciales del usuario contra la base de datos.
        :param usuario: Nombre de usuario.
        :param contraseña: Contraseña del usuario.
        :return: Objeto Usuario si las credenciales son válidas, None si no lo son.
        """
        db = DBConnection()
        try:
            db.conectar(base="users")
            query = """
                SELECT id, nombre, apellido, usuario, contraseña, rol, activo
                FROM Usuarios
                WHERE usuario = ? AND contraseña = ? AND activo = 1
            """
            resultado = db.ejecutar_query(query, [usuario, contraseña])

            if resultado:
                usuario_obj = Usuario.desde_row(resultado[0])
                Session.set_usuario(usuario_obj)
                return usuario_obj
            else:
                return None
        except Exception as e:
            raise RuntimeError(f"Error al intentar iniciar sesión: {e}")
        finally:
            db.cerrar()

    def verificar_credenciales(self, usuario, contraseña):
        """
        Verifica las credenciales del usuario contra la base de datos.
        :param usuario: Nombre de usuario.
        :param contraseña: Contraseña del usuario.
        :return: Objeto Usuario si las credenciales son válidas, None si no lo son.
        """
        db = DBConnection()
        try:
            db.conectar(base="users")
            query = """
                SELECT id, nombre, apellido, usuario, contraseña, rol, activo
                FROM Usuarios
                WHERE usuario = ? AND contraseña = ? AND activo = 1
            """
            resultado = db.ejecutar_query(query, [usuario, contraseña])
            if resultado:
                return Usuario.desde_row(resultado[0])
            return None
        finally:
            db.cerrar()
