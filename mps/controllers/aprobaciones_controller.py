from datetime import datetime
from mps.services.db import DBConnection
from mps.services.auditoria import registrar_auditoria

class AprobacionesController:
    def __init__(self):
        self.db = DBConnection()

    def crear_solicitud(self, tipo, id_referencia, usuario_solicitante):
        """
        Crea una nueva solicitud de aprobación.
        :param tipo: Tipo de solicitud (ej. "Orden", "Usuario").
        :param id_referencia: ID de la referencia asociada a la solicitud.
        :param usuario_solicitante: Usuario que solicita la aprobación.
        """
        try:
            self.db.conectar(base="inventario")
            query = """
                INSERT INTO Aprobaciones (tipo, id_referencia, usuario_solicitante, estado, fecha)
                VALUES (?, ?, ?, 'pendiente', ?)
            """
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db.ejecutar_insert(query, [tipo, id_referencia, usuario_solicitante, fecha_actual])
            registrar_auditoria(usuario_solicitante, "Aprobaciones", "Crear Solicitud", f"Tipo: {tipo}, ID Referencia: {id_referencia}")
        finally:
            self.db.cerrar()

    def listar_pendientes(self):
        """
        Lista todas las solicitudes pendientes.
        :return: Lista de solicitudes con estado "pendiente".
        """
        try:
            self.db.conectar(base="inventario")
            query = "SELECT id, tipo, id_referencia, usuario_solicitante, estado, fecha FROM Aprobaciones WHERE estado = 'pendiente'"
            resultados = self.db.ejecutar_query(query)
            return resultados
        finally:
            self.db.cerrar()

    def aprobar_solicitud(self, id, usuario_aprobador, comentario=""):
        """
        Aprueba una solicitud de aprobación.
        :param id: ID de la solicitud.
        :param usuario_aprobador: Usuario que aprueba la solicitud.
        :param comentario: Comentario opcional del aprobador.
        """
        try:
            self.db.conectar(base="inventario")
            query = """
                UPDATE Aprobaciones
                SET estado = 'aprobado', usuario_aprobador = ?, comentario = ?, fecha_aprobacion = ?
                WHERE id = ?
            """
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db.ejecutar_insert(query, [usuario_aprobador, comentario, fecha_actual, id])
            registrar_auditoria(usuario_aprobador, "Aprobaciones", "Aprobar Solicitud", f"ID: {id}, Comentario: {comentario}")
        finally:
            self.db.cerrar()

    def rechazar_solicitud(self, id, usuario_aprobador, comentario):
        """
        Rechaza una solicitud de aprobación.
        :param id: ID de la solicitud.
        :param usuario_aprobador: Usuario que rechaza la solicitud.
        :param comentario: Comentario del rechazador.
        """
        try:
            self.db.conectar(base="inventario")
            query = """
                UPDATE Aprobaciones
                SET estado = 'rechazado', usuario_aprobador = ?, comentario = ?, fecha_aprobacion = ?
                WHERE id = ?
            """
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db.ejecutar_insert(query, [usuario_aprobador, comentario, fecha_actual, id])
            registrar_auditoria(usuario_aprobador, "Aprobaciones", "Rechazar Solicitud", f"ID: {id}, Comentario: {comentario}")
        finally:
            self.db.cerrar()
