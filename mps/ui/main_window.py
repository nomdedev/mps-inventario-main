# Archivo para la ventana principal de la aplicación.
# Contendrá la clase MainWindow con un menú lateral y un QStackedWidget para cambiar entre módulos.

import sys
from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QWidget, QPushButton, QLabel, QStackedWidget, QMessageBox
from mps.services.session import Session
from mps.ui.inventario_view import InventarioView
from mps.ui.usuarios_view import UsuariosView
from mps.ui.obras_view import ObrasView
from mps.ui.ordenes_view import OrdenesView
from mps.ui.qr_view import QRView
from mps.ui.aprobaciones_view import AprobacionesView
from mps.ui.inventario_widget import InventarioWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MPS Inventario App")
        self.setGeometry(100, 100, 1000, 600)

        # Layout principal
        main_layout = QHBoxLayout()

        # Menú lateral
        menu_layout = QVBoxLayout()
        usuario_actual = Session.get_usuario_actual()
        self.menu_label = QLabel(f"Usuario: {usuario_actual.nombre} ({usuario_actual.rol})")
        self.menu_label.setStyleSheet("font-size: 14px; color: #457b9d;")
        menu_layout.addWidget(self.menu_label)

        self.inventario_button = QPushButton("Inventario")
        self.inventario_button.clicked.connect(self.mostrar_inventario)
        menu_layout.addWidget(self.inventario_button)

        self.usuarios_button = QPushButton("Usuarios")
        self.usuarios_button.clicked.connect(self.mostrar_usuarios)
        menu_layout.addWidget(self.usuarios_button)

        self.obras_button = QPushButton("Obras")
        self.obras_button.clicked.connect(self.mostrar_obras)
        menu_layout.addWidget(self.obras_button)

        self.ordenes_button = QPushButton("Órdenes")
        self.ordenes_button.clicked.connect(self.mostrar_ordenes)
        menu_layout.addWidget(self.ordenes_button)

        self.qr_button = QPushButton("QR")
        self.qr_button.clicked.connect(self.mostrar_qr)
        menu_layout.addWidget(self.qr_button)

        self.aprobaciones_button = QPushButton("Aprobaciones")
        self.aprobaciones_button.clicked.connect(self.mostrar_aprobaciones)
        menu_layout.addWidget(self.aprobaciones_button)

        # Mostrar u ocultar botones según el rol del usuario
        if usuario_actual.rol == "Operador":
            self.usuarios_button.hide()
            self.aprobaciones_button.hide()
        elif usuario_actual.rol == "Supervisor":
            self.usuarios_button.hide()
        # Admin tiene acceso a todo, no se oculta ningún botón

        # Contenido central
        self.stacked_widget = QStackedWidget()
        self.inventario_view = InventarioView()
        self.usuarios_view = UsuariosView()
        self.obras_view = ObrasView()
        self.ordenes_view = OrdenesView()
        self.qr_view = QRView()
        self.aprobaciones_view = AprobacionesView()
        self.inventario_widget = None  # Se cargará solo si el usuario tiene permiso

        self.stacked_widget.addWidget(self.inventario_view)
        self.stacked_widget.addWidget(self.usuarios_view)
        self.stacked_widget.addWidget(self.obras_view)
        self.stacked_widget.addWidget(self.ordenes_view)
        self.stacked_widget.addWidget(self.qr_view)
        self.stacked_widget.addWidget(self.aprobaciones_view)

        # Agregar el menú y el contenido al layout principal
        main_layout.addLayout(menu_layout)
        main_layout.addWidget(self.stacked_widget)

        # Configuración del widget central
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def mostrar_inventario(self):
        """
        Muestra el InventarioWidget en el panel central si el usuario tiene permiso.
        """
        if not Session.tiene_permiso(Session.get_usuario_actual(), "ver"):
            QMessageBox.warning(self, "Acceso Denegado", "No tiene permiso para acceder al inventario.")
            return

        if self.inventario_widget is None:
            self.inventario_widget = InventarioWidget()
            self.stacked_widget.addWidget(self.inventario_widget)

        self.stacked_widget.setCurrentWidget(self.inventario_widget)

    def mostrar_usuarios(self):
        self.stacked_widget.setCurrentWidget(self.usuarios_view)

    def mostrar_obras(self):
        self.stacked_widget.setCurrentWidget(self.obras_view)

    def mostrar_ordenes(self):
        self.stacked_widget.setCurrentWidget(self.ordenes_view)

    def mostrar_qr(self):
        self.stacked_widget.setCurrentWidget(self.qr_view)

    def mostrar_aprobaciones(self):
        self.stacked_widget.setCurrentWidget(self.aprobaciones_view)
