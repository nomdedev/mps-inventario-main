import pyodbc
from mps.config.db_config import DB_CONFIG

def connect_database(nombre_db):
    if nombre_db not in DB_CONFIG:
        raise ValueError(f"No se encontró la configuración para la base de datos '{nombre_db}'.")
    config = DB_CONFIG[nombre_db]
    conn_str = (
        f"DRIVER={config['driver']};"
        f"SERVER={config['server']};"
        f"DATABASE={config['database']};"
        f"UID={config['uid']};"
        f"PWD={config['pwd']};"
    )
    try:
        print(f"Intentando conectar a la base de datos SQL Express: {nombre_db}")
        connection = pyodbc.connect(conn_str)
        print(f"Conexión exitosa a la base de datos: {nombre_db}")
        return connection
    except Exception as e:
        # Si el error indica que la base de datos no existe o no se puede acceder, mostrar un mensaje específico
        if "4060" in str(e):
            raise RuntimeError(f"Error al conectar a la base de datos {nombre_db}: La base de datos '{nombre_db}' no existe o el usuario no tiene permisos para acceder.")
        if "18456" in str(e):
            raise RuntimeError(f"Error al conectar al servidor SQL: El usuario '{config['uid']}' no tiene permisos de inicio de sesión.")
        print(f"Error al intentar conectar a la base de datos SQL Express: {nombre_db}")
        raise RuntimeError(f"Error al conectar a la base de datos {nombre_db}: {e}")