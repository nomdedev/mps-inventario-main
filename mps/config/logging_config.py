import logging

# Configurar logging
logging.basicConfig(
    filename="app.log",  # Archivo donde se guardarán los logs
    level=logging.INFO,  # Nivel de registro
    format="%(asctime)s - %(levelname)s - %(message)s",  # Formato del log
)

def get_logger(name):
    return logging.getLogger(name)
