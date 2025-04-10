import pyodbc

class DatabaseManager:
    def __init__(self, server, database, username, password):
        self.connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server};"
            f"DATABASE={database};"
            f"UID={username};"
            f"PWD={password};"
        )
        self.connection = None

    def connect(self):
        try:
            self.connection = pyodbc.connect(self.connection_string)
            print("Conexión exitosa al servidor SQL.")
        except pyodbc.Error as e:
            print(f"Error al conectar con la base de datos: {e}")
            raise

    def list_tables(self):
        if not self.connection:
            raise ConnectionError("No hay conexión activa con la base de datos.")
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE';"
        )
        tables = [row.TABLE_NAME for row in cursor.fetchall()]
        return tables

    def execute_query(self, query):
        if not self.connection:
            raise ConnectionError("No hay conexión activa con la base de datos.")
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    def close(self):
        if self.connection:
            self.connection.close()
            print("Conexión cerrada.")
