from datetime import datetime
from mps.services.db import DBConnection
from mps.services.auditoria import registrar_auditoria
from mps.models.obra import Obra

class ObrasController:
    def __init__(self):
        self.db = DBConnection()

    def listar_obras(self):
        """
        Lista todas las obras.
        :return: Lista de objetos Obra.
        """
        try:
            self.db.conectar(base="inventario")
            query = "SELECT id, nombre, cliente, estado, fecha_inicio, fecha_fin FROM Obras"
            resultados = self.db.ejecutar_query(query)
            return [Obra.desde_row(row) for row in resultados]
        finally:
            self.db.cerrar()

    def agregar_obra(self, obra: Obra):
        """
        Agrega una nueva obra.
        :param obra: Objeto Obra.
        """
        try:
            self.db.conectar(base="inventario")
            query = """
                INSERT INTO Obras (nombre, cliente, estado, fecha_inicio)
                VALUES (?, ?, 'En Progreso', ?)
            """
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            self.db.ejecutar_insert(query, [obra.nombre, obra.cliente, fecha_actual])
            registrar_auditoria("admin", "Obras", "Agregar Obra", f"Obra: {obra.nombre}, Cliente: {obra.cliente}")
        finally:
            self.db.cerrar()

    def editar_obra(self, id, nuevos_datos):
        """
        Edita una obra existente.
        :param id: ID de la obra.
        :param nuevos_datos: Diccionario con los nuevos datos de la obra.
        """
        try:
            self.db.conectar(base="inventario")
            query = """
                UPDATE Obras
                SET nombre = ?, cliente = ?
                WHERE id = ?
            """
            self.db.ejecutar_insert(query, [nuevos_datos["nombre"], nuevos_datos["cliente"], id])
            registrar_auditoria("admin", "Obras", "Editar Obra", f"ID: {id}, Nuevos Datos: {nuevos_datos}")
        finally:
            self.db.cerrar()

    def finalizar_obra(self, id):
        """
        Finaliza una obra.
        :param id: ID de la obra.
        """
        try:
            self.db.conectar(base="inventario")
            query = """
                UPDATE Obras
                SET estado = 'Finalizada', fecha_fin = ?
                WHERE id = ?
            """
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            self.db.ejecutar_insert(query, [fecha_actual, id])
            registrar_auditoria("admin", "Obras", "Finalizar Obra", f"ID: {id}")
        finally:
            self.db.cerrar()
