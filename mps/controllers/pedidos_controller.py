from datetime import datetime
from mps.services.db import DBConnection
from mps.services.auditoria import registrar_auditoria

class PedidosController:
    def __init__(self):
        self.db = DBConnection()

    def generar_pedido(self, obra_id, etapa, items):
        """
        Genera un nuevo pedido de material.
        :param obra_id: ID de la obra asociada.
        :param etapa: Etapa del pedido (ej. "medicion", "fabricacion").
        :param items: Lista de materiales con cantidades.
        """
        try:
            self.db.conectar(base="inventario")
            query = """
                INSERT INTO Pedidos (obra_id, etapa, estado, fecha)
                VALUES (?, ?, 'pendiente', ?)
            """
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db.ejecutar_insert(query, [obra_id, etapa, fecha_actual])

            # Registrar auditoría
            registrar_auditoria("admin", "Pedidos", "Generar Pedido", f"Obra ID: {obra_id}, Etapa: {etapa}")
        finally:
            self.db.cerrar()

    def confirmar_pedido(self, id_pedido):
        """
        Confirma un pedido existente.
        :param id_pedido: ID del pedido.
        """
        try:
            self.db.conectar(base="inventario")
            query = """
                UPDATE Pedidos
                SET estado = 'confirmado'
                WHERE id = ?
            """
            self.db.ejecutar_insert(query, [id_pedido])

            # Registrar auditoría
            registrar_auditoria("admin", "Pedidos", "Confirmar Pedido", f"Pedido ID: {id_pedido}")
        finally:
            self.db.cerrar()

    def ajustar_pedido(self, id_pedido, nuevos_items):
        """
        Ajusta un pedido existente con nuevos materiales.
        :param id_pedido: ID del pedido.
        :param nuevos_items: Lista de nuevos materiales con cantidades.
        """
        try:
            self.db.conectar(base="inventario")
            # Aquí se implementaría la lógica para ajustar los materiales del pedido.
            registrar_auditoria("admin", "Pedidos", "Ajustar Pedido", f"Pedido ID: {id_pedido}, Nuevos Items: {nuevos_items}")
        finally:
            self.db.cerrar()
