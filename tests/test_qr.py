import unittest
import os
from mps.controllers.qr_controller import QRController

class TestQRController(unittest.TestCase):
    def setUp(self):
        self.controller = QRController()
        self.test_data = "Datos de prueba para QR"
        self.test_qr_path = "test_qr.png"

    def tearDown(self):
        if os.path.exists(self.test_qr_path):
            os.remove(self.test_qr_path)

    def test_generar_qr(self):
        try:
            self.controller.generar_qr(self.test_data, self.test_qr_path)
            self.assertTrue(os.path.exists(self.test_qr_path))
        except Exception as e:
            self.fail(f"Error al generar el QR: {e}")

    def test_escanear_qr(self):
        try:
            self.controller.generar_qr(self.test_data, self.test_qr_path)
            result = self.controller.escanear_qr(self.test_qr_path)
            self.assertEqual(result, self.test_data)
        except Exception as e:
            self.fail(f"Error al escanear el QR: {e}")
