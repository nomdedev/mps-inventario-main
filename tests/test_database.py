import unittest
from mps.database_utils import connect_database

class TestDatabaseManager(unittest.TestCase):
    def test_connection(self):
        try:
            connection = connect_database(server="localhost\\SQLEXPRESS")
            self.assertIsNotNone(connection)
        except Exception as e:
            self.fail(f"La conexión falló con el error: {e}")
        finally:
            if connection:
                connection.close()

    def test_query_execution(self):
        try:
            connection = connect_database(server="localhost\\SQLEXPRESS")
            cursor = connection.cursor()
            cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES")
            tables = cursor.fetchall()
            self.assertIsInstance(tables, list)
        except Exception as e:
            self.fail(f"Error al ejecutar la consulta: {e}")
        finally:
            if connection:
                connection.close()
