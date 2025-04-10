import logging
import os
from datetime import datetime

# Clase para manejar el registro de logs en la aplicación.
# Incluirá métodos para registrar información, advertencias y errores.

class Logger:
    LOG_DIR = "logs"

    @staticmethod
    def _get_logger():
        """
        Configura y devuelve un logger con un archivo de log diario.
        """
        if not os.path.exists(Logger.LOG_DIR):
            os.makedirs(Logger.LOG_DIR)

        log_filename = os.path.join(Logger.LOG_DIR, f"{datetime.now().strftime('%Y-%m-%d')}.log")
        logger = logging.getLogger("MPSLogger")

        if not logger.hasHandlers():
            logger.setLevel(logging.DEBUG)
            file_handler = logging.FileHandler(log_filename)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger

    @staticmethod
    def log_info(mensaje):
        """
        Registra un mensaje informativo.
        :param mensaje: Mensaje a registrar.
        """
        logger = Logger._get_logger()
        logger.info(mensaje)

    @staticmethod
    def log_error(error):
        """
        Registra un mensaje de error.
        :param error: Error a registrar.
        """
        logger = Logger._get_logger()
        logger.error(error)

    @staticmethod
    def log_evento(tipo, mensaje):
        """
        Registra un evento importante.
        :param tipo: Tipo de evento (ej. "LOGIN", "AUDITORÍA").
        :param mensaje: Mensaje del evento.
        """
        logger = Logger._get_logger()
        logger.info(f"[{tipo}] {mensaje}")
