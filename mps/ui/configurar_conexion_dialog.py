from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QDialog, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import pyodbc

class ConfigurarConexionDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuración del Servidor")
        self.resize(1000, 1000)  # Tamaño inicial
        self.setMinimumSize(1000, 1000)  # Tamaño mínimo

        # Layout principal
        layout = QVBoxLayout(self)

        # Campos de entrada
        self.server_input = QLineEdit()
        self.server_input.setPlaceholderText("Servidor (IP o nombre)")
        layout.addWidget(QLabel("Servidor:"))
        layout.addWidget(self.server_input)

        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("Puerto")
        layout.addWidget(QLabel("Puerto:"))
        layout.addWidget(self.port_input)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuario")
        layout.addWidget(QLabel("Usuario:"))
        layout.addWidget(self.user_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(QLabel("Contraseña:"))
        layout.addWidget(self.password_input)

        # Indicador de estado de conexión
        self.connection_status_label = QLabel()
        self.connection_status_label.setPixmap(QPixmap("red_circle.png"))  # Imagen inicial (desconectado)
        layout.addWidget(QLabel("Estado de conexión:"))
        layout.addWidget(self.connection_status_label)

        # Botones
        button_layout = QHBoxLayout()

        self.test_button = QPushButton("Probar conexión")
        self.test_button.clicked.connect(self.test_connection)
        button_layout.addWidget(self.test_button)

        self.save_button = QPushButton("Guardar configuración")
        self.save_button.setEnabled(False)  # Deshabilitar el botón de guardar inicialmente
        button_layout.addWidget(self.save_button)

        self.cancel_button = QPushButton("Cancelar")
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

    def test_connection(self):
        """
        Prueba la conexión con los datos ingresados.
        """
        server = self.server_input.text().strip()
        port = self.port_input.text().strip()
        user = self.user_input.text().strip()
        password = self.password_input.text().strip()

        connection_string = (
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={server},{port};"
            f"UID={user};"
            f"PWD={password};"
            f"Encrypt=no;TrustServerCertificate=yes"
        )

        try:
            conn = pyodbc.connect(connection_string, timeout=5)
            conn.close()
            QMessageBox.information(self, "Éxito", "Conexión exitosa.")
            self.connection_status_label.setPixmap(QPixmap("green_circle.png"))  # Cambiar a conectado
            self.save_button.setEnabled(True)  # Habilitar el botón de guardar
        except pyodbc.Error as e:
            QMessageBox.critical(self, "Error", f"No se pudo conectar: {e}")
            self.connection_status_label.setPixmap(QPixmap("red_circle.png"))  # Cambiar a desconectado
            self.save_button.setEnabled(False)  # Deshabilitar el botón de guardar
