class Obra:
    def __init__(self, id, nombre, cliente, estado, fecha_inicio, fecha_fin):
        """
        Modelo de datos para una obra.
        :param id: ID de la obra.
        :param nombre: Nombre de la obra.
        :param cliente: Cliente asociado a la obra.
        :param estado: Estado de la obra (ej. "En Progreso", "Finalizada").
        :param fecha_inicio: Fecha de inicio de la obra.
        :param fecha_fin: Fecha de finalización de la obra (puede ser None si no ha finalizado).
        """
        self.id = id
        self.nombre = nombre
        self.cliente = cliente
        self.estado = estado
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin

    @staticmethod
    def desde_row(row):
        """
        Crea un objeto Obra a partir de una fila de base de datos.
        :param row: Fila de la base de datos (tupla o lista).
        :return: Objeto Obra.
        """
        return Obra(
            id=row[0],
            nombre=row[1],
            cliente=row[2],
            estado=row[3],
            fecha_inicio=row[4],
            fecha_fin=row[5]
        )
