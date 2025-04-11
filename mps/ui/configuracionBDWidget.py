from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton
import pyodbc

class ConfiguracionBDWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Layout principal
        main_layout = QVBoxLayout(self)

        # Layout para el campo de servidor
        servidor_layout = QHBoxLayout()
        servidor_label = QLabel("Servidor:")
        servidor_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        servidor_layout.addWidget(servidor_label)

        self.leServidor = QLineEdit(self)
        servidor_layout.addWidget(self.leServidor)

        self.lblStatus = QLabel(self)
        self.lblStatus.setFixedSize(24, 24)
        servidor_layout.addWidget(self.lblStatus)

        main_layout.addLayout(servidor_layout)

        # Campo de usuario
        usuario_layout = QHBoxLayout()
        usuario_label = QLabel("Usuario:")
        usuario_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        usuario_layout.addWidget(usuario_label)

        self.leUsuario = QLineEdit(self)
        usuario_layout.addWidget(self.leUsuario)
        main_layout.addLayout(usuario_layout)

        # Campo de contraseña
        contrasena_layout = QHBoxLayout()
        contrasena_label = QLabel("Contraseña:")
        contrasena_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        contrasena_layout.addWidget(contrasena_label)

        self.leContrasena = QLineEdit(self)
        self.leContrasena.setEchoMode(QLineEdit.EchoMode.Password)
        contrasena_layout.addWidget(self.leContrasena)
        main_layout.addLayout(contrasena_layout)

        # Botón de guardar
        self.btnGuardar = QPushButton("Guardar configuración", self)
        self.btnGuardar.setEnabled(False)
        main_layout.addWidget(self.btnGuardar)

        # Conectar señales
        self.leServidor.textChanged.connect(self._on_text_changed)
        self.leUsuario.textChanged.connect(self._on_text_changed)
        self.leContrasena.textChanged.connect(self._on_text_changed)

        # Timer para verificar conexión
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._on_timer_timeout)

    def _on_text_changed(self):
        self.timer.start(500)

    def _on_timer_timeout(self):
        self.timer.stop()
        self.verificar_conexion_en_tiempo_real()

    def verificar_conexion_en_tiempo_real(self):
        servidor = self.leServidor.text()
        usuario = self.leUsuario.text()
        contrasena = self.leContrasena.text()
        try:
            con_str = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={servidor};DATABASE=master;UID={usuario};PWD={contrasena};"
            pyodbc.connect(con_str, timeout=2).close()
            self.lblStatus.setPixmap(QPixmap('check.png'))
            self.btnGuardar.setEnabled(True)
        except pyodbc.Error:
            self.lblStatus.setPixmap(QPixmap('error.png'))
            self.btnGuardar.setEnabled(False)