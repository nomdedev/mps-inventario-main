import unittest
from mps.database_utils import connect_database

class TestDatabaseTables(unittest.TestCase):
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

    def test_list_all_tables(self):
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

    def test_fetch_data_from_tables(self):
        tables_to_test = [
            "inventario", "usuarios", "obras", "auditoria", "ordenes", "orden_detalles"
        ]
        for table in tables_to_test:
            with self.subTest(table=table):
                try:
                    cursor = self.connection.cursor()
                    cursor.execute(f"SELECT TOP 5 * FROM {table}")
                    rows = cursor.fetchall()
                    print(f"\nDatos de la tabla '{table}':")
                    if rows:
                        for row in rows:
                            print(row)
                    else:
                        print(f"La tabla '{table}' no contiene datos.")
                except Exception as e:
                    self.fail(f"Error al obtener datos de la tabla '{table}': {e}")
