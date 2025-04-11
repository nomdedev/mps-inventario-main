from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QDialog
from mps.controllers.ordenes_controller import OrdenesController
from mps.services.session import Session
from mps.services.permissions import tiene_permiso
from mps.ui.ventana_con_estilo import VentanaConEstilo

class OrdenesWidget(VentanaConEstilo):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 600)

        # Layout principal
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # Tabla de órdenes
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Obra", "Fecha", "Estado", "Total Items"])
        layout.addWidget(self.table)

        # Botones de acción
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Crear Nueva Orden")
        self.add_button.clicked.connect(self.crear_orden)
        button_layout.addWidget(self.add_button)

        self.details_button = QPushButton("Ver Detalles")
        self.details_button.clicked.connect(self.ver_detalles)
        button_layout.addWidget(self.details_button)

        self.change_status_button = QPushButton("Cambiar Estado")
        self.change_status_button.clicked.connect(self.cambiar_estado)
        button_layout.addWidget(self.change_status_button)

        layout.addLayout(button_layout)

        # Cargar órdenes al iniciar
        self.cargar_ordenes()

    def cargar_ordenes(self):
        """
        Carga las órdenes en la tabla desde el controlador.
        """
        try:
            usuario_actual = Session.get_usuario_actual()
            if not tiene_permiso(usuario_actual.usuario, "ver_ordenes"):
                QMessageBox.warning(self, "Acceso Denegado", "No tiene permiso para ver órdenes.")
                return

            # Simulación de carga de órdenes
            ordenes = self.controller.obtener_ordenes_por_obra(1)  # Ejemplo con obra_id = 1
            self.table.setRowCount(0)

            for orden in ordenes:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem(str(orden.obra_id)))
                self.table.setItem(row_position, 1, QTableWidgetItem(orden.fecha))
                self.table.setItem(row_position, 2, QTableWidgetItem(orden.estado))
                self.table.setItem(row_position, 3, QTableWidgetItem(str(orden.total_items)))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar las órdenes: {e}")

    def crear_orden(self):
        """
        Abre un diálogo para crear una nueva orden.
        """
        QMessageBox.information(self, "Acción", "Función para crear nueva orden no implementada.")

    def ver_detalles(self):
        """
        Muestra los detalles de la orden seleccionada.
        """
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            orden_id = int(self.table.item(selected_row, 0).text())
            QMessageBox.information(self, "Acción", f"Función para ver detalles de la orden '{orden_id}' no implementada.")
        else:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar una orden para ver los detalles.")

    def cambiar_estado(self):
        """
        Cambia el estado de la orden seleccionada.
        """
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            orden_id = int(self.table.item(selected_row, 0).text())
            usuario_actual = Session.get_usuario_actual()
            if not tiene_permiso(usuario_actual.usuario, "cambiar_estado_orden"):
                QMessageBox.warning(self, "Acceso Denegado", "No tiene permiso para cambiar el estado de órdenes.")
                return
            QMessageBox.information(self, "Acción", f"Función para cambiar estado de la orden '{orden_id}' no implementada.")
        else:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar una orden para cambiar su estado.")
