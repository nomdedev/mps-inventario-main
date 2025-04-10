import unittest
from mps.controllers.ordenes_controller import OrdenesController

class TestOrdenesController(unittest.TestCase):
    def setUp(self):
        self.controller = OrdenesController()

    def test_listar_ordenes(self):
        try:
            ordenes = self.controller.listar_ordenes()
            self.assertIsInstance(ordenes, list, "El resultado no es una lista.")
            print("Órdenes disponibles:")
            for orden in ordenes:
                print(orden)
        except Exception as e:
            self.fail(f"Error al listar las órdenes: {e}")

    def test_agregar_orden(self):
        try:
            self.controller.agregar_orden(1, 1, 100.50)  # IDs de prueba
            ordenes = self.controller.listar_ordenes()
            self.assertTrue(
                any(orden[3] == 100.50 for orden in ordenes),
                "La orden no fue agregada correctamente."
            )
        except Exception as e:
            self.fail(f"Error al agregar una orden: {e}")

    def test_verificar_tabla_ordenes(self):
        try:
            existe = self.controller.verificar_tabla_ordenes()
            self.assertTrue(existe, "La tabla 'ordenes' no existe o no es accesible.")
        except Exception as e:
            self.fail(f"Error al verificar la tabla 'ordenes': {e}")
