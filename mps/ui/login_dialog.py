from PyQt6.QtWidgets import QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from mps.controllers.usuarios_controller import UsuariosController
from mps.controllers.auditoria_controller import AuditoriaController
from mps.ui.ventana_con_estilo import VentanaConEstilo

class LoginDialog(VentanaConEstilo):
    def __init__(self):
        super().__init__()
        self.setFixedSize(360, 640)

        self.controller = UsuariosController()
        self.auditoria_controller = AuditoriaController()  # Controlador de auditoría

        # Layout principal
        layout = QVBoxLayout(self.main_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(20, 20, 20, 20)

        # Espacio para el logo
        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setPixmap(QPixmap("mps/assets/images/logo.png").scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio))
        layout.addWidget(self.logo_label)

        # Espaciador
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        # Etiqueta de instrucciones
        self.label = QLabel("Ingrese sus credenciales")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("font-size: 16px; color: #457b9d;")
        layout.addWidget(self.label)

        # Campo de usuario
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Usuario")
        self.username_input.setStyleSheet("padding: 10px; font-size: 14px;")
        layout.addWidget(self.username_input)

        # Campo de contraseña
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("padding: 10px; font-size: 14px;")
        layout.addWidget(self.password_input)

        # Botón de inicio de sesión
        self.login_button = QPushButton("Iniciar Sesión")
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #457b9d;
                color: white;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2a9d8f;
            }
        """)
        self.login_button.clicked.connect(self.iniciar_sesion)
        layout.addWidget(self.login_button)

        # Espaciador
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))

        self.usuario_actual = None

    def iniciar_sesion(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if username and password:
            try:
                print("Conectando al servidor...")
                self.controller.conectar_servidor()

                print("Conectando a la base de datos 'usuarios'...")
                self.controller.conectar_base_datos("usuarios")
                print("Conexión a la base de datos 'usuarios' establecida.")

                print(f"Verificando credenciales para el usuario: {username}")
                usuario = self.controller.verificar_credenciales(username, password)

                if usuario:
                    print(f"Usuario autenticado: {usuario}")
                    self.usuario_actual = usuario

                    print("Conectando a la base de datos 'inventario'...")
                    self.controller.conectar_base_datos("inventario")
                    print("Conexión a la base de datos 'inventario' establecida.")

                    self.auditoria_controller.registrar_accion(
                        usuario_id=usuario[0],
                        accion="Inicio de sesión",
                        tabla_afectada="usuarios"
                    )
                    self.accept()
                else:
                    QMessageBox.warning(self, "Error", "Credenciales incorrectas.")
            except Exception as e:
                print(f"Error durante el inicio de sesión: {e}")
                QMessageBox.critical(self, "Error", f"Error al verificar las credenciales: {e}")
        else:
            QMessageBox.warning(self, "Advertencia", "Por favor, complete todos los campos.")
