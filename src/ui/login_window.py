import json
import pyodbc
from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox, QDialog, QWidget, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from mps.ui.ventana_con_estilo import VentanaConEstilo

CONFIG_PATH = './config/databaseConfig.json'

class LoginWindow(VentanaConEstilo):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 600)

        # Layout principal
        layout = QVBoxLayout(self.main_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(20, 20, 20, 20)

        # Logo
        logo_label = QLabel()
        logo_label.setPixmap(QPixmap("mps/resources/logo.png").scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)

        # Espaciador
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Título de la app
        app_name_label = QLabel("MPS Inventario")
        app_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        app_name_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #555;")
        layout.addWidget(app_name_label)

        # Campos de usuario y contraseña
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuario")
        self.user_input.setFixedWidth(300)
        self.user_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.user_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedWidth(300)
        self.password_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.password_input)

        # Botón de inicio de sesión
        self.login_button = QPushButton("Iniciar sesión")
        self.login_button.setFixedWidth(300)
        self.login_button.clicked.connect(self.attempt_login)
        layout.addWidget(self.login_button)

        # Botón de configuración (opcional)
        self.config_button = QPushButton("Configurar conexión")
        self.config_button.setFixedWidth(300)
        self.config_button.clicked.connect(self.open_config_dialog)
        layout.addWidget(self.config_button)

        # Espaciador
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def attempt_login(self):
        try:
            config = self.load_config()
            self.test_user_database_connection(config)
            QMessageBox.information(self, "Éxito", "Conexión exitosa. Usuario autenticado.")
        except pyodbc.InterfaceError as e:
            QMessageBox.critical(self, "Error", f"Error de conexión: {e}")
            self.open_config_dialog()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {e}")

    def load_config(self):
        try:
            with open(CONFIG_PATH, 'r') as config_file:
                return json.load(config_file)
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", "Archivo de configuración no encontrado.")
            self.open_config_dialog()
            raise

    def test_user_database_connection(self, config):
        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={config['server']},{config['port']};"
            f"DATABASE={config['databases']['users']};"
            f"UID={config['user']};"
            f"PWD={config['password']}"
        )
        conn = pyodbc.connect(connection_string)
        conn.close()

    def open_config_dialog(self):
        dialog = ConfiguracionBDWidget(CONFIG_PATH)
        if dialog.exec_() == QDialog.Accepted:
            try:
                # Cargar la nueva configuración guardada
                config = self.load_config()
                # Probar la conexión con la nueva configuración
                self.test_user_database_connection(config)
                QMessageBox.information(self, "Éxito", "Conexión exitosa con la nueva configuración.")
            except pyodbc.InterfaceError as e:
                QMessageBox.critical(self, "Error", f"Error de conexión con la nueva configuración: {e}")
                self.open_config_dialog()  # Reabrir el diálogo si falla la conexión
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error inesperado: {e}")

    def fetch_data_in_batches(self, query, batch_size=1000):
        """
        Carga datos de la base de datos en lotes para mejorar el rendimiento.
        :param query: Consulta SQL a ejecutar.
        :param batch_size: Tamaño del lote.
        :return: Generador que devuelve los lotes de datos.
        """
        try:
            config = self.load_config()
            connection_string = (
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER={config['server']},{config['port']};"
                f"DATABASE={config['databases']['users']};"
                f"UID={config['user']};"
                f"PWD={config['password']}"
            )
            conn = pyodbc.connect(connection_string)
            cursor = conn.cursor()
            cursor.execute(query)

            while True:
                rows = cursor.fetchmany(batch_size)
                if not rows:
                    break
                yield rows

            cursor.close()
            conn.close()
        except pyodbc.Error as e:
            QMessageBox.critical(self, "Error", f"Error al cargar datos: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {e}")

    def process_data(self):
        """
        Ejemplo de procesamiento de datos en lotes.
        """
        query = "SELECT * FROM usuarios"  # Cambia esta consulta según tu base de datos
        for batch in self.fetch_data_in_batches(query):
            # Procesa cada lote de datos
            print(f"Procesando lote de {len(batch)} registros")
            # ... lógica para procesar los datos ...
