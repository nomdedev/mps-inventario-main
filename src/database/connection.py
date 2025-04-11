import configparser
import pyodbc

# Lee la configuración desde el archivo INI
config = configparser.ConfigParser()
config.read('./config/databaseConfig.ini')

db_config = config['database']

# Configuración de la conexión
connection_string = (
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={db_config['server']};"
    f"DATABASE={db_config['database']};"
    f"UID={db_config['user']};"
    f"PWD={db_config['password']};"
    f"PORT={db_config['port']}"
)

def connect_to_database():
    try:
        conn = pyodbc.connect(connection_string)
        print("Conexión exitosa a la base de datos")
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        raise
