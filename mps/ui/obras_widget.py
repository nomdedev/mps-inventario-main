from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
from mps.controllers.obras_controller import ObrasController
from mps.services.session import Session
from mps.services.permissions import tiene_permiso
from mps.ui.ventana_con_estilo import VentanaConEstilo

class ObrasWidget(VentanaConEstilo):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Obras")
        self.setFixedSize(800, 600)
        self.controller = ObrasController()

        # Verificar permisos
        usuario_actual = Session.get_usuario_actual()
        if not tiene_permiso(usuario_actual.usuario, "ver_obras"):
            QMessageBox.warning(self, "Acceso Denegado", "No tiene permiso para acceder a las obras.")
            self.setDisabled(True)
            return

        # Layout principal
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # Tabla de obras
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Nombre", "Cliente", "Estado", "Fecha Inicio", "Fecha Fin"])
        layout.addWidget(self.table)

        # Botones de acción
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Agregar Obra")
        self.add_button.clicked.connect(self.agregar_obra)
        button_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Editar Obra")
        self.edit_button.clicked.connect(self.editar_obra)
        button_layout.addWidget(self.edit_button)

        self.finalize_button = QPushButton("Finalizar Obra")
        self.finalize_button.clicked.connect(self.finalizar_obra)
        button_layout.addWidget(self.finalize_button)

        self.view_materials_button = QPushButton("Ver Materiales Apartados")
        self.view_materials_button.clicked.connect(self.ver_materiales_apartados)
        button_layout.addWidget(self.view_materials_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Cargar obras al iniciar
        self.cargar_obras()

    def cargar_obras(self):
        """
        Carga las obras en la tabla desde el controlador.
        """
        try:
            obras = self.controller.listar_obras()
            self.table.setRowCount(0)  # Limpiar la tabla

            for obra in obras:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem(obra.nombre))
                self.table.setItem(row_position, 1, QTableWidgetItem(obra.cliente))
                self.table.setItem(row_position, 2, QTableWidgetItem(obra.estado))
                self.table.setItem(row_position, 3, QTableWidgetItem(obra.fecha_inicio))
                self.table.setItem(row_position, 4, QTableWidgetItem(obra.fecha_fin if obra.fecha_fin else "N/A"))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar las obras: {e}")

    def agregar_obra(self):
        """
        Abre un diálogo para agregar una nueva obra.
        """
        QMessageBox.information(self, "Acción", "Función para agregar obra no implementada.")

    def editar_obra(self):
        """
        Abre un diálogo para editar la obra seleccionada.
        """
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            obra_id = self.table.item(selected_row, 0).text()
            QMessageBox.information(self, "Acción", f"Función para editar obra '{obra_id}' no implementada.")
        else:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar una obra para editar.")

    def finalizar_obra(self):
        """
        Finaliza la obra seleccionada.
        """
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            obra_id = self.table.item(selected_row, 0).text()
            usuario_actual = Session.get_usuario_actual()
            if not tiene_permiso(usuario_actual.usuario, "finalizar_obra"):
                QMessageBox.warning(self, "Acceso Denegado", "No tiene permiso para finalizar obras.")
                return
            try:
                self.controller.finalizar_obra(obra_id)
                QMessageBox.information(self, "Éxito", "Obra finalizada correctamente.")
                self.cargar_obras()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al finalizar la obra: {e}")
        else:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar una obra para finalizar.")

    def ver_materiales_apartados(self):
        """
        Muestra los materiales apartados para la obra seleccionada.
        """
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            obra_id = self.table.item(selected_row, 0).text()
            QMessageBox.information(self, "Acción", f"Función para ver materiales apartados de la obra '{obra_id}' no implementada.")
        else:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar una obra para ver los materiales apartados.")
