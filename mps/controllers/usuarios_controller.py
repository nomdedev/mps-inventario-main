# Controlador para manejar la lógica de usuarios.
from mps.database_utils import connect_database

class UsuariosController:
    _conexion_servidor = None

    def __init__(self):
        self.conexion_db = None
        self.connection = None  # Inicializa el atributo connection

    @classmethod
    def conectar_servidor(cls):
        if cls._conexion_servidor is None:
            # Establecer conexión al servidor (simulado)
            cls._conexion_servidor = "Conexión al servidor establecida"
            print("Conexión al servidor creada.")
        else:
            print("Reutilizando conexión al servidor.")

    def conectar_base_datos(self, nombre_db):
        if self._conexion_servidor is None:
            raise RuntimeError("Error: Primero debe conectarse al servidor llamando a 'conectar_servidor'.")
        try:
            # Simula la conexión a la base de datos
            print(f"Intentando conectar a la base de datos: {nombre_db}")
            self.connection = connect_database(nombre_db)  # Asigna la conexión a self.connection
            if self.connection is None:
                raise RuntimeError(f"Error: No se pudo establecer la conexión con la base de datos {nombre_db}.")
            self.conexion_db = f"Conectado a la base de datos {nombre_db}"
            print(f"Conexión establecida con la base de datos: {nombre_db}")
            # Verifica si las tablas están disponibles
            cursor = self.connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            print("Tablas disponibles en la base de datos:", tables)
        except Exception as e:
            raise RuntimeError(f"Error al conectar a la base de datos {nombre_db}: {e}")

    def listar_usuarios(self):
        try:
            if self.connection is None:
                raise RuntimeError("Error: La conexión a la base de datos no está inicializada.")
            print("Ejecutando consulta para listar usuarios.")
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM usuarios")
            result = cursor.fetchall()
            print(f"Usuarios encontrados: {result}")
            return result
        except Exception as e:
            raise RuntimeError(f"Error al listar los usuarios: {e}")

    def agregar_usuario(self, username, role):
        try:
            if self.connection is None:
                raise RuntimeError("Error: La conexión a la base de datos no está inicializada.")
            print(f"Agregando usuario: {username} con rol: {role}")
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO usuarios (username, role) VALUES (?, ?)",
                (username, role)
            )
            self.connection.commit()
            print("Usuario agregado exitosamente.")
        except Exception as e:
            raise RuntimeError(f"Error al agregar el usuario: {e}")

    def verificar_credenciales(self, username, password):
        if self.conexion_db != "Conectado a la base de datos usuarios":
            self.conectar_base_datos("usuarios")
        try:
            if self.connection is None:
                raise RuntimeError("Error: La conexión a la base de datos no está inicializada.")
            print(f"Ejecutando consulta para verificar credenciales del usuario: {username}")
            cursor = self.connection.cursor()
            cursor.execute(
                "SELECT id, username, role FROM usuarios WHERE username = ? AND password = ?",
                (username, password)
            )
            result = cursor.fetchone()
            print(f"Resultado de la consulta: {result}")
            return result  # Devuelve el usuario si las credenciales son correctas
        except Exception as e:
            raise RuntimeError(f"Error al verificar las credenciales: {e}")