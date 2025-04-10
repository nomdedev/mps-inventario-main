class Orden:
    def __init__(self, id, obra_id, fecha, estado, total_items, creado_por):
        """
        Modelo de datos para una orden.
        :param id: ID de la orden.
        :param obra_id: ID de la obra asociada.
        :param fecha: Fecha de creación de la orden.
        :param estado: Estado de la orden (ej. "pendiente", "aprobada").
        :param total_items: Total de materiales en la orden.
        :param creado_por: Usuario que creó la orden.
        """
        self.id = id
        self.obra_id = obra_id
        self.fecha = fecha
        self.estado = estado
        self.total_items = total_items
        self.creado_por = creado_por

    @staticmethod
    def desde_row(row):
        """
        Crea un objeto Orden a partir de una fila de base de datos.
        :param row: Fila de la base de datos (tupla o lista).
        :return: Objeto Orden.
        """
        return Orden(
            id=row[0],
            obra_id=row[1],
            fecha=row[2],
            estado=row[3],
            total_items=row[4],
            creado_por=row[5]
        )


class OrdenMaterial:
    def __init__(self, orden_id, material_id, cantidad):
        """
        Modelo de datos para un material en una orden.
        :param orden_id: ID de la orden asociada.
        :param material_id: ID del material.
        :param cantidad: Cantidad solicitada del material.
        """
        self.orden_id = orden_id
        self.material_id = material_id
        self.cantidad = cantidad

    @staticmethod
    def desde_row(row):
        """
        Crea un objeto OrdenMaterial a partir de una fila de base de datos.
        :param row: Fila de la base de datos (tupla o lista).
        :return: Objeto OrdenMaterial.
        """
        return OrdenMaterial(
            orden_id=row[0],
            material_id=row[1],
            cantidad=row[2]
        )
