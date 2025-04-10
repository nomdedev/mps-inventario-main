import unittest
import os
from mps.utils.file_utils import is_file_accessible, write_file

class TestFileUtils(unittest.TestCase):
    def test_is_file_accessible(self):
        test_file = "test_file.txt"
        with open(test_file, 'w') as f:
            f.write("Contenido de prueba")
        self.assertTrue(is_file_accessible(test_file))
        os.remove(test_file)

    def test_is_file_accessible_nonexistent(self):
        self.assertFalse(is_file_accessible("archivo_inexistente.txt"))

    def test_write_file(self):
        test_file = "test_write.txt"
        content = "Contenido de prueba"
        write_file(test_file, content)
        with open(test_file, 'r') as f:
            self.assertEqual(f.read(), content)
        os.remove(test_file)
