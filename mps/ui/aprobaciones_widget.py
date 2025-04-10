from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QLineEdit
from mps.controllers.aprobaciones_controller import AprobacionesController
from mps.services.session import Session
from mps.services.permissions import tiene_permiso

class AprobacionesWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Aprobaciones")
        self.controller = AprobacionesController()

        # Verificar permisos
        usuario_actual = Session.get_usuario_actual()
        if not tiene_permiso(usuario_actual.usuario, "ver_aprobaciones"):
            QMessageBox.warning(self, "Acceso Denegado", "No tiene permiso para acceder a las aprobaciones.")
            self.setDisabled(True)
            return

        # Layout principal
        layout = QVBoxLayout()

        # Tabla de solicitudes pendientes
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Tipo", "ID de Acción", "Solicitante", "Estado", "Fecha"])
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

        # Cargar solicitudes al iniciar
        self.cargar_solicitudes()

    def cargar_solicitudes(self):
        """
        Carga las solicitudes pendientes en la tabla desde el controlador.
        """
        try:
            solicitudes = self.controller.listar_pendientes()
            self.table.setRowCount(0)  # Limpiar la tabla

            for solicitud in solicitudes:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem(solicitud[1]))  # Tipo
                self.table.setItem(row_position, 1, QTableWidgetItem(str(solicitud[2])))  # ID de Acción
                self.table.setItem(row_position, 2, QTableWidgetItem(solicitud[3]))  # Solicitante
                self.table.setItem(row_position, 3, QTableWidgetItem(solicitud[4]))  # Estado
                self.table.setItem(row_position, 4, QTableWidgetItem(solicitud[5]))  # Fecha
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar las solicitudes: {e}")

    def aprobar_solicitud(self):
        """
        Aprueba la solicitud seleccionada.
        """
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            solicitud_id = int(self.table.item(selected_row, 1).text())
            usuario_actual = Session.get_usuario_actual().usuario
            try:
                self.controller.aprobar_solicitud(solicitud_id, usuario_actual)
                QMessageBox.information(self, "Éxito", "Solicitud aprobada correctamente.")
                self.cargar_solicitudes()
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
            solicitud_id = int(self.table.item(selected_row, 1).text())
            usuario_actual = Session.get_usuario_actual().usuario
            comentario, ok = QLineEdit.getText(self, "Rechazar Solicitud", "Ingrese un comentario:")
            if ok and comentario.strip():
                try:
                    self.controller.rechazar_solicitud(solicitud_id, usuario_actual, comentario.strip())
                    QMessageBox.information(self, "Éxito", "Solicitud rechazada correctamente.")
                    self.cargar_solicitudes()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error al rechazar la solicitud: {e}")
            else:
                QMessageBox.warning(self, "Advertencia", "Debe ingresar un comentario para rechazar la solicitud.")
        else:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar una solicitud para rechazar.")
