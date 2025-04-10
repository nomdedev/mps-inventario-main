import unittest
from mps.analysis.dependency_analyzer import DependencyAnalyzer

class TestDependencyAnalyzer(unittest.TestCase):
    def test_analyze(self):
        analyzer = DependencyAnalyzer()
        result = analyzer.analyze("test_file.py")
        self.assertIsInstance(result, list)

    def test_analyze_file_not_found(self):
        analyzer = DependencyAnalyzer()
        with self.assertRaises(FileNotFoundError):
            analyzer.analyze("archivo_inexistente.py")

    def test_analyze_multiple(self):
        analyzer = DependencyAnalyzer()
        result = analyzer.analyze_multiple(["test_file1.py", "test_file2.py"])
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_filter_dependencies(self):
        analyzer = DependencyAnalyzer()
        dependencies = ["modulo1", "modulo2", "modulo3"]
        filtered = analyzer.filter_dependencies(dependencies, "modulo1")
        self.assertEqual(filtered, ["modulo1"])
