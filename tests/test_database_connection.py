import unittest
from mps.database_utils import connect_database

class TestDatabaseConnection(unittest.TestCase):
    def setUp(self):
        try:
            self.connection = connect_database()
            print("Conexión establecida exitosamente.")
        except Exception as e:
            self.fail(f"Error al conectar con la base de datos: {e}")

    def tearDown(self):
        if self.connection:
            self.connection.close()
            print("Conexión cerrada.")

    def test_list_tables(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_TYPE = 'BASE TABLE'
            """)
            tables = cursor.fetchall()
            self.assertGreater(len(tables), 0, "No se encontraron tablas en la base de datos.")
            print("\nTablas disponibles en la base de datos:")
            for table in tables:
                print(f"- {table.TABLE_NAME}")
        except Exception as e:
            self.fail(f"Error al listar las tablas de la base de datos: {e}")

    def test_fetch_data_from_inventario(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM inventario")
            rows = cursor.fetchall()
            self.assertIsInstance(rows, list, "El resultado no es una lista.")
            print("\nDatos de la tabla 'inventario':")
            for row in rows:
                print(row)
        except Exception as e:
            self.fail(f"Error al obtener los datos de la tabla 'inventario': {e}")

    def test_table_usuarios_exists(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME = 'usuarios'
            """)
            result = cursor.fetchone()
            self.assertIsNotNone(result, "La tabla 'usuarios' no existe en la base de datos 'usuarios_db'.")
            print("La tabla 'usuarios' existe en la base de datos 'usuarios_db'.")
        except Exception as e:
            self.fail(f"Error al verificar la existencia de la tabla 'usuarios': {e}")
