from datetime import datetime
from mps.services.db import DBConnection
from mps.services.auditoria import registrar_auditoria
from mps.controllers.aprobaciones_controller import AprobacionesController

class MovimientosController:
    def __init__(self):
        self.db = DBConnection()
        self.aprobaciones_controller = AprobacionesController()

    def aumentar_stock(self, material_id, cantidad):
        """
        Aumenta el stock total y disponible de un material.
        :param material_id: ID del material.
        :param cantidad: Cantidad a aumentar.
        """
        try:
            self.db.conectar(base="inventario")
            query = """
                UPDATE Materiales
                SET stock_total = stock_total + ?, stock_disponible = stock_disponible + ?
                WHERE id = ?
            """
            self.db.ejecutar_insert(query, [cantidad, cantidad, material_id])
        finally:
            self.db.cerrar()

    def disminuir_stock(self, material_id, cantidad):
        """
        Disminuye el stock disponible de un material.
        :param material_id: ID del material.
        :param cantidad: Cantidad a disminuir.
        """
        try:
            self.db.conectar(base="inventario")
            query_validar_stock = "SELECT stock_disponible FROM Materiales WHERE id = ?"
            resultado = self.db.ejecutar_query(query_validar_stock, [material_id])
            if not resultado or resultado[0][0] < cantidad:
                raise ValueError("Stock insuficiente para realizar la operación.")
            
            query = """
                UPDATE Materiales
                SET stock_disponible = stock_disponible - ?
                WHERE id = ?
            """
            self.db.ejecutar_insert(query, [cantidad, material_id])
        finally:
            self.db.cerrar()

    def registrar_entrada(self, material_id, cantidad, usuario, obra_id=None):
        """
        Registra una entrada de stock para un material.
        """
        try:
            self.db.conectar(base="inventario")
            query_movimiento = """
                INSERT INTO Movimientos (material_id, cantidad, tipo, usuario, obra_id, fecha, estado)
                VALUES (?, ?, 'entrada', ?, ?, ?, 'aprobado')
            """
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db.ejecutar_insert(query_movimiento, [material_id, cantidad, usuario, obra_id, fecha_actual])
            self.aumentar_stock(material_id, cantidad)
            registrar_auditoria(usuario, "Movimientos", "Registrar Entrada", f"Material ID: {material_id}, Cantidad: {cantidad}, Obra ID: {obra_id}")
        finally:
            self.db.cerrar()

    def registrar_salida(self, material_id, cantidad, usuario, obra_id=None):
        """
        Registra una salida de stock para un material.
        """
        try:
            self.db.conectar(base="inventario")
            query_movimiento = """
                INSERT INTO Movimientos (material_id, cantidad, tipo, usuario, obra_id, fecha, estado)
                VALUES (?, ?, 'salida', ?, ?, ?, ?)
            """
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            estado = "pendiente" if cantidad > 10 else "aprobado"

            if estado == "pendiente":
                self.aprobaciones_controller.crear_solicitud("SalidaStock", material_id, usuario)
                registrar_auditoria(usuario, "Aprobaciones", "Crear Solicitud", f"Material ID: {material_id}, Cantidad: {cantidad}")
                raise RuntimeError("La salida requiere aprobación antes de ejecutarse.")

            self.db.ejecutar_insert(query_movimiento, [material_id, cantidad, usuario, obra_id, fecha_actual, estado])
            self.disminuir_stock(material_id, cantidad)
            registrar_auditoria(usuario, "Movimientos", "Registrar Salida", f"Material ID: {material_id}, Cantidad: {cantidad}, Obra ID: {obra_id}")
        finally:
            self.db.cerrar()

    def apartar_material(self, material_id, cantidad, obra_id, usuario):
        """
        Aparta una cantidad de material para una obra específica.
        :param material_id: ID del material.
        :param cantidad: Cantidad a apartar.
        :param obra_id: ID de la obra asociada.
        :param usuario: Usuario que realiza la acción.
        """
        try:
            self.db.conectar(base="inventario")

            # Validar stock suficiente
            query_validar_stock = "SELECT stock_disponible FROM Materiales WHERE id = ?"
            resultado = self.db.ejecutar_query(query_validar_stock, [material_id])
            if not resultado or resultado[0][0] < cantidad:
                raise ValueError("Stock insuficiente para realizar el apartado.")

            # Actualizar stock
            query_actualizar_stock = """
                UPDATE Materiales
                SET stock_disponible = stock_disponible - ?, stock_apartado = stock_apartado + ?
                WHERE id = ?
            """
            self.db.ejecutar_insert(query_actualizar_stock, [cantidad, cantidad, material_id])

            # Registrar movimiento
            query_movimiento = """
                INSERT INTO Movimientos (material_id, cantidad, tipo, usuario, obra_id, fecha, estado)
                VALUES (?, ?, 'apartado', ?, ?, ?, 'aprobado')
            """
            fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.db.ejecutar_insert(query_movimiento, [material_id, cantidad, usuario, obra_id, fecha_actual])

            # Registrar auditoría
            registrar_auditoria(usuario, "Movimientos", "Apartar Material", f"Material ID: {material_id}, Cantidad: {cantidad}, Obra ID: {obra_id}")

            # Crear solicitud de aprobación si la cantidad es alta
            if cantidad > 10:
                self.aprobaciones_controller.crear_solicitud("ApartadoMaterial", obra_id, usuario)
                registrar_auditoria(usuario, "Aprobaciones", "Crear Solicitud", f"Material ID: {material_id}, Cantidad: {cantidad}, Obra ID: {obra_id}")
                raise RuntimeError("El apartado requiere aprobación antes de ejecutarse.")
        finally:
            self.db.cerrar()
