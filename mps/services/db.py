import pyodbc
from mps.ui.configurar_conexion_dialog import ConfigurarConexionDialog
from mps.utils.logger import get_logger

logger = get_logger(__name__)

class DBConnection:
    def __init__(self):
        """
        Inicializa la conexión a la base de datos remota.
        """
        self.server = "tcp:127.0.0.1"  # Cambiado a tcp:127.0.0.1 para evitar resolución de nombre
        self.port = "1433"             # Se agregó el puerto explícito
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
                f"SERVER={self.server},{self.port};"  # Incluye el puerto explícitamente
                f"DATABASE={base};"
                f"UID={self.user};"
                f"PWD={self.password};"
            )
            self.connection = pyodbc.connect(self.connection_string)
            logger.info(f"Conexión a la base de datos '{base}' establecida.")
        except pyodbc.Error as e:
            logger.critical(f"Error al conectar a la base de datos '{base}': {e}")
            self.mostrar_error_conexion(e)

    def mostrar_error_conexion(self, error):
        """
        Muestra un mensaje de error al usuario y abre la pantalla de configuración.
        """
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.critical(None, "Error de Conexión", f"No se pudo conectar a la base de datos: {error}")
        logger.error("Abriendo la pantalla de configuración del servidor.")
        dialog = ConfigurarConexionDialog()
        dialog.exec()

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
