from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem
from mps.controllers.dashboard_controller import DashboardController
from mps.services.session import Session
from mps.utils.exporter import exportar_dashboard
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mps.ui.ventana_con_estilo import VentanaConEstilo

class DashboardWidget(VentanaConEstilo):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 600)
        self.controller = DashboardController()
        self.usuario_actual = Session.get_usuario_actual()

        # Layout principal
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # Panel superior con KPIs
        self.kpi_layout = QHBoxLayout()
        self.label_total_materiales = QLabel("Total Materiales: 0")
        self.label_stock_total = QLabel("Stock Disponible: 0")
        self.label_obras_activas = QLabel("Obras Activas: 0")
        self.label_ordenes_pendientes = QLabel("Órdenes Pendientes: 0")
        self.kpi_layout.addWidget(self.label_total_materiales)
        self.kpi_layout.addWidget(self.label_stock_total)
        self.kpi_layout.addWidget(self.label_obras_activas)
        self.kpi_layout.addWidget(self.label_ordenes_pendientes)
        layout.addLayout(self.kpi_layout)

        # Gráfica de torta
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Tabla de entregas recientes
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Obra", "Usuario", "Fecha"])
        layout.addWidget(self.table)

        # Botón refrescar
        self.refresh_button = QPushButton("Refrescar")
        self.refresh_button.clicked.connect(self.cargar_datos)
        layout.addWidget(self.refresh_button)

        # Botón exportar
        self.export_button = QPushButton("Exportar Dashboard")
        self.export_button.clicked.connect(self.exportar_dashboard)
        layout.addWidget(self.export_button)

        self.cargar_datos()

    def cargar_datos(self):
        """
        Carga los datos del dashboard desde el controlador.
        """
        try:
            totales = self.controller.obtener_totales()
            self.label_total_materiales.setText(f"Total Materiales: {totales['total_materiales']}")
            self.label_stock_total.setText(f"Stock Disponible: {totales['stock_total']}")
            self.label_obras_activas.setText(f"Obras Activas: {totales['obras_activas']}")
            self.label_ordenes_pendientes.setText(f"Órdenes Pendientes: {totales['ordenes_pendientes']}")

            etapas = self.controller.obtener_etapas_obras()
            self.mostrar_grafica_etapas(etapas)

            entregas = self.controller.obtener_entregas_recientes()
            self.table.setRowCount(0)
            for entrega in entregas:
                row_position = self.table.rowCount()
                self.table.insertRow(row_position)
                self.table.setItem(row_position, 0, QTableWidgetItem(entrega["obra"]))
                self.table.setItem(row_position, 1, QTableWidgetItem(entrega["usuario"]))
                self.table.setItem(row_position, 2, QTableWidgetItem(entrega["fecha"]))
        except Exception as e:
            print(f"Error al cargar datos del dashboard: {e}")

    def mostrar_grafica_etapas(self, etapas):
        """
        Muestra una gráfica de torta con las etapas de las obras.
        """
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        labels = etapas.keys()
        sizes = etapas.values()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        self.canvas.draw()

    def exportar_dashboard(self):
        """
        Exporta el dashboard a un archivo PDF.
        """
        try:
            totales = self.controller.obtener_totales()
            entregas = self.controller.obtener_entregas_recientes()
            datos = {
                "totales": totales,
                "entregas": entregas
            }
            ruta = exportar_dashboard(self.usuario_actual.usuario, datos)
            print(f"Dashboard exportado a: {ruta}")
        except Exception as e:
            print(f"Error al exportar el dashboard: {e}")
