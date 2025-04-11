from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QWidget
from PyQt6.QtCore import Qt
import json
import pyodbc

CONFIG_PATH = './config/databaseConfig.json'

class ConfigurarConexionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(500, 500)  # Aumentar el tamaño del diálogo

        # Contenedor interno con estilo
        self.main_widget = QWidget(self)
        self.main_widget.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;
                border-radius: 15px;
            }
        """)

        # Layout principal
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # Campos de entrada
        self.server_input = QLineEdit()
        self.server_input.setPlaceholderText("Servidor (ej: DESKTOP-G3CQERD\\SQLEXPRESS)")
        layout.addWidget(QLabel("Servidor:"))
        layout.addWidget(self.server_input)

        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("Puerto (default: 1433)")
        layout.addWidget(QLabel("Puerto:"))
        layout.addWidget(self.port_input)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuario")
        layout.addWidget(QLabel("Usuario:"))
        layout.addWidget(self.user_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel("Contraseña:"))
        layout.addWidget(self.password_input)

        self.auth_mode_input = QLineEdit()
        self.auth_mode_input.setPlaceholderText("Modo de autenticación (ej: SQL Server Authentication)")
        layout.addWidget(QLabel("Modo de Autenticación:"))
        layout.addWidget(self.auth_mode_input)

        self.encryption_input = QLineEdit()
        self.encryption_input.setPlaceholderText("Cifrado (ej: Optional)")
        layout.addWidget(QLabel("Cifrado:"))
        layout.addWidget(self.encryption_input)

        self.trust_cert_input = QLineEdit()
        self.trust_cert_input.setPlaceholderText("Confiar en el certificado (ej: True o False)")
        layout.addWidget(QLabel("Confiar en el Certificado:"))
        layout.addWidget(self.trust_cert_input)

        # Botones
        self.test_button = QPushButton("Probar Conexión")
        self.test_button.clicked.connect(self.test_connection)
        layout.addWidget(self.test_button)

        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.save_config)
        layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        layout.addWidget(self.cancel_button)

        # Cargar configuración existente
        self.load_config()

    def load_config(self):
        try:
            with open(CONFIG_PATH, 'r') as config_file:
                config = json.load(config_file)
                self.server_input.setText(config.get("server", "DESKTOP-G3CQERD\\SQLEXPRESS"))
                self.port_input.setText(str(config.get("port", 1433)))
                self.user_input.setText(config.get("user", "sa"))
                self.password_input.setText(config.get("password", "mps1887"))
                self.auth_mode_input.setText(config.get("auth_mode", "SQL Server Authentication"))
                self.encryption_input.setText(config.get("encryption", "Optional"))
                self.trust_cert_input.setText(config.get("trust_cert", "True"))
        except FileNotFoundError:
            pass  # No hay configuración previa

    def save_config(self):
        config = {
            "server": self.server_input.text().strip(),
            "port": int(self.port_input.text().strip()) if self.port_input.text().strip().isdigit() else 1433,
            "user": self.user_input.text().strip(),
            "password": self.password_input.text().strip(),
            "auth_mode": self.auth_mode_input.text().strip(),
            "encryption": self.encryption_input.text().strip(),
            "trust_cert": self.trust_cert_input.text().strip()
        }
        try:
            with open(CONFIG_PATH, 'w') as config_file:
                json.dump(config, config_file, indent=4)
            QMessageBox.information(self, "Éxito", "Configuración guardada correctamente.")
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar la configuración: {e}")

    def test_connection(self):
        server = self.server_input.text().strip()
        port = self.port_input.text().strip()
        user = self.user_input.text().strip()
        password = self.password_input.text().strip()

        if not server or not port or not user or not password:
            QMessageBox.warning(self, "Advertencia", "Todos los campos son obligatorios para probar la conexión.")
            return

        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server},{port};"
            f"UID={user};"
            f"PWD={password};"
            f"Encrypt={self.encryption_input.text().strip()};"
            f"TrustServerCertificate={self.trust_cert_input.text().strip()}"
        )
        try:
            conn = pyodbc.connect(connection_string, timeout=5)
            conn.close()
            QMessageBox.information(self, "Éxito", "Conexión exitosa.")
        except pyodbc.InterfaceError:
            QMessageBox.critical(self, "Error", "No se pudo conectar al servidor. Verifique el servidor y el puerto.")
        except pyodbc.OperationalError:
            QMessageBox.critical(self, "Error", "Credenciales incorrectas. Verifique el usuario y la contraseña.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error inesperado: {e}")
