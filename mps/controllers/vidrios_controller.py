from mps.database_utils import connect_database

class VidriosController:
    def __init__(self):
        self.connection = connect_database()

    def listar_vidrios(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT v.id, o.nombre AS obra, v.ancho, v.alto, v.tipologia, v.observaciones, v.estado
                FROM vidrios v
                JOIN obras o ON v.obra_id = o.id
            """)
            return cursor.fetchall()
        except Exception as e:
            raise RuntimeError(f"Error al listar los vidrios: {e}")

    def agregar_vidrio(self, obra_id, ancho, alto, tipologia, observaciones):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO vidrios (obra_id, ancho, alto, tipologia, observaciones)
                VALUES (?, ?, ?, ?, ?)
            """, (obra_id, ancho, alto, tipologia, observaciones))
            self.connection.commit()
        except Exception as e:
            raise RuntimeError(f"Error al agregar el vidrio: {e}")

    def actualizar_estado(self, vidrio_id, estado):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE vidrios
                SET estado = ?
                WHERE id = ?
            """, (estado, vidrio_id))
            self.connection.commit()
        except Exception as e:
            raise RuntimeError(f"Error al actualizar el estado del vidrio: {e}")
