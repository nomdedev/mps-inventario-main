class EstadoObra:
    def __init__(self, id, obra_id, etapa, estado, fecha_inicio, fecha_fin, observaciones):
        """
        Modelo de datos para el estado de una obra.
        :param id: ID del estado.
        :param obra_id: ID de la obra asociada.
        :param etapa: Etapa de la obra (ej. "medicion", "instalacion").
        :param estado: Estado de la etapa (ej. "en progreso", "finalizada").
        :param fecha_inicio: Fecha de inicio de la etapa.
        :param fecha_fin: Fecha de finalización de la etapa (puede ser None si no ha finalizado).
        :param observaciones: Observaciones adicionales sobre la etapa.
        """
        self.id = id
        self.obra_id = obra_id
        self.etapa = etapa
        self.estado = estado
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.observaciones = observaciones

    @staticmethod
    def desde_row(row):
        """
        Crea un objeto EstadoObra a partir de una fila de base de datos.
        :param row: Fila de la base de datos (tupla o lista).
        :return: Objeto EstadoObra.
        """
        return EstadoObra(
            id=row[0],
            obra_id=row[1],
            etapa=row[2],
            estado=row[3],
            fecha_inicio=row[4],
            fecha_fin=row[5],
            observaciones=row[6]
        )
