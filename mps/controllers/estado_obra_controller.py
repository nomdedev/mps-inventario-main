from datetime import datetime
from mps.services.db import DBConnection
from mps.services.auditoria import registrar_auditoria
from mps.models.estado_obra import EstadoObra

class EstadoObraController:
    def __init__(self):
        self.db = DBConnection()

    def iniciar_etapa(self, obra_id, etapa):
        """
        Inicia una nueva etapa para una obra.
        :param obra_id: ID de la obra.
        :param etapa: Nombre de la etapa a iniciar.
        """
        try:
            self.db.conectar(base="inventario")
            query = """
                INSERT INTO EstadoObra (obra_id, etapa, estado, fecha_inicio)
                VALUES (?, ?, 'en progreso', ?)
            """
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db.ejecutar_insert(query, [obra_id, etapa, fecha_actual])
            registrar_auditoria("admin", "EstadoObra", "Iniciar Etapa", f"Obra ID: {obra_id}, Etapa: {etapa}")
        finally:
            self.db.cerrar()

    def finalizar_etapa(self, obra_id, etapa, observaciones=""):
        """
        Finaliza una etapa para una obra.
        :param obra_id: ID de la obra.
        :param etapa: Nombre de la etapa a finalizar.
        :param observaciones: Observaciones adicionales sobre la etapa.
        """
        try:
            self.db.conectar(base="inventario")
            query = """
                UPDATE EstadoObra
                SET estado = 'finalizada', fecha_fin = ?, observaciones = ?
                WHERE obra_id = ? AND etapa = ? AND estado = 'en progreso'
            """
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db.ejecutar_insert(query, [fecha_actual, observaciones, obra_id, etapa])
            registrar_auditoria("admin", "EstadoObra", "Finalizar Etapa", f"Obra ID: {obra_id}, Etapa: {etapa}, Observaciones: {observaciones}")

            # Disparar flujo de pedido de material si la etapa es 'medicion'
            if etapa == "medicion":
                self._disparar_pedido_material(obra_id)
        finally:
            self.db.cerrar()

    def obtener_estado_actual(self, obra_id):
        """
        Obtiene el estado actual de una obra.
        :param obra_id: ID de la obra.
        :return: Objeto EstadoObra con el estado actual.
        """
        try:
            self.db.conectar(base="inventario")
            query = """
                SELECT id, obra_id, etapa, estado, fecha_inicio, fecha_fin, observaciones
                FROM EstadoObra
                WHERE obra_id = ? AND estado = 'en progreso'
            """
            resultado = self.db.ejecutar_query(query, [obra_id])
            return EstadoObra.desde_row(resultado[0]) if resultado else None
        finally:
            self.db.cerrar()

    def _disparar_pedido_material(self, obra_id):
        """
        Dispara el flujo de pedido de material para una obra.
        :param obra_id: ID de la obra.
        """
        registrar_auditoria("admin", "EstadoObra", "Disparar Pedido Material", f"Obra ID: {obra_id}")
        print(f"Flujo de pedido de material disparado para la obra ID {obra_id}.")
