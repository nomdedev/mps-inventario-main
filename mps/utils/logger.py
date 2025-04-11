import logging
import os
from datetime import datetime

def configurar_logger():
    """
    Configura el logger para la aplicación.
    Crea la carpeta 'logs/' si no existe y asegura que el archivo 'logger.log' sea accesible.
    """
    try:
        # Crear carpeta 'logs/' si no existe
        logs_folder = "logs"
        if not os.path.exists(logs_folder):
            os.makedirs(logs_folder)

        # Configurar archivo de log
        log_file = os.path.join(logs_folder, "logger.log")
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[
                logging.FileHandler(log_file, mode="a", encoding="utf-8"),
                logging.StreamHandler()
            ]
        )
        logging.info("Logger configurado correctamente.")
    except Exception as e:
        print(f"Error al configurar el logger: {e}")
        import traceback
        traceback.print_exc()

# Llamar a la configuración del logger al importar el módulo
configurar_logger()

def get_logger(name):
    """
    Retorna un logger con el nombre especificado.
    :param name: Nombre del logger.
    :return: Instancia del logger.
    """
    return logging.getLogger(name)
