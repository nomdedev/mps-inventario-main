from mps.database_utils import connect_database

def test_connection():
    try:
        connection = connect_database("usuarios")
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print("Tablas disponibles:", tables)
        connection.close()
    except Exception as e:
        print(f"Error al probar la conexión: {e}")

if __name__ == "__main__":
    test_connection()
