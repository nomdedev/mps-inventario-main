import pyodbc
import os

class DatabaseSetup:
    def __init__(self, config):
        self.config = config
        self.connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={config['server']},{config['port']};"
            f"UID={config['user']};"
            f"PWD={config['password']};"
            f"Encrypt={config.get('encryption', 'Optional')};"
            f"TrustServerCertificate={config.get('trust_cert', 'True')}"
        )

    def connect(self):
        try:
            return pyodbc.connect(self.connection_string)
        except Exception as e:
            raise Exception(f"Error al conectar a la base de datos: {e}")

    def database_exists(self, conn, database_name):
        query = f"SELECT database_id FROM sys.databases WHERE name = '{database_name}'"
        cursor = conn.cursor()
        cursor.execute(query)
        return cursor.fetchone() is not None

    def create_database(self, conn, database_name):
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE {database_name}")
        conn.commit()

    def execute_sql_file(self, conn, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"El archivo {file_path} no existe.")
        with open(file_path, 'r', encoding='utf-8') as sql_file:
            sql_script = sql_file.read()
        cursor = conn.cursor()
        cursor.execute(sql_script)
        conn.commit()

    def validate_table_data(self, conn, table_name, expected_count):
        query = f"SELECT COUNT(*) FROM {table_name}"
        cursor = conn.cursor()
        cursor.execute(query)
        count = cursor.fetchone()[0]
        return count == expected_count

    def setup(self):
        try:
            conn = self.connect()

            # Verificar y crear base de datos 'inventario'
            if not self.database_exists(conn, 'inventario'):
                print("La base de datos 'inventario' no existe. Creándola...")
                self.create_database(conn, 'inventario')

            # Usar la base de datos 'inventario'
            conn.cursor().execute("USE inventario")

            # Validar y cargar datos en 'perfiles_pvc'
            if not self.validate_table_data(conn, 'perfiles_pvc', 2549):
                print("Cargando datos en la tabla 'perfiles_pvc'...")
                self.execute_sql_file(conn, './data/inventario_completo_batch.sql')

            # Validar y cargar datos en 'herrajes'
            if not self.validate_table_data(conn, 'herrajes', 0):  # Cambiar 0 por el número esperado si se conoce
                print("Cargando datos en la tabla 'herrajes'...")
                self.execute_sql_file(conn, './data/herrajes_roto_2025.sql')

            print("Configuración de la base de datos completada.")
        except Exception as e:
            print(f"Error durante la configuración de la base de datos: {e}")
