from PyQt6.QtWidgets import QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
from mps.controllers.ordenes_controller import OrdenesController
from mps.ui.ventana_con_estilo import VentanaConEstilo

class OrdenesView(VentanaConEstilo):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 600)

        # Layout principal
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        self.label = QLabel("Órdenes de Compra")
        layout.addWidget(self.label)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.add_button = QPushButton("Agregar Orden")
        self.add_button.clicked.connect(self.agregar_orden)
        layout.addWidget(self.add_button)

        self.controller = OrdenesController()
        self.cargar_datos()

    def cargar_datos(self):
        try:
            ordenes = self.controller.listar_ordenes()
            self.table.setRowCount(len(ordenes))
            self.table.setColumnCount(4)  # ID, Fecha, Usuario, Total
            self.table.setHorizontalHeaderLabels(["ID", "Fecha", "Usuario", "Total"])
            for i, row in enumerate(ordenes):
                for j, value in enumerate(row):
                    self.table.setItem(i, j, QTableWidgetItem(str(value)))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar las órdenes: {e}")

    def agregar_orden(self):
        QMessageBox.information(self, "Agregar Orden", "Funcionalidad para agregar órdenes en desarrollo.")
