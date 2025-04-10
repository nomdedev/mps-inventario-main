import unittest
import os
from mps.packaging.package_builder import PackageBuilder

class TestPackageBuilder(unittest.TestCase):
    def test_build_zip_package(self):
        builder = PackageBuilder()
        dependencies = ["modulo1", "modulo2"]
        output_path = "test_package.zip"
        builder.build_zip_package(dependencies, output_path)
        self.assertTrue(os.path.exists(output_path))
        os.remove(output_path)  # Limpiar archivo de prueba

    def test_build_submodules(self):
        builder = PackageBuilder()
        dependencies = ["modulo1", "modulo2"]
        submodule_name = "submodulo_prueba"
        try:
            builder.build_submodules(dependencies, submodule_name)
        except Exception as e:
            self.fail(f"build_submodules lanzó una excepción inesperada: {e}")
