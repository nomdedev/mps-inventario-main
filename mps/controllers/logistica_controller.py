from mps.database_utils import connect_database

class LogisticaController:
    def __init__(self):
        self.connection = connect_database()

    def listar_logistica(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT l.id, o.nombre AS obra, l.fecha_entrega, l.estado
                FROM logistica l
                JOIN obras o ON l.obra_id = o.id
            """)
            return cursor.fetchall()
        except Exception as e:
            raise RuntimeError(f"Error al listar la logística: {e}")

    def agregar_logistica(self, obra_id, fecha_entrega, estado):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO logistica (obra_id, fecha_entrega, estado)
                VALUES (?, ?, ?)
            """, (obra_id, fecha_entrega, estado))
            self.connection.commit()
        except Exception as e:
            raise RuntimeError(f"Error al agregar la logística: {e}")
