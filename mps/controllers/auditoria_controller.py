from mps.database_utils import connect_database

class AuditoriaController:
    def __init__(self):
        # Cambia 'auditoria' por el nombre real de la base de datos de auditoría si es diferente
        self.connection = connect_database("auditoria")  # Proporciona el nombre de la base de datos
        print("Conexión establecida con la base de datos de auditoría.")

    def listar_auditoria(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT a.fecha, u.nombre AS usuario, a.accion, a.tabla_afectada
                FROM auditoria a
                JOIN usuarios u ON a.usuario_id = u.id
                ORDER BY a.fecha DESC
            """)
            return cursor.fetchall()
        except Exception as e:
            raise RuntimeError(f"Error al listar la auditoría: {e}")

    def registrar_accion(self, usuario_id, accion, tabla_afectada):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO auditoria (usuario_id, accion, tabla_afectada, fecha) VALUES (?, ?, ?, datetime('now'))",
                (usuario_id, accion, tabla_afectada)
            )
            self.connection.commit()
            print("Acción registrada en la auditoría.")
        except Exception as e:
            raise RuntimeError(f"Error al registrar la acción en la auditoría: {e}")

    def registrar_accion_pendiente(self, usuario_id, accion, tabla_afectada, justificativo):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO auditoria (usuario_id, accion, tabla_afectada, estado, justificativo)
                VALUES (?, ?, ?, 'Pendiente', ?)
            """, (usuario_id, accion, tabla_afectada, justificativo))
            self.connection.commit()
        except Exception as e:
            raise RuntimeError(f"Error al registrar la acción pendiente: {e}")

    def aprobar_accion(self, auditoria_id, admin_id, razon):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE auditoria
                SET estado = 'Aprobada', admin_id = ?, razon = ?
                WHERE id = ?
            """, (admin_id, razon, auditoria_id))
            self.connection.commit()
        except Exception as e:
            raise RuntimeError(f"Error al aprobar la acción: {e}")

    def denegar_accion(self, auditoria_id, admin_id, razon):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                UPDATE auditoria
                SET estado = 'Denegada', admin_id = ?, razon = ?
                WHERE id = ?
            """, (admin_id, razon, auditoria_id))
            self.connection.commit()
        except Exception as e:
            raise RuntimeError(f"Error al denegar la acción: {e}")
