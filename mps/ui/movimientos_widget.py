from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox, QInputDialog
from mps.controllers.movimientos_controller import MovimientosController
from mps.ui.ventana_con_estilo import VentanaConEstilo

class MovimientosWidget(VentanaConEstilo):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Movimientos")
        self.setFixedSize(800, 600)
        self.controller = MovimientosController()

        # Layout principal
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # Tabla de movimientos
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Fecha", "Tipo", "Cantidad", "Usuario", "Obra", "Estado"])
        layout.addWidget(self.table)

        # Botón de filtrar
        button_layout = QHBoxLayout()
        self.filter_button = QPushButton("Filtrar por Material")
        self.filter_button.clicked.connect(self.filtrar_por_material)
        button_layout.addWidget(self.filter_button)
        layout.addLayout(button_layout)

    def cargar_movimientos(self, material_id=None):
        """
        Carga los movimientos en la tabla desde el controlador.
        :param material_id: ID del material para filtrar (opcional).
        """
        try:
            query = "SELECT fecha, tipo, cantidad, usuario, obra_id, estado FROM Movimientos"
            if material_id:
                query += " WHERE material_id = ?"
                movimientos = self.controller.db.ejecutar_query(query, [material_id])
            else:
                movimientos = self.controller.db.ejecutar_query(query)

            self.table.setRowCount(0)  # Limpiar la tabla

            for movimiento in movimientos:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem(movimiento[0]))  # Fecha
                self.table.setItem(row_position, 1, QTableWidgetItem(movimiento[1]))  # Tipo
                self.table.setItem(row_position, 2, QTableWidgetItem(str(movimiento[2])))  # Cantidad
                self.table.setItem(row_position, 3, QTableWidgetItem(movimiento[3]))  # Usuario
                self.table.setItem(row_position, 4, QTableWidgetItem(str(movimiento[4]) if movimiento[4] else "N/A"))  # Obra
                self.table.setItem(row_position, 5, QTableWidgetItem(movimiento[5]))  # Estado
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar los movimientos: {e}")

    def filtrar_por_material(self):
        """
        Filtra los movimientos por un material seleccionado.
        """
        material_id, ok = QInputDialog.getInt(self, "Filtrar por Material", "Ingrese el ID del material:")
        if ok:
            self.cargar_movimientos(material_id)
