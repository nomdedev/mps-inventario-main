from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from cryptography.fernet import Fernet
import base64
import pyodbc
from mps.config.logging_config import get_logger

logger = get_logger(__name__)

class ConfiguracionBDWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuración de Base de Datos")
        layout = QVBoxLayout()

        # Campos de configuración
        self.server_input = QLineEdit()
        self.user_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.database_input = QLineEdit()

        layout.addWidget(QLabel("Servidor:"))
        layout.addWidget(self.server_input)
        layout.addWidget(QLabel("Usuario:"))
        layout.addWidget(self.user_input)
        layout.addWidget(QLabel("Contraseña:"))
        layout.addWidget(self.password_input)
        layout.addWidget(QLabel("Base de Datos:"))
        layout.addWidget(self.database_input)

        # Botón para guardar
        self.save_button = QPushButton("Guardar")
        self.save_button.clicked.connect(self.save_config)
        self.save_button.setEnabled(False)  # Deshabilitar el botón inicialmente
        layout.addWidget(self.save_button)

        self.server_input.textChanged.connect(self.validate_inputs)
        self.user_input.textChanged.connect(self.validate_inputs)
        self.password_input.textChanged.connect(self.validate_inputs)
        self.database_input.textChanged.connect(self.validate_inputs)

        self.setLayout(layout)

    def validate_inputs(self):
        # Habilitar el botón solo si todos los campos están llenos
        if all([self.server_input.text(), self.user_input.text(), self.password_input.text(), self.database_input.text()]):
            self.save_button.setEnabled(True)
        else:
            self.save_button.setEnabled(False)

    def save_config(self):
        server = self.server_input.text()
        user = self.user_input.text()
        password = self.password_input.text()
        database = self.database_input.text()

        if not all([server, user, password, database]):
            logger.warning("Intento de guardar configuración con campos incompletos.")
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios.")
            return

        # Validar conexión antes de guardar
        try:
            logger.info("Validando conexión con la configuración proporcionada...")
            connection_string = f"Server={server};User Id={user};Password={password};Database={database}"
            connection = pyodbc.connect(connection_string, timeout=5)
            connection.close()
            logger.info("Conexión validada exitosamente.")
        except Exception as e:
            logger.warning(f"Error al validar la conexión: {str(e)}")
            QMessageBox.warning(self, "Error", f"No se pudo conectar con la configuración proporcionada: {str(e)}")
            return

        # Cifrar la contraseña
        key = b'YOUR_SECRET_KEY_HERE'  # Usar la misma clave que en db_config.py
        fernet = Fernet(key)
        encrypted_password = base64.b64encode(fernet.encrypt(password.encode())).decode()

        # Guardar en .env
        try:
            with open(".env", "w") as env_file:
                env_file.write(f"DB_SERVER={server}\n")
                env_file.write(f"DB_USER={user}\n")
                env_file.write(f"DB_PASS={encrypted_password}\n")
                env_file.write(f"DB_NAME_INVENTARIO={database}\n")
            logger.info("Configuración guardada correctamente en .env.")
            QMessageBox.information(self, "Éxito", "Configuración guardada correctamente.")
        except Exception as e:
            logger.error(f"Error al guardar la configuración: {str(e)}")
            QMessageBox.critical(self, "Error", f"No se pudo guardar la configuración: {str(e)}")
