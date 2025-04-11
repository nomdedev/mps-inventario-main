# Archivo para la interfaz gráfica de inicio de sesión.
# Contendrá la clase LoginWindow para manejar el login de usuarios.

from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLabel, QLineEdit, QPushButton, QWidget, QMessageBox
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import pyqtSignal, Qt, QCoreApplication
from mps.controllers.auth_controller import AuthController

class LoginWindow(QMainWindow):
    login_successful = pyqtSignal(object)  # Señal emitida cuando el login es exitoso

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(360, 640)  # Tamaño fijo
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # Eliminar bordes innecesarios

        # Centrar la ventana
        screen_geometry = QCoreApplication.instance().primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

        self.auth_controller = AuthController()

        # Configurar diseño
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap("mps/resources/logo.png")
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)

        # Nombre de la app
        app_name_label = QLabel("MPS Inventario")
        app_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        app_name_label.setStyleSheet("font-size: 20px; color: #555;")
        layout.addWidget(app_name_label)

        # Campos de usuario y contraseña
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuario")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        # Botón de inicio de sesión
        self.login_button = QPushButton("Iniciar sesión")
        self.login_button.setFixedWidth(200)
        self.login_button.clicked.connect(self.iniciar_sesion)

        # Agregar widgets al layout
        layout.addWidget(self.user_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setCentralWidget(central_widget)

    def iniciar_sesion(self):
        """
        Maneja el evento de clic en el botón de inicio de sesión.
        """
        username = self.user_input.text().strip()
        password = self.password_input.text().strip()

        if username and password:
            self.intentar_login(username, password)
        else:
            QMessageBox.warning(self, "Advertencia", "Por favor, complete todos los campos.")

    def intentar_login(self, usuario, contraseña):
        """
        Intenta autenticar al usuario con las credenciales proporcionadas.
        """
        try:
            usuario_actual = self.auth_controller.verificar_credenciales(usuario, contraseña)
            if usuario_actual:
                QMessageBox.information(self, "Éxito", "Inicio de sesión exitoso.")
                self.login_successful.emit({"id": usuario_actual[0], "username": usuario_actual[1], "role": usuario_actual[2]})
            else:
                QMessageBox.warning(self, "Error de Login", "Usuario o contraseña incorrectos.")
        except AttributeError as e:
            QMessageBox.critical(self, "Error", "Error en la configuración del logger. Verifique su implementación.")
            print(f"Error de logger: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al verificar las credenciales: {e}")
            print(f"Error inesperado: {e}")
