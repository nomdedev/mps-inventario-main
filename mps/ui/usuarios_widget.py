from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
from mps.controllers.usuarios_controller import UsuariosController
from mps.services.session import Session
from mps.services.permissions import tiene_permiso
from mps.ui.ventana_con_estilo import VentanaConEstilo

class UsuariosWidget(VentanaConEstilo):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Usuarios")
        self.setFixedSize(800, 600)
        self.controller = UsuariosController()

        # Verificar permisos
        usuario_actual = Session.get_usuario_actual()
        if not tiene_permiso(usuario_actual.usuario, "ver_usuarios"):
            QMessageBox.warning(self, "Acceso Denegado", "No tiene permiso para acceder a la gestión de usuarios.")
            self.setDisabled(True)
            return

        # Layout principal
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # Tabla de usuarios
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Nombre", "Apellido", "Usuario", "Rol", "Activo"])
        layout.addWidget(self.table)

        # Botones de acción
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Agregar Usuario")
        self.add_button.clicked.connect(self.agregar_usuario)
        button_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Editar Usuario")
        self.edit_button.clicked.connect(self.editar_usuario)
        button_layout.addWidget(self.edit_button)

        self.change_role_button = QPushButton("Cambiar Rol")
        self.change_role_button.clicked.connect(self.cambiar_rol)
        button_layout.addWidget(self.change_role_button)

        self.toggle_active_button = QPushButton("Activar/Desactivar")
        self.toggle_active_button.clicked.connect(self.activar_desactivar_usuario)
        button_layout.addWidget(self.toggle_active_button)

        layout.addLayout(button_layout)

        # Cargar usuarios al iniciar
        self.cargar_usuarios()

    def cargar_usuarios(self):
        """
        Carga los usuarios en la tabla desde el controlador.
        """
        try:
            usuarios = self.controller.listar_usuarios()
            self.table.setRowCount(0)  # Limpiar la tabla

            for usuario in usuarios:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem(usuario.nombre))
                self.table.setItem(row_position, 1, QTableWidgetItem(usuario.apellido))
                self.table.setItem(row_position, 2, QTableWidgetItem(usuario.usuario))
                self.table.setItem(row_position, 3, QTableWidgetItem(usuario.rol))
                self.table.setItem(row_position, 4, QTableWidgetItem("Sí" if usuario.activo else "No"))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar los usuarios: {e}")

    def agregar_usuario(self):
        """
        Abre un diálogo para agregar un nuevo usuario.
        """
        QMessageBox.information(self, "Acción", "Función para agregar usuario no implementada.")

    def editar_usuario(self):
        """
        Abre un diálogo para editar el usuario seleccionado.
        """
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            usuario_id = self.table.item(selected_row, 2).text()
            QMessageBox.information(self, "Acción", f"Función para editar usuario '{usuario_id}' no implementada.")
        else:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar un usuario para editar.")

    def cambiar_rol(self):
        """
        Cambia el rol del usuario seleccionado.
        """
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            usuario_id = self.table.item(selected_row, 2).text()
            QMessageBox.information(self, "Acción", f"Función para cambiar rol del usuario '{usuario_id}' no implementada.")
        else:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar un usuario para cambiar su rol.")

    def activar_desactivar_usuario(self):
        """
        Activa o desactiva el usuario seleccionado.
        """
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            usuario_id = self.table.item(selected_row, 2).text()
            QMessageBox.information(self, "Acción", f"Función para activar/desactivar usuario '{usuario_id}' no implementada.")
        else:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar un usuario para activar/desactivar.")
