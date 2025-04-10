import sqlite3
import os

def initialize_auditoria_db():
    ruta_db = "c:/Users/Oficina/Documents/Proyectos/mps-inventario/databases/auditoria.db"
    os.makedirs(os.path.dirname(ruta_db), exist_ok=True)
    connection = sqlite3.connect(ruta_db)
    cursor = connection.cursor()

    # Crear la tabla auditoria si no existe
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS auditoria (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            accion TEXT NOT NULL,
            tabla_afectada TEXT NOT NULL,
            fecha TEXT NOT NULL,
            estado TEXT DEFAULT 'Completada',
            justificativo TEXT,
            admin_id INTEGER,
            razon TEXT
        )
    """)
    print("Estructura de la base de datos 'auditoria' inicializada.")
    connection.commit()
    connection.close()

if __name__ == "__main__":
    initialize_auditoria_db()
