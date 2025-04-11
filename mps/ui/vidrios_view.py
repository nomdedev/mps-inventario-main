from PyQt6.QtWidgets import QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QComboBox, QMessageBox
from mps.controllers.vidrios_controller import VidriosController
from mps.ui.ventana_con_estilo import VentanaConEstilo

class VidriosView(VentanaConEstilo):
    def __init__(self, usuario_actual):
        super().__init__()
        self.setFixedSize(800, 600)
        self.usuario_actual = usuario_actual

        # Layout principal
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        self.label = QLabel("Gestión de Vidrios por Obra")
        layout.addWidget(self.label)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        if self.usuario_actual[2] in ["Administrador", "Compras"]:  # Solo admin y compras pueden modificar
            self.estado_input = QComboBox()
            self.estado_input.addItems(["Pendiente", "Pedido", "Comprado", "Reposición"])
            layout.addWidget(self.estado_input)

            self.update_button = QPushButton("Actualizar Estado")
            self.update_button.clicked.connect(self.actualizar_estado)
            layout.addWidget(self.update_button)

        self.controller = VidriosController()
        self.cargar_datos()

    def cargar_datos(self):
        try:
            vidrios = self.controller.listar_vidrios()
            self.table.setRowCount(len(vidrios))
            self.table.setColumnCount(7)  # ID, Obra, Ancho, Alto, Tipología, Observaciones, Estado
            self.table.setHorizontalHeaderLabels(["ID", "Obra", "Ancho", "Alto", "Tipología", "Observaciones", "Estado"])
            for i, row in enumerate(vidrios):
                for j, value in enumerate(row):
                    self.table.setItem(i, j, QTableWidgetItem(str(value)))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar los vidrios: {e}")

    def actualizar_estado(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            vidrio_id = self.table.item(selected_row, 0).text()
            nuevo_estado = self.estado_input.currentText()
            try:
                self.controller.actualizar_estado(vidrio_id, nuevo_estado)
                QMessageBox.information(self, "Éxito", "Estado actualizado correctamente.")
                self.cargar_datos()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al actualizar el estado: {e}")
        else:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar un vidrio para actualizar el estado.")
