from PyQt6.QtWidgets import QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QMessageBox
from mps.controllers.usuarios_controller import UsuariosController
from mps.ui.ventana_con_estilo import VentanaConEstilo

class UsuariosView(VentanaConEstilo):
    def __init__(self, usuario_actual):
        super().__init__()
        self.setFixedSize(800, 600)
        self.usuario_actual = usuario_actual  # Usuario actual

        # Layout principal
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        self.label = QLabel("Usuarios del Sistema")
        layout.addWidget(self.label)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        if self.usuario_actual == "admin":  # Solo admin puede gestionar usuarios
            self.nombre_input = QLineEdit()
            self.nombre_input.setPlaceholderText("Nombre del usuario")
            layout.addWidget(self.nombre_input)

            self.rol_input = QLineEdit()
            self.rol_input.setPlaceholderText("Rol del usuario")
            layout.addWidget(self.rol_input)

            self.add_button = QPushButton("Agregar Usuario")
            self.add_button.clicked.connect(self.agregar_usuario)
            layout.addWidget(self.add_button)

            self.edit_button = QPushButton("Editar Usuario")
            self.edit_button.clicked.connect(self.editar_usuario)
            layout.addWidget(self.edit_button)

            self.delete_button = QPushButton("Eliminar Usuario")
            self.delete_button.clicked.connect(self.eliminar_usuario)
            layout.addWidget(self.delete_button)

        self.controller = UsuariosController()
        self.cargar_datos()

    def cargar_datos(self):
        try:
            usuarios = self.controller.listar_usuarios()
            self.table.setRowCount(len(usuarios))
            self.table.setColumnCount(len(usuarios[0]))
            self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Rol"])
            for i, row in enumerate(usuarios):
                for j, value in enumerate(row):
                    self.table.setItem(i, j, QTableWidgetItem(str(value)))
        except Exception as e:
            self.label.setText(f"Error al cargar los usuarios: {e}")

    def agregar_usuario(self):
        nombre = self.nombre_input.text()
        rol = self.rol_input.text()
        if nombre and rol:
            try:
                self.controller.agregar_usuario(nombre, rol)
                self.cargar_datos()
                self.nombre_input.clear()
                self.rol_input.clear()
            except Exception as e:
                self.label.setText(f"Error al agregar el usuario: {e}")

    def editar_usuario(self):
        QMessageBox.information(self, "Editar Usuario", "Funcionalidad para editar usuarios en desarrollo.")

    def eliminar_usuario(self):
        QMessageBox.information(self, "Eliminar Usuario", "Funcionalidad para eliminar usuarios en desarrollo.")
