from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import json
import os

class DBConfigEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuración de Base de Datos")
        self.setFixedSize(400, 300)

        # Layout principal
        layout = QVBoxLayout(self)

        # Campos de configuración
        self.server_input = QLineEdit()
        self.server_input.setPlaceholderText("Servidor (IP o nombre)")
        layout.addWidget(QLabel("Servidor:"))
        layout.addWidget(self.server_input)

        self.instance_input = QLineEdit()
        self.instance_input.setPlaceholderText("Instancia (opcional)")
        layout.addWidget(QLabel("Instancia:"))
        layout.addWidget(self.instance_input)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Usuario")
        layout.addWidget(QLabel("Usuario:"))
        layout.addWidget(self.user_input)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Contraseña")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(QLabel("Contraseña:"))
        layout.addWidget(self.password_input)

        # Botones
        self.save_button = QPushButton("Guardar configuración")
        self.save_button.clicked.connect(self.guardar_configuracion)
        layout.addWidget(self.save_button)

        self.test_button = QPushButton("Probar conexión")
        self.test_button.clicked.connect(self.probar_conexion)
        layout.addWidget(self.test_button)

    def guardar_configuracion(self):
        """
        Guarda la configuración en un archivo JSON.
        """
        config = {
            "server": self.server_input.text().strip(),
            "instance": self.instance_input.text().strip(),
            "user": self.user_input.text().strip(),
            "password": self.password_input.text().strip()
        }
        try:
            with open("db_config.json", "w") as f:
                json.dump(config, f, indent=4)
            QMessageBox.information(self, "Éxito", "Configuración guardada correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar la configuración: {e}")

    def probar_conexion(self):
        """
        Prueba la conexión a la base de datos.
        """
        config = {
            "server": self.server_input.text().strip(),
            "instance": self.instance_input.text().strip(),
            "user": self.user_input.text().strip(),
            "password": self.password_input.text().strip()
        }
        try:
            # Simulación de prueba de conexión
            if config["server"] and config["user"] and config["password"]:
                QMessageBox.information(self, "Éxito", "Conexión exitosa.")
            else:
                raise ValueError("Faltan datos de configuración.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo conectar a la base de datos: {e}")
