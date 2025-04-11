from PyQt6.QtWidgets import QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QPushButton, QLineEdit, QHBoxLayout
from mps.controllers.auditoria_controller import AuditoriaController
from mps.ui.ventana_con_estilo import VentanaConEstilo

class AuditoriaView(VentanaConEstilo):
    def __init__(self, usuario_actual):
        super().__init__()
        self.setFixedSize(800, 600)
        self.usuario_actual = usuario_actual

        # Layout principal
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        self.label = QLabel("Historial de Auditoría")
        layout.addWidget(self.label)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        if self.usuario_actual[2] == "Administrador":  # Solo admin puede aprobar/denegar
            action_layout = QHBoxLayout()
            self.razon_input = QLineEdit()
            self.razon_input.setPlaceholderText("Justificación para aprobar/denegar")
            action_layout.addWidget(self.razon_input)

            self.approve_button = QPushButton("Aprobar")
            self.approve_button.clicked.connect(self.aprobar_accion)
            action_layout.addWidget(self.approve_button)

            self.deny_button = QPushButton("Denegar")
            self.deny_button.clicked.connect(self.denegar_accion)
            action_layout.addWidget(self.deny_button)

            layout.addLayout(action_layout)

        self.controller = AuditoriaController()
        self.cargar_datos()

    def cargar_datos(self):
        try:
            auditoria = self.controller.listar_auditoria()
            self.table.setRowCount(len(auditoria))
            self.table.setColumnCount(4)  # Fecha, Usuario, Acción, Tabla Afectada
            self.table.setHorizontalHeaderLabels(["Fecha", "Usuario", "Acción", "Tabla Afectada"])
            for i, row in enumerate(auditoria):
                for j, value in enumerate(row):
                    self.table.setItem(i, j, QTableWidgetItem(str(value)))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar la auditoría: {e}")

    def aprobar_accion(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            auditoria_id = self.table.item(selected_row, 0).text()
            razon = self.razon_input.text()
            if razon:
                try:
                    self.controller.aprobar_accion(auditoria_id, self.usuario_actual[0], razon)
                    QMessageBox.information(self, "Éxito", "Acción aprobada correctamente.")
                    self.cargar_datos()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error al aprobar la acción: {e}")
            else:
                QMessageBox.warning(self, "Advertencia", "Debe proporcionar una justificación.")
        else:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar una acción para aprobar.")

    def denegar_accion(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            auditoria_id = self.table.item(selected_row, 0).text()
            razon = self.razon_input.text()
            if razon:
                try:
                    self.controller.denegar_accion(auditoria_id, self.usuario_actual[0], razon)
                    QMessageBox.information(self, "Éxito", "Acción denegada correctamente.")
                    self.cargar_datos()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error al denegar la acción: {e}")
            else:
                QMessageBox.warning(self, "Advertencia", "Debe proporcionar una justificación.")
        else:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar una acción para denegar.")
