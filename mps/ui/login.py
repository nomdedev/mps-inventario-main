# Archivo para la interfaz gráfica de inicio de sesión.
# Contendrá la clase LoginWindow para manejar el login de usuarios.

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import pyqtSignal
from mps.controllers.auth_controller import AuthController

class LoginWindow(QWidget):
    login_successful = pyqtSignal(dict)  # Señal emitida cuando el login es exitoso

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inicio de Sesión")
        self.setGeometry(100, 100, 300, 200)

        self.auth_controller = AuthController()

        layout = QVBoxLayout()

        # Etiqueta de instrucciones
        self.label = QLabel("Ingrese sus credenciales")
        layout.addWidget(self.label)

        # Campo de usuario
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")
        layout.addWidget(self.username_input)

        # Campo de contraseña
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        # Botón de inicio de sesión
        self.login_button = QPushButton("Ingresar")
        self.login_button.clicked.connect(self.iniciar_sesion)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def iniciar_sesion(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if username and password:
            try:
                usuario = self.auth_controller.verificar_credenciales(username, password)
                if usuario:
                    QMessageBox.information(self, "Éxito", "Inicio de sesión exitoso.")
                    self.login_successful.emit({"id": usuario[0], "username": usuario[1], "role": usuario[2]})
                else:
                    QMessageBox.warning(self, "Error", "Credenciales incorrectas.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al verificar las credenciales: {e}")
        else:
            QMessageBox.warning(self, "Advertencia", "Por favor, complete todos los campos.")
