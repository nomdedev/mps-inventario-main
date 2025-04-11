import json
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt6.QtCore import Qt
from mps.ui.ventana_con_estilo import VentanaConEstilo

CONFIG_PATH = './config/databaseConfig.json'

class LoginWindow(VentanaConEstilo):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("MPS Inventario")

        # Crear y asignar un layout principal
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Campo de usuario
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuario")
        layout.addWidget(QLabel("Usuario:"))
        layout.addWidget(self.user_input)

        # Campo de contraseña
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel("Contraseña:"))
        layout.addWidget(self.password_input)

        # Botón para configurar el servidor
        self.config_button = QPushButton("Configurar conexión")
        self.config_button.clicked.connect(self.open_config_dialog)
        layout.addWidget(self.config_button)

    def open_config_dialog(self):
        """
        Abre la ventana de configuración del servidor.
        """
        from mps.ui.configurar_conexion_dialog import ConfigurarConexionDialog
        dialog = ConfigurarConexionDialog()
        dialog.exec()
