import unittest
from mps.controllers.usuarios_controller import UsuariosController

class TestUsuariosController(unittest.TestCase):
    def setUp(self):
        self.controller = UsuariosController()

    def test_listar_usuarios(self):
        try:
            usuarios = self.controller.listar_usuarios()
            self.assertIsInstance(usuarios, list, "El resultado no es una lista.")
            print("Usuarios disponibles:")
            for usuario in usuarios:
                print(usuario)
        except Exception as e:
            self.fail(f"Error al listar los usuarios: {e}")

    def test_agregar_usuario(self):
        try:
            self.controller.agregar_usuario("Usuario de prueba", "Operador")
            usuarios = self.controller.listar_usuarios()
            self.assertTrue(
                any(usuario[1] == "Usuario de prueba" and usuario[2] == "Operador" for usuario in usuarios),
                "El usuario no fue agregado correctamente."
            )
        except Exception as e:
            self.fail(f"Error al agregar un usuario: {e}")
