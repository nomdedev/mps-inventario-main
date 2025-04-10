from mps.services.db import DBConnection

class DashboardController:
    def __init__(self):
        self.db = DBConnection()

    def obtener_totales(self):
        """
        Obtiene totales generales para el dashboard.
        :return: Diccionario con métricas generales.
        """
        try:
            self.db.conectar(base="inventario")
            query_totales = """
                SELECT 
                    (SELECT COUNT(*) FROM Materiales) AS total_materiales,
                    (SELECT SUM(stock_disponible) FROM Materiales) AS stock_total,
                    (SELECT COUNT(*) FROM Usuarios) AS total_usuarios,
                    (SELECT COUNT(*) FROM Obras WHERE estado = 'En Progreso') AS obras_activas,
                    (SELECT COUNT(*) FROM Ordenes WHERE estado = 'pendiente') AS ordenes_pendientes
            """
            resultado = self.db.ejecutar_query(query_totales)[0]
            return {
                "total_materiales": resultado[0],
                "stock_total": resultado[1],
                "total_usuarios": resultado[2],
                "obras_activas": resultado[3],
                "ordenes_pendientes": resultado[4]
            }
        finally:
            self.db.cerrar()

    def obtener_materiales_mas_usados(self):
        """
        Obtiene los materiales más usados.
        :return: Lista de diccionarios con códigos y cantidades.
        """
        try:
            self.db.conectar(base="inventario")
            query = """
                SELECT codigo, SUM(cantidad) AS total_usado
                FROM Movimientos
                JOIN Materiales ON Movimientos.material_id = Materiales.id
                WHERE tipo = 'salida'
                GROUP BY codigo
                ORDER BY total_usado DESC
                LIMIT 5
            """
            resultados = self.db.ejecutar_query(query)
            return [{"codigo": row[0], "cantidad": row[1]} for row in resultados]
        finally:
            self.db.cerrar()

    def obtener_etapas_obras(self):
        """
        Obtiene la cantidad de obras por etapa actual.
        :return: Diccionario con etapas y cantidades.
        """
        try:
            self.db.conectar(base="inventario")
            query = """
                SELECT etapa, COUNT(*) AS total
                FROM EstadoObra
                WHERE estado = 'en progreso'
                GROUP BY etapa
            """
            resultados = self.db.ejecutar_query(query)
            return {row[0]: row[1] for row in resultados}
        finally:
            self.db.cerrar()

    def obtener_entregas_recientes(self):
        """
        Obtiene las últimas 5 entregas registradas.
        :return: Lista de diccionarios con obra, usuario y fecha.
        """
        try:
            self.db.conectar(base="inventario")
            query = """
                SELECT Obras.nombre, Movimientos.usuario, Movimientos.fecha
                FROM Movimientos
                JOIN Obras ON Movimientos.obra_id = Obras.id
                WHERE tipo = 'entrega'
                ORDER BY Movimientos.fecha DESC
                LIMIT 5
            """
            resultados = self.db.ejecutar_query(query)
            return [{"obra": row[0], "usuario": row[1], "fecha": row[2]} for row in resultados]
        finally:
            self.db.cerrar()
