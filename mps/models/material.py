# Modelo de datos para representar un material del inventario.
# Incluirá atributos como id, nombre, cantidad, precio y observaciones.

class Material:
    def __init__(self, id, codigo, descripcion, largo_mm, stock_total, stock_disponible, stock_apartado):
        """
        Modelo de datos para un material del inventario.
        :param id: ID del material.
        :param codigo: Código único del material.
        :param descripcion: Descripción del material.
        :param largo_mm: Largo del material en milímetros.
        :param stock_total: Cantidad total en stock.
        :param stock_disponible: Cantidad disponible en stock.
        :param stock_apartado: Cantidad apartada en stock.
        """
        self.id = id
        self.codigo = codigo
        self.descripcion = descripcion
        self.largo_mm = largo_mm
        self.stock_total = stock_total
        self.stock_disponible = stock_disponible
        self.stock_apartado = stock_apartado

    @staticmethod
    def desde_row(row):
        """
        Crea un objeto Material a partir de una fila de base de datos.
        :param row: Fila de la base de datos (tupla o lista).
        :return: Objeto Material.
        """
        # Validar que la fila tenga al menos 7 elementos para evitar errores de índice.
        if len(row) < 7:
            raise ValueError("La fila proporcionada no tiene suficientes columnas para crear un objeto Material.")
        
        return Material(
            id=row[0],
            codigo=row[1],
            descripcion=row[2],
            largo_mm=row[3],
            stock_total=row[4],
            stock_disponible=row[5],
            stock_apartado=row[6]
        )
