import json
import sys
import pyodbc
from PyQt5.QtWidgets import QApplication
from ui.configuracion_bd_widget import ConfiguracionBDWidget

CONFIG_PATH = './config/databaseConfig.json'

def load_config():
    try:
        with open(CONFIG_PATH, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        return None

def test_connections(config):
    for db_name in config["databases"].values():
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={config['server']},{config['port']};"
            f"DATABASE={db_name};"
            f"UID={config['user']};"
            f"PWD={config['password']}"
        )
        conn = pyodbc.connect(connection_string)
        conn.close()

def main():
    app = QApplication(sys.argv)
    config = load_config()

    if not config:
        widget = ConfiguracionBDWidget(CONFIG_PATH)
        widget.show()
        sys.exit(app.exec_())

    try:
        test_connections(config)
        print("Conexión exitosa a todas las bases de datos.")
    except Exception as e:
        print(f"Error al conectar: {e}")
        widget = ConfiguracionBDWidget(CONFIG_PATH)
        widget.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()
