# Modelo de datos para representar un usuario.
# Incluirá atributos como id, nombre, rol y métodos relacionados.

class Usuario:
    def __init__(self, id, nombre, apellido, usuario, contraseña, rol, activo):
        """
        Modelo de datos para un usuario.
        :param id: ID del usuario.
        :param nombre: Nombre del usuario.
        :param apellido: Apellido del usuario.
        :param usuario: Nombre de usuario.
        :param contraseña: Contraseña del usuario.
        :param rol: Rol del usuario (ej. admin, supervisor, operador).
        :param activo: Estado del usuario (True si está activo, False si no).
        """
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.usuario = usuario
        self.contraseña = contraseña
        self.rol = rol
        self.activo = activo

    @staticmethod
    def desde_row(row):
        """
        Crea un objeto Usuario a partir de una fila de base de datos.
        :param row: Fila de la base de datos (tupla o lista).
        :return: Objeto Usuario.
        """
        return Usuario(
            id=row[0],
            nombre=row[1],
            apellido=row[2],
            usuario=row[3],
            contraseña=row[4],
            rol=row[5],
            activo=row[6]
        )
