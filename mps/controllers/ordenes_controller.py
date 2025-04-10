from datetime import datetime
from mps.services.db import DBConnection
from mps.services.auditoria import registrar_auditoria
from mps.controllers.aprobaciones_controller import AprobacionesController
from mps.models.orden import Orden, OrdenMaterial

class OrdenesController:
    def __init__(self):
        self.db = DBConnection()
        self.aprobaciones_controller = AprobacionesController()

    def crear_orden(self, obra_id, materiales, usuario):
        """
        Crea una nueva orden y sus materiales asociados.
        :param obra_id: ID de la obra asociada.
        :param materiales: Lista de materiales con cantidades.
        :param usuario: Usuario que crea la orden.
        """
        try:
            self.db.conectar(base="inventario")
            # Insertar la orden
            query_orden = """
                INSERT INTO Ordenes (obra_id, fecha, estado, total_items, creado_por)
                VALUES (?, ?, 'pendiente', ?, ?)
            """
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            total_items = sum(item["cantidad"] for item in materiales)
            self.db.ejecutar_insert(query_orden, [obra_id, fecha_actual, total_items, usuario])

            # Obtener el ID de la orden recién creada
            query_last_id = "SELECT SCOPE_IDENTITY()"
            orden_id = self.db.ejecutar_query(query_last_id)[0][0]

            # Insertar los materiales en OrdenMaterial
            query_material = """
                INSERT INTO OrdenMaterial (orden_id, material_id, cantidad)
                VALUES (?, ?, ?)
            """
            for item in materiales:
                self.db.ejecutar_insert(query_material, [orden_id, item["material_id"], item["cantidad"]])

            # Registrar en auditoría
            registrar_auditoria(usuario, "Ordenes", "Crear Orden", f"Orden ID: {orden_id}, Obra ID: {obra_id}, Total Items: {total_items}")

            # Crear solicitud de aprobación si el total de materiales supera un umbral
            if total_items > 50:  # Umbral de ejemplo
                self.aprobaciones_controller.crear_solicitud("OrdenMaterial", orden_id, usuario)
                registrar_auditoria(usuario, "Aprobaciones", "Crear Solicitud", f"Orden ID: {orden_id}, Total Items: {total_items}")
        finally:
            self.db.cerrar()

    def cambiar_estado_orden(self, id_orden, nuevo_estado, usuario):
        """
        Cambia el estado de una orden.
        :param id_orden: ID de la orden.
        :param nuevo_estado: Nuevo estado de la orden.
        :param usuario: Usuario que realiza el cambio.
        """
        try:
            self.db.conectar(base="inventario")
            query = """
                UPDATE Ordenes
                SET estado = ?
                WHERE id = ?
            """
            self.db.ejecutar_insert(query, [nuevo_estado, id_orden])
            registrar_auditoria(usuario, "Ordenes", "Cambiar Estado", f"Orden ID: {id_orden}, Nuevo Estado: {nuevo_estado}")
        finally:
            self.db.cerrar()

    def obtener_ordenes_por_obra(self, obra_id):
        """
        Obtiene todas las órdenes asociadas a una obra.
        :param obra_id: ID de la obra.
        :return: Lista de objetos Orden.
        """
        try:
            self.db.conectar(base="inventario")
            query = """
                SELECT id, obra_id, fecha, estado, total_items, creado_por
                FROM Ordenes
                WHERE obra_id = ?
            """
            resultados = self.db.ejecutar_query(query, [obra_id])
            return [Orden.desde_row(row) for row in resultados]
        finally:
            self.db.cerrar()

    def obtener_detalle_orden(self, id_orden):
        """
        Obtiene el detalle de una orden.
        :param id_orden: ID de la orden.
        :return: Lista de objetos OrdenMaterial.
        """
        try:
            self.db.conectar(base="inventario")
            query = """
                SELECT orden_id, material_id, cantidad
                FROM OrdenMaterial
                WHERE orden_id = ?
            """
            resultados = self.db.ejecutar_query(query, [id_orden])
            return [OrdenMaterial.desde_row(row) for row in resultados]
        finally:
            self.db.cerrar()
