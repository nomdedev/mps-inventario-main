from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QInputDialog
from mps.controllers.aprobaciones_controller import AprobacionesController

class AprobacionesView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Aprobaciones")
        self.controller = AprobacionesController()

        # Layout principal
        layout = QVBoxLayout()

        # Tabla de aprobaciones pendientes
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["ID", "Tipo", "Referencia", "Solicitante"])
        layout.addWidget(self.table)

        # Botones de acción
        button_layout = QHBoxLayout()

        self.approve_button = QPushButton("Aprobar")
        self.approve_button.clicked.connect(self.aprobar_solicitud)
        button_layout.addWidget(self.approve_button)

        self.reject_button = QPushButton("Rechazar")
        self.reject_button.clicked.connect(self.rechazar_solicitud)
        button_layout.addWidget(self.reject_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Cargar aprobaciones al iniciar
        self.cargar_aprobaciones()

    def cargar_aprobaciones(self):
        """
        Carga las aprobaciones pendientes en la tabla desde el controlador.
        """
        try:
            aprobaciones = self.controller.listar_pendientes()
            self.table.setRowCount(0)  # Limpiar la tabla

            for aprobacion in aprobaciones:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem(str(aprobacion[0])))  # ID
                self.table.setItem(row_position, 1, QTableWidgetItem(aprobacion[1]))  # Tipo
                self.table.setItem(row_position, 2, QTableWidgetItem(str(aprobacion[2])))  # Referencia
                self.table.setItem(row_position, 3, QTableWidgetItem(aprobacion[3]))  # Solicitante
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar las aprobaciones: {e}")

    def aprobar_solicitud(self):
        """
        Aprueba la solicitud seleccionada.
        """
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            solicitud_id = int(self.table.item(selected_row, 0).text())
            try:
                comentario, ok = QInputDialog.getText(self, "Aprobar Solicitud", "Ingrese un comentario (opcional):")
                if ok:
                    self.controller.aprobar_solicitud(solicitud_id, "admin", comentario)
                    QMessageBox.information(self, "Éxito", "Solicitud aprobada correctamente.")
                    self.cargar_aprobaciones()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al aprobar la solicitud: {e}")
        else:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar una solicitud para aprobar.")

    def rechazar_solicitud(self):
        """
        Rechaza la solicitud seleccionada.
        """
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            solicitud_id = int(self.table.item(selected_row, 0).text())
            try:
                comentario, ok = QInputDialog.getText(self, "Rechazar Solicitud", "Ingrese un comentario:")
                if ok and comentario.strip():
                    self.controller.rechazar_solicitud(solicitud_id, "admin", comentario.strip())
                    QMessageBox.information(self, "Éxito", "Solicitud rechazada correctamente.")
                    self.cargar_aprobaciones()
                else:
                    QMessageBox.warning(self, "Advertencia", "Debe ingresar un comentario para rechazar la solicitud.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al rechazar la solicitud: {e}")
        else:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar una solicitud para rechazar.")
