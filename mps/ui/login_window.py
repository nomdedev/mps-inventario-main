import json
from PyQt6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QSpacerItem, QSizePolicy
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, pyqtSignal
from mps.ui.ventana_con_estilo import VentanaConEstilo
from mps.controllers.auth_controller import AuthController
from mps.ui.configurar_conexion_dialog import ConfigurarConexionDialog

CONFIG_PATH = './config/databaseConfig.json'

class LoginWindow(VentanaConEstilo):
    login_successful = pyqtSignal(object)  # Señal emitida cuando el login es exitoso

    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 600)

        # Asegurar que el fondo sea transparente
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Estilo del contenedor principal
        self.main_widget.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;  /* Fondo oscuro */
                border-radius: 15px;
            }
        """)

        self.auth_controller = AuthController()

        # Cargar configuración SQL
        self.config = self.load_config()
        if not self.config.get("server") or not self.config.get("user"):
            QMessageBox.warning(self, "Advertencia", "La conexión SQL no está configurada. Por favor, configúrela.")

        # Layout principal
        layout = QVBoxLayout(self.main_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(20, 20, 20, 20)

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap("mps/resources/logo.png")
        if not pixmap.isNull():
            logo_label.setPixmap(pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
        else:
            logo_label.setText("LOGO")
            logo_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #fff;")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)

        # Espaciador
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Título de la app
        app_name_label = QLabel("MPS Inventario")
        app_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        app_name_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #fff;")
        layout.addWidget(app_name_label)

        # Campos de usuario y contraseña
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuario")
        self.user_input.setFixedWidth(300)
        self.user_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.user_input.setStyleSheet("padding: 10px; border-radius: 10px; border: 1px solid #ccc; background-color: #333; color: #fff;")
        layout.addWidget(self.user_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedWidth(300)
        self.password_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.password_input.setStyleSheet("padding: 10px; border-radius: 10px; border: 1px solid #ccc; background-color: #333; color: #fff;")
        layout.addWidget(self.password_input)

        # Botón de inicio de sesión
        self.login_button = QPushButton("Iniciar sesión")
        self.login_button.setFixedWidth(300)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #0078d7;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
        """)
        self.login_button.clicked.connect(self.attempt_login)
        layout.addWidget(self.login_button)

        # Botón de configuración (opcional)
        self.config_button = QPushButton("Configurar conexión")
        self.config_button.setFixedWidth(300)
        self.config_button.setStyleSheet("""
            QPushButton {
                background-color: #f0f0f0;
                color: #555;
                font-size: 14px;
                padding: 10px;
                border-radius: 10px;
                border: 1px solid #ccc;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
        """)
        self.config_button.clicked.connect(self.open_config_dialog)
        layout.addWidget(self.config_button)

        # Espaciador
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

    def attempt_login(self):
        username = self.user_input.text().strip()
        password = self.password_input.text().strip()

        if username and password:
            try:
                usuario_actual = self.auth_controller.verificar_credenciales(username, password)
                if usuario_actual:
                    QMessageBox.information(self, "Éxito", "Inicio de sesión exitoso.")
                    self.login_successful.emit(usuario_actual)  # Emitir señal con el usuario actual
                else:
                    QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al intentar iniciar sesión: {e}")
        else:
            QMessageBox.warning(self, "Advertencia", "Por favor, complete todos los campos.")

    def open_config_dialog(self):
        dialog = ConfigurarConexionDialog()
        dialog.exec()

    def load_config(self):
        try:
            with open(CONFIG_PATH, 'r') as config_file:
                return json.load(config_file)
        except FileNotFoundError:
            return {}
