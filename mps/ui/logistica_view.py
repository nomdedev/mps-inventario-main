from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QDateEdit, QMessageBox
from mps.controllers.logistica_controller import LogisticaController

class LogisticaView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Logística")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        self.label = QLabel("Logística de Obras")
        layout.addWidget(self.label)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.obra_input = QLineEdit()
        self.obra_input.setPlaceholderText("ID de la obra")
        layout.addWidget(self.obra_input)

        self.fecha_entrega_input = QDateEdit()
        self.fecha_entrega_input.setCalendarPopup(True)
        layout.addWidget(self.fecha_entrega_input)

        self.estado_input = QLineEdit()
        self.estado_input.setPlaceholderText("Estado (Confirmada, Pendiente, etc.)")
        layout.addWidget(self.estado_input)

        self.add_button = QPushButton("Agregar Logística")
        self.add_button.clicked.connect(self.agregar_logistica)
        layout.addWidget(self.add_button)

        self.setLayout(layout)
        self.controller = LogisticaController()
        self.cargar_datos()

    def cargar_datos(self):
        try:
            logistica = self.controller.listar_logistica()
            self.table.setRowCount(len(logistica))
            self.table.setColumnCount(4)  # ID, Obra, Fecha de Entrega, Estado
            self.table.setHorizontalHeaderLabels(["ID", "Obra", "Fecha de Entrega", "Estado"])
            for i, row in enumerate(logistica):
                for j, value in enumerate(row):
                    self.table.setItem(i, j, QTableWidgetItem(str(value)))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar la logística: {e}")

    def agregar_logistica(self):
        obra_id = self.obra_input.text()
        fecha_entrega = self.fecha_entrega_input.text()
        estado = self.estado_input.text()
        if obra_id and fecha_entrega and estado:
            try:
                self.controller.agregar_logistica(obra_id, fecha_entrega, estado)
                self.cargar_datos()
                self.obra_input.clear()
                self.estado_input.clear()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al agregar la logística: {e}")
