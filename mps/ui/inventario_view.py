from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QLineEdit, QHBoxLayout, QMessageBox
)
from mps.controllers.inventario_controller import InventarioController

class InventarioView(QWidget):
    def __init__(self, usuario_actual):
        super().__init__()
        self.setWindowTitle("Inventario")
        self.setGeometry(100, 100, 800, 600)
        self.usuario_actual = usuario_actual  # Usuario actual

        # Layout principal
        layout = QVBoxLayout()

        # Título
        self.label = QLabel("Inventario Actual")
        layout.addWidget(self.label)

        # Tabla de inventario
        self.table = QTableWidget()
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)  # Tabla de solo lectura por defecto
        layout.addWidget(self.table)

        # Filtros
        filter_layout = QHBoxLayout()
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Buscar por descripción o código")
        self.filter_button = QPushButton("Filtrar")
        self.filter_button.clicked.connect(self.filtrar_inventario)
        filter_layout.addWidget(self.filter_input)
        filter_layout.addWidget(self.filter_button)
        layout.addLayout(filter_layout)

        # Botones de acciones (solo para admin)
        if self.usuario_actual == "admin":
            button_layout = QHBoxLayout()
            self.add_button = QPushButton("Agregar Ítem")
            self.add_button.clicked.connect(self.agregar_item)
            self.edit_button = QPushButton("Editar Ítem")
            self.edit_button.clicked.connect(self.editar_item)
            self.delete_button = QPushButton("Eliminar Ítem")
            self.delete_button.clicked.connect(self.eliminar_item)
            self.apartar_button = QPushButton("Apartar Stock")
            self.ingresar_button = QPushButton("Ingresar Stock")
            self.pedido_button = QPushButton("Hacer Pedido")
            button_layout.addWidget(self.add_button)
            button_layout.addWidget(self.edit_button)
            button_layout.addWidget(self.delete_button)
            button_layout.addWidget(self.apartar_button)
            button_layout.addWidget(self.ingresar_button)
            button_layout.addWidget(self.pedido_button)
            layout.addLayout(button_layout)

        # Total de inventario
        self.total_label = QLabel("Total de ítems: 0")
        layout.addWidget(self.total_label)

        self.setLayout(layout)
        self.controller = InventarioController()
        self.cargar_datos()

    def cargar_datos(self):
        try:
            inventario = self.controller.listar_inventario()
            self.table.setRowCount(len(inventario))
            self.table.setColumnCount(5)  # Código, Descripción, Stock Actual, Apartado, Observaciones
            self.table.setHorizontalHeaderLabels(["Código", "Descripción", "Stock Actual", "Apartado", "Observaciones"])
            for i, row in enumerate(inventario):
                self.table.setItem(i, 0, QTableWidgetItem(row[0]))  # Código (xxxxxx.xxx)
                self.table.setItem(i, 1, QTableWidgetItem(row[1]))  # Descripción (nombre del perfil)
                self.table.setItem(i, 2, QTableWidgetItem(str(row[2] or 0)))  # Stock Actual
                self.table.setItem(i, 3, QTableWidgetItem(str(row[3] or 0)))  # Apartado
                self.table.setItem(i, 4, QTableWidgetItem(row[4] or ""))  # Observaciones
            self.total_label.setText(f"Total de ítems: {len(inventario)}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar el inventario: {e}")

    def filtrar_inventario(self):
        filtro = self.filter_input.text()
        if filtro:
            try:
                inventario = self.controller.filtrar_inventario(filtro)
                self.table.setRowCount(len(inventario))
                for i, row in enumerate(inventario):
                    for j, value in enumerate(row):
                        self.table.setItem(i, j, QTableWidgetItem(str(value)))
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al filtrar el inventario: {e}")

    def agregar_item(self):
        QMessageBox.information(self, "Agregar Ítem", "Funcionalidad para agregar ítems en desarrollo.")

    def editar_item(self):
        QMessageBox.information(self, "Editar Ítem", "Funcionalidad para editar ítems en desarrollo.")

    def eliminar_item(self):
        QMessageBox.information(self, "Eliminar Ítem", "Funcionalidad para eliminar ítems en desarrollo.")
