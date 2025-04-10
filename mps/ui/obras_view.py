from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit
from mps.controllers.obras_controller import ObrasController

class ObrasView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Obras")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()
        self.label = QLabel("Obras del Sistema")
        layout.addWidget(self.label)

        self.table = QTableWidget()
        layout.addWidget(self.table)

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre de la obra")
        layout.addWidget(self.nombre_input)

        self.cliente_input = QLineEdit()
        self.cliente_input.setPlaceholderText("Cliente asociado")
        layout.addWidget(self.cliente_input)

        self.add_button = QPushButton("Agregar Obra")
        self.add_button.clicked.connect(self.agregar_obra)
        layout.addWidget(self.add_button)

        self.setLayout(layout)
        self.controller = ObrasController()
        self.cargar_datos()

    def cargar_datos(self):
        try:
            obras = self.controller.listar_obras()
            self.table.setRowCount(len(obras))
            self.table.setColumnCount(len(obras[0]))
            self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Cliente"])
            for i, row in enumerate(obras):
                for j, value in enumerate(row):
                    self.table.setItem(i, j, QTableWidgetItem(str(value)))
        except Exception as e:
            self.label.setText(f"Error al cargar las obras: {e}")

    def agregar_obra(self):
        nombre = self.nombre_input.text()
        cliente = self.cliente_input.text()
        if nombre and cliente:
            try:
                self.controller.agregar_obra(nombre, cliente)
                self.cargar_datos()
                self.nombre_input.clear()
                self.cliente_input.clear()
            except Exception as e:
                self.label.setText(f"Error al agregar la obra: {e}")
