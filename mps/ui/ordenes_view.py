from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QMessageBox
from mps.controllers.ordenes_controller import OrdenesController

class OrdenesView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Órdenes de Compra")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.label = QLabel("Órdenes de Compra")
        layout.addWidget(self.label)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.add_button = QPushButton("Agregar Orden")
        self.add_button.clicked.connect(self.agregar_orden)
        layout.addWidget(self.add_button)

        self.setLayout(layout)
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
