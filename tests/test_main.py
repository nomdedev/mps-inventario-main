import unittest
from unittest.mock import patch, MagicMock
from mps.analysis.dependency_analyzer import DependencyAnalyzer
from mps.packaging.package_builder import PackageBuilder
from mps.cross_references.cross_reference import CrossReference
from mps.database.database_manager import DatabaseManager

class TestMain(unittest.TestCase):
    @patch("builtins.input", side_effect=["1", "ruta/a/archivo.py", "7"])
    @patch("builtins.print")
    def test_analyze_dependencies_option(self, mock_print, mock_input):
        analyzer = DependencyAnalyzer()
        with patch.object(analyzer, "analyze", return_value=["modulo1", "modulo2"]):
            from mps.main import main
            main()
        mock_print.assert_any_call("Dependencias encontradas: ['modulo1', 'modulo2']")

    @patch("builtins.input", side_effect=["4", "localhost", "test_db", "user", "password", "7"])
    @patch("builtins.print")
    def test_connect_to_database(self, mock_print, mock_input):
        db_manager = DatabaseManager("localhost", "test_db", "user", "password")
        with patch.object(db_manager, "connect", return_value=None):
            from mps.main import main
            main()
        mock_print.assert_any_call("Conexión exitosa al servidor SQL.")

    @patch("builtins.input", side_effect=["5", "7"])
    @patch("builtins.print")
    def test_list_tables(self, mock_print, mock_input):
        db_manager = DatabaseManager("localhost", "test_db", "user", "password")
        with patch.object(db_manager, "list_tables", return_value=["tabla1", "tabla2"]):
            from mps.main import main
            main()
        mock_print.assert_any_call("Tablas en la base de datos:")
        mock_print.assert_any_call("- tabla1")
        mock_print.assert_any_call("- tabla2")

    @patch("builtins.input", side_effect=["6", "SELECT * FROM tabla1", "7"])
    @patch("builtins.print")
    def test_execute_query(self, mock_print, mock_input):
        db_manager = DatabaseManager("localhost", "test_db", "user", "password")
        with patch.object(db_manager, "execute_query", return_value=[("fila1",), ("fila2",)]):
            from mps.main import main
            main()
        mock_print.assert_any_call("Resultados de la consulta:")
        mock_print.assert_any_call(("fila1",))
        mock_print.assert_any_call(("fila2",))
