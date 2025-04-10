import unittest
from mps.controllers.obras_controller import ObrasController

class TestObrasController(unittest.TestCase):
    def setUp(self):
        self.controller = ObrasController()

    def test_listar_obras(self):
        try:
            obras = self.controller.listar_obras()
            self.assertIsInstance(obras, list, "El resultado no es una lista.")
            print("Obras disponibles:")
            for obra in obras:
                print(obra)
        except Exception as e:
            self.fail(f"Error al listar las obras: {e}")

    def test_agregar_obra(self):
        try:
            self.controller.agregar_obra("Obra de prueba", "Cliente de prueba")
            obras = self.controller.listar_obras()
            self.assertTrue(
                any(obra[1] == "Obra de prueba" and obra[2] == "Cliente de prueba" for obra in obras),
                "La obra no fue agregada correctamente."
            )
        except Exception as e:
            self.fail(f"Error al agregar una obra: {e}")
