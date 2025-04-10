from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QTabWidget, QLabel, QLineEdit, QCheckBox, QMessageBox
from mps.controllers.estado_obra_controller import EstadoObraController
from mps.controllers.pedidos_controller import PedidosController
from mps.services.auditoria import registrar_auditoria
from mps.utils.exporter import exportar_materiales_obra, exportar_checklist_final

class LogisticaWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Logística")
        self.estado_controller = EstadoObraController()
        self.pedidos_controller = PedidosController()

        # Layout principal
        layout = QVBoxLayout()

        # Tabla de obras activas
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Nombre", "Cliente"])
        self.table.itemSelectionChanged.connect(self.cargar_etapas)
        layout.addWidget(self.table)

        # Tabs para las etapas
        self.tabs = QTabWidget()
        self.tabs.addTab(self.crear_tab_medicion(), "Medición")
        self.tabs.addTab(self.crear_tab_fabricacion(), "Fabricación")
        self.tabs.addTab(self.crear_tab_colocacion(), "Colocación")
        layout.addWidget(self.tabs)

        # Botón para exportar a Excel
        self.export_button = QPushButton("Exportar a Excel")
        self.export_button.clicked.connect(self.exportar_materiales)
        layout.addWidget(self.export_button)

        self.setLayout(layout)
        self.cargar_obras()

    def cargar_obras(self):
        """
        Carga las obras activas en la tabla.
        """
        try:
            obras = self.estado_controller.listar_obras_activas()
            self.table.setRowCount(0)
            for obra in obras:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem(str(obra.id)))
                self.table.setItem(row_position, 1, QTableWidgetItem(obra.nombre))
                self.table.setItem(row_position, 2, QTableWidgetItem(obra.cliente))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar las obras: {e}")

    def cargar_etapas(self):
        """
        Carga las etapas de la obra seleccionada.
        """
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            obra_id = int(self.table.item(selected_row, 0).text())
            self.tabs.setEnabled(True)
            self.cargar_tab_medicion(obra_id)
            self.cargar_tab_fabricacion(obra_id)
            self.cargar_tab_colocacion(obra_id)
        else:
            self.tabs.setEnabled(False)

    def crear_tab_medicion(self):
        """
        Crea el tab para la etapa de medición.
        """
        tab = QWidget()
        layout = QVBoxLayout()

        self.medicion_observaciones = QLineEdit()
        self.medicion_observaciones.setPlaceholderText("Observaciones")
        layout.addWidget(QLabel("Observaciones:"))
        layout.addWidget(self.medicion_observaciones)

        self.generar_pedido_button = QPushButton("Generar Pedido de Material")
        self.generar_pedido_button.clicked.connect(self.generar_pedido_medicion)
        layout.addWidget(self.generar_pedido_button)

        tab.setLayout(layout)
        return tab

    def cargar_tab_medicion(self, obra_id):
        """
        Carga los datos de la etapa de medición para la obra seleccionada.
        """
        # Aquí se podrían cargar observaciones previas o datos relacionados.

    def generar_pedido_medicion(self):
        """
        Genera un pedido de material para la etapa de medición.
        """
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            obra_id = int(self.table.item(selected_row, 0).text())
            observaciones = self.medicion_observaciones.text().strip()
            try:
                self.pedidos_controller.generar_pedido(obra_id, "medicion", [])
                registrar_auditoria("admin", "Logística", "Generar Pedido", f"Obra ID: {obra_id}, Etapa: Medición")
                QMessageBox.information(self, "Éxito", "Pedido de material generado correctamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al generar el pedido: {e}")
        else:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar una obra para generar el pedido.")

    def crear_tab_fabricacion(self):
        """
        Crea el tab para la etapa de fabricación.
        """
        tab = QWidget()
        layout = QVBoxLayout()

        self.fabricacion_checkbox = QCheckBox("Confirmar Pedido")
        layout.addWidget(self.fabricacion_checkbox)

        self.confirmar_pedido_button = QPushButton("Confirmar Pedido")
        self.confirmar_pedido_button.clicked.connect(self.confirmar_pedido_fabricacion)
        layout.addWidget(self.confirmar_pedido_button)

        tab.setLayout(layout)
        return tab

    def cargar_tab_fabricacion(self, obra_id):
        """
        Carga los datos de la etapa de fabricación para la obra seleccionada.
        """
        # Aquí se podrían cargar datos del pedido actual.

    def confirmar_pedido_fabricacion(self):
        """
        Confirma el pedido de la etapa de fabricación.
        """
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            obra_id = int(self.table.item(selected_row, 0).text())
            try:
                self.pedidos_controller.confirmar_pedido(obra_id)
                registrar_auditoria("admin", "Logística", "Confirmar Pedido", f"Obra ID: {obra_id}, Etapa: Fabricación")
                QMessageBox.information(self, "Éxito", "Pedido confirmado correctamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al confirmar el pedido: {e}")
        else:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar una obra para confirmar el pedido.")

    def crear_tab_colocacion(self):
        """
        Crea el tab para la etapa de colocación.
        """
        tab = QWidget()
        layout = QVBoxLayout()

        self.colocacion_fecha = QLineEdit()
        self.colocacion_fecha.setPlaceholderText("Fecha de instalación")
        layout.addWidget(QLabel("Fecha de instalación:"))
        layout.addWidget(self.colocacion_fecha)

        self.finalizar_obra_button = QPushButton("Finalizar Obra")
        self.finalizar_obra_button.clicked.connect(self.finalizar_obra)
        layout.addWidget(self.finalizar_obra_button)

        tab.setLayout(layout)
        return tab

    def cargar_tab_colocacion(self, obra_id):
        """
        Carga los datos de la etapa de colocación para la obra seleccionada.
        """
        # Aquí se podrían cargar datos relacionados con la instalación.

    def finalizar_obra(self):
        """
        Finaliza la obra seleccionada.
        """
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            obra_id = int(self.table.item(selected_row, 0).text())
            fecha_instalacion = self.colocacion_fecha.text().strip()
            try:
                self.estado_controller.finalizar_obra(obra_id, fecha_instalacion)
                registrar_auditoria("admin", "Logística", "Finalizar Obra", f"Obra ID: {obra_id}, Fecha: {fecha_instalacion}")
                QMessageBox.information(self, "Éxito", "Obra finalizada correctamente.")
                self.cargar_obras()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al finalizar la obra: {e}")
        else:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar una obra para finalizar.")

    def exportar_materiales(self):
        """
        Exporta los materiales apartados de la obra seleccionada a un archivo Excel.
        """
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            obra_id = int(self.table.item(selected_row, 0).text())
            try:
                # Simulación de datos de materiales apartados
                materiales = [
                    {"codigo": "MAT001", "descripcion": "Material A", "cantidad": 10, "fecha_apartado": "2023-10-01", "usuario": "admin"},
                    {"codigo": "MAT002", "descripcion": "Material B", "cantidad": 5, "fecha_apartado": "2023-10-02", "usuario": "admin"}
                ]
                ruta = exportar_materiales_obra(obra_id, materiales)
                QMessageBox.information(self, "Éxito", f"Materiales exportados a: {ruta}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al exportar materiales: {e}")
        else:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar una obra para exportar los materiales.")
