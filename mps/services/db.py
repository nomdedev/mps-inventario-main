import pyodbc
from mps.utils.logger import get_logger

logger = get_logger(__name__)

class DBConnection:
    def __init__(self):
        """
        Inicializa la conexión a la base de datos remota.
        """
        self.server = "192.168.1.10\\SQLEXPRESS"
        self.user = "sa"
        self.password = "mps.1887"
        self.driver = "ODBC Driver 17 for SQL Server"
        self.connection = None
        logger.info("Inicializando conexión a la base de datos.")

    def conectar(self, base: str = "inventario"):
        """
        Establece la conexión a la base de datos indicada.
        :param base: Nombre de la base de datos a conectar (por defecto 'inventario').
        """
        try:
            self.connection_string = (
                f"DRIVER={{{self.driver}}};"
                f"SERVER={self.server};"
                f"DATABASE={base};"
                f"UID={self.user};"
                f"PWD={self.password};"
            )
            self.connection = pyodbc.connect(self.connection_string)
            logger.info(f"Conexión a la base de datos '{base}' establecida.")
        except pyodbc.Error as e:
            logger.error(f"Error al conectar a la base de datos '{base}': {e}")
            raise RuntimeError(f"Error al conectar a la base de datos '{base}': {e}")

    def ejecutar_query(self, query: str, params: list = []):
        """
        Ejecuta una consulta SELECT en la base de datos.
        :param query: Consulta SQL.
        :param params: Parámetros para la consulta.
        :return: Resultados de la consulta.
        """
        try:
            if self.connection is None:
                raise RuntimeError("La conexión a la base de datos no está inicializada.")
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
        except pyodbc.Error as e:
            logger.error(f"Error al ejecutar la consulta: {e}")
            raise RuntimeError(f"Error al ejecutar la consulta: {e}")

    def ejecutar_insert(self, query: str, params: list = []):
        """
        Ejecuta una consulta INSERT/UPDATE/DELETE en la base de datos.
        :param query: Consulta SQL.
        :param params: Parámetros para la consulta.
        """
        try:
            if self.connection is None:
                raise RuntimeError("La conexión a la base de datos no está inicializada.")
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            logger.info("Consulta ejecutada y cambios guardados.")
        except pyodbc.Error as e:
            logger.error(f"Error al ejecutar la consulta: {e}")
            raise RuntimeError(f"Error al ejecutar la consulta: {e}")

    def cerrar(self):
        """
        Cierra la conexión a la base de datos.
        """
        try:
            if self.connection:
                self.connection.close()
                logger.info("Conexión a la base de datos cerrada.")
        except pyodbc.Error as e:
            logger.error(f"Error al cerrar la conexión: {e}")
            raise RuntimeError(f"Error al cerrar la conexión: {e}")
