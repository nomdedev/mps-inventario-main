# Clase para manejar la sesión del usuario actualmente logueado.
# Incluirá métodos para iniciar sesión, cerrar sesión y verificar permisos.

class Session:
    usuario_actual = None
    rol = None

    @classmethod
    def set_usuario(cls, usuario):
        """
        Establece el usuario actualmente logueado.
        :param usuario: Objeto Usuario o diccionario con información del usuario.
        """
        cls.usuario_actual = usuario
        cls.rol = usuario.rol if hasattr(usuario, 'rol') else usuario.get("role")
        print(f"Sesión iniciada para el usuario: {cls.usuario_actual.nombre if hasattr(usuario, 'nombre') else usuario.get('username')}")

    @classmethod
    def get_usuario_actual(cls):
        """
        Obtiene el usuario actualmente logueado.
        :return: Objeto Usuario o diccionario con información del usuario.
        """
        return cls.usuario_actual

    @classmethod
    def es_admin(cls):
        """
        Verifica si el usuario actual tiene rol de administrador.
        :return: True si el usuario es administrador, False en caso contrario.
        """
        return cls.rol == "Administrador"

    @classmethod
    def es_operador(cls):
        """
        Verifica si el usuario actual tiene rol de operador.
        :return: True si el usuario es operador, False en caso contrario.
        """
        return cls.rol == "Operador"

    @classmethod
    def cerrar_sesion(cls):
        """
        Cierra la sesión actual.
        """
        print(f"Sesión cerrada para el usuario: {cls.usuario_actual.nombre if cls.usuario_actual else 'Ninguno'}")
        cls.usuario_actual = None
        cls.rol = None

    @staticmethod
    def tiene_permiso(usuario, accion):
        """
        Verifica si el usuario tiene permiso para realizar una acción específica según su rol.
        :param usuario: Objeto Usuario o diccionario con información del usuario.
        :param accion: Acción a validar.
        :return: True si tiene permiso, False en caso contrario.
        """
        permisos_por_rol = {
            "admin": ["crear", "editar", "eliminar", "aprobar", "denegar", "ver"],
            "supervisor": ["crear", "editar", "ver"],
            "operador": ["ver"]
        }

        rol = usuario.rol if hasattr(usuario, 'rol') else usuario.get("role")
        acciones_permitidas = permisos_por_rol.get(rol, [])
        return accion in acciones_permitidas
