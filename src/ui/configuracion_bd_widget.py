import json
import pyodbc
from PyQt5.QtWidgets import (
    QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
)
from mps.ui.ventana_con_estilo import VentanaConEstilo

class ConfiguracionBDWidget(VentanaConEstilo):
    def __init__(self, config_path):
        super().__init__()
        self.config_path = config_path
        self.setFixedSize(400, 300)

        # Layout principal
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # Campos de entrada
        self.server_input = QLineEdit(self)
        self.server_input.setPlaceholderText("Servidor (ej: localhost\\SQLEXPRESS)")
        layout.addWidget(QLabel("Servidor:"))
        layout.addWidget(self.server_input)

        self.port_input = QLineEdit(self)
        self.port_input.setPlaceholderText("Puerto (opcional, default: 1433)")
        layout.addWidget(QLabel("Puerto:"))
        layout.addWidget(self.port_input)

        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText("Usuario")
        layout.addWidget(QLabel("Usuario:"))
        layout.addWidget(self.user_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Contraseña:"))
        layout.addWidget(self.password_input)

        self.inventario_input = QLineEdit(self)
        self.inventario_input.setPlaceholderText("Nombre de la base 'inventario'")
        layout.addWidget(QLabel("Base de datos 'inventario':"))
        layout.addWidget(self.inventario_input)

        self.users_input = QLineEdit(self)
        self.users_input.setPlaceholderText("Nombre de la base 'users'")
        layout.addWidget(QLabel("Base de datos 'users':"))
        layout.addWidget(self.users_input)

        self.auditorias_input = QLineEdit(self)
        self.auditorias_input.setPlaceholderText("Nombre de la base 'auditorias'")
        layout.addWidget(QLabel("Base de datos 'auditorias':"))
        layout.addWidget(self.auditorias_input)

        # Botones
        self.test_button = QPushButton("Probar conexión", self)
        self.test_button.clicked.connect(self.test_connection)
        layout.addWidget(self.test_button)

        self.save_button = QPushButton("Guardar configuración", self)
        self.save_button.clicked.connect(self.save_config)
        layout.addWidget(self.save_button)

    def test_connection(self):
        try:
            config = self.get_config_from_inputs()
            for db_name in config["databases"].values():
                connection_string = (
                    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                    f"SERVER={config['server']},{config['port']};"
                    f"DATABASE={db_name};"
                    f"UID={config['user']};"
                    f"PWD={config['password']}"
                )
                conn = pyodbc.connect(connection_string)
                conn.close()
            QMessageBox.information(self, "Éxito", "Conexión exitosa a todas las bases de datos.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al conectar: {e}")

    def save_config(self):
        try:
            config = self.get_config_from_inputs()
            with open(self.config_path, 'w') as config_file:
                json.dump(config, config_file, indent=2)
            QMessageBox.information(self, "Éxito", "Configuración guardada exitosamente.")
            self.accept()  # Cierra el diálogo y devuelve QDialog.Accepted
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar configuración: {e}")

    def get_config_from_inputs(self):
        return {
            "server": self.server_input.text(),
            "port": int(self.port_input.text()) if self.port_input.text() else 1433,
            "user": self.user_input.text(),
            "password": self.password_input.text(),
            "databases": {
                "inventario": self.inventario_input.text(),
                "users": self.users_input.text(),
                "auditorias": self.auditorias_input.text()
            }
        }
