import sys
import json
import os
import logging
import pyodbc
from PyQt6.QtWidgets import QApplication, QMessageBox, QDialog
from PyQt6.QtCore import QFile, QTextStream
from mps.ui.login_window import LoginWindow
from mps.ui.main_window import MainWindow
from mps.config.design_config import DESIGN_CONFIG
from mps.ui.configurar_conexion_dialog import ConfigurarConexionDialog
from mps.controllers.database_setup import DatabaseSetup
from mps.config.logging_config import get_logger

CONFIG_PATH = './config/databaseConfig.json'

# Configurar logging
logger = get_logger(__name__)

def handle_exception(exc_type, exc_value, exc_traceback):
    """Manejador global de excepciones."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.error("Excepción no manejada", exc_info=(exc_type, exc_value, exc_traceback))
    QMessageBox.critical(None, "Error crítico", f"Ocurrió un error inesperado: {exc_value}")

# Configurar el manejador global de excepciones
sys.excepthook = handle_exception

def load_stylesheet(app):
    """
    Carga la hoja de estilo global desde el archivo style.qss.
    """
    try:
        file = QFile("mps/assets/styles/style.qss")
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            stylesheet = stream.readAll()
            app.setStyleSheet(stylesheet)
            print("Hoja de estilo cargada correctamente.")
        else:
            print("Advertencia: No se pudo abrir el archivo style.qss.")
    except Exception as e:
        print(f"Error al cargar el archivo de estilos: {e}")

def load_config():
    """
    Carga la configuración de conexión SQL desde el archivo JSON.
    """
    try:
        with open(CONFIG_PATH, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print("Archivo de configuración no encontrado. Usando valores predeterminados.")
        return {"server": "", "port": 1433, "user": "", "password": ""}

def main():
    app = QApplication(sys.argv)

    # Mostrar la ventana de inicio de sesión primero
    login_window = LoginWindow()
    login_window.show()

    # Si se necesita configurar el servidor, se puede invocar manualmente
    # configurar_conexion_dialog = ConfigurarConexionDialog()
    # configurar_conexion_dialog.exec()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
