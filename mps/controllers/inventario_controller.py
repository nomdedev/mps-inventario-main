from mps.services.db import DBConnection
from mps.services.auditoria import registrar_auditoria
from mps.models.material import Material

class InventarioController:
    def __init__(self):
        self.db = DBConnection()

    def listar_materiales(self):
        """
        Lista todos los materiales del inventario.
        :return: Lista de objetos Material.
        """
        db = DBConnection()
        try:
            db.conectar(base="inventario")
            query = """
                SELECT id, codigo, descripcion, largo_mm, stock_total, stock_disponible, stock_apartado
                FROM Materiales
            """
            resultados = db.ejecutar_query(query)
            return [Material.desde_row(row) for row in resultados]
        except Exception as e:
            db.logger.error(f"Error al listar materiales: {e}")
            raise RuntimeError(f"Error al listar materiales: {e}")
        finally:
            db.cerrar()

    def agregar_material(self, material):
        """
        Agrega un nuevo material al inventario.
        :param material: Objeto Material o diccionario con los datos del material.
        """
        db = DBConnection()
        try:
            db.conectar(base="inventario")
            query = """
                INSERT INTO Materiales (codigo, descripcion, largo_mm, stock_total, stock_disponible, stock_apartado)
                VALUES (?, ?, ?, 0, 0, 0)
            """
            if isinstance(material, Material):
                params = [material.codigo, material.descripcion, material.largo_mm]
            elif isinstance(material, dict):
                params = [material["codigo"], material["descripcion"], material["largo_mm"]]
            else:
                raise ValueError("El parámetro 'material' debe ser un objeto Material o un diccionario.")

            db.ejecutar_insert(query, params)
            registrar_auditoria("admin", "Inventario", "Agregar Material", f"Material: {params[1]}")
        except Exception as e:
            raise RuntimeError(f"Error al agregar el material: {e}")
        finally:
            db.cerrar()

    def editar_material(self, id, nuevos_datos: dict):
        """
        Edita un material existente en el inventario.
        :param id: ID del material.
        :param nuevos_datos: Diccionario con los nuevos datos del material.
        """
        try:
            self.db.conectar()
            query = """
                UPDATE Materiales
                SET codigo = ?, descripcion = ?, largo_mm = ?, stock_total = ?, stock_disponible = ?, stock_apartado = ?
                WHERE id = ?
            """
            self.db.ejecutar_insert(query, [
                nuevos_datos["codigo"], nuevos_datos["descripcion"], nuevos_datos["largo_mm"],
                nuevos_datos["stock_total"], nuevos_datos["stock_disponible"], nuevos_datos["stock_apartado"], id
            ])
            registrar_auditoria("admin", "Inventario", "Editar Material", f"ID: {id}, Nuevos Datos: {nuevos_datos}")
        finally:
            self.db.cerrar()

    def eliminar_material(self, id):
        """
        Elimina un material del inventario.
        :param id: ID del material.
        """
        try:
            self.db.conectar()
            query = "DELETE FROM Materiales WHERE id = ?"
            self.db.ejecutar_insert(query, [id])
            registrar_auditoria("admin", "Inventario", "Eliminar Material", f"ID: {id}")
        finally:
            self.db.cerrar()

    def registrar_entrada(self, id_material, cantidad):
        """
        Registra una entrada de stock para un material.
        :param id_material: ID del material.
        :param cantidad: Cantidad a agregar.
        """
        try:
            self.db.conectar()
            query = """
                UPDATE Materiales
                SET stock_total = stock_total + ?, stock_disponible = stock_disponible + ?
                WHERE id = ?
            """
            self.db.ejecutar_insert(query, [cantidad, cantidad, id_material])
            registrar_auditoria("admin", "Inventario", "Registrar Entrada", f"ID: {id_material}, Cantidad: {cantidad}")
        finally:
            self.db.cerrar()

    def registrar_salida(self, id_material, cantidad):
        """
        Registra una salida de stock para un material.
        :param id_material: ID del material.
        :param cantidad: Cantidad a descontar.
        """
        try:
            self.db.conectar()
            query = """
                UPDATE Materiales
                SET stock_disponible = stock_disponible - ?
                WHERE id = ? AND stock_disponible >= ?
            """
            self.db.ejecutar_insert(query, [cantidad, id_material, cantidad])
            registrar_auditoria("admin", "Inventario", "Registrar Salida", f"ID: {id_material}, Cantidad: {cantidad}")
        finally:
            self.db.cerrar()

    def apartar_material(self, id_material, cantidad, obra_id):
        """
        Aparta una cantidad de material para una obra específica.
        :param id_material: ID del material.
        :param cantidad: Cantidad a apartar.
        :param obra_id: ID de la obra.
        """
        try:
            self.db.conectar()
            query = """
                UPDATE Materiales
                SET stock_disponible = stock_disponible - ?, stock_apartado = stock_apartado + ?
                WHERE id = ? AND stock_disponible >= ?
            """
            self.db.ejecutar_insert(query, [cantidad, cantidad, id_material, cantidad])
            registrar_auditoria("admin", "Inventario", "Apartar Material", f"ID: {id_material}, Cantidad: {cantidad}, Obra ID: {obra_id}")
        finally:
            self.db.cerrar()
