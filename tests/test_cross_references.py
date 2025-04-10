import unittest
import os
from mps.cross_references.cross_reference import CrossReference

class TestCrossReference(unittest.TestCase):
    def test_generate_report(self):
        cross_ref = CrossReference()
        try:
            cross_ref.generate_report(["modulo1", "modulo2"])
        except Exception as e:
            self.fail(f"generate_report lanzó una excepción inesperada: {e}")

    def test_save_report(self):
        cross_ref = CrossReference()
        output_path = "test_report.txt"
        try:
            cross_ref.save_report(["modulo1", "modulo2"], output_path)
            self.assertTrue(os.path.exists(output_path))
        finally:
            if os.path.exists(output_path):
                os.remove(output_path)

    def test_load_report(self):
        cross_ref = CrossReference()
        input_path = "test_report.txt"
        content = "Reporte de referencias cruzadas:\n['modulo1', 'modulo2']"
        with open(input_path, "w") as f:
            f.write(content)
        try:
            loaded_content = cross_ref.load_report(input_path)
            self.assertEqual(loaded_content, content)
        finally:
            if os.path.exists(input_path):
                os.remove(input_path)
