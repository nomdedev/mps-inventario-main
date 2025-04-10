# Archivo para la ventana principal de la aplicación.
# Contendrá la clase MainWindow con un menú lateral y un QStackedWidget para cambiar entre módulos.

import sys
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QCoreApplication

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MPS Inventario")
        self.resize(1024, 768)  # Tamaño inicial

        # Centrar la ventana
        screen_geometry = QCoreApplication.instance().primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

        # Configurar diseño
        central_widget = QWidget()
        layout = QHBoxLayout(central_widget)

        # Menú lateral
        menu_layout = QVBoxLayout()
        menu_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        menu_layout.setContentsMargins(10, 10, 10, 10)

        # Logo o nombre de la app
        logo_label = QLabel()
        pixmap = QPixmap("mps/resources/logo.png")
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        menu_layout.addWidget(logo_label)

        # Botones del menú lateral
        botones = ["Dashboard", "Inventario", "Órdenes", "Aprobaciones", "Configuración"]
        for texto in botones:
            boton = QPushButton(texto)
            boton.setFixedWidth(200)
            menu_layout.addWidget(boton)

        # Agregar menú lateral al layout principal
        layout.addLayout(menu_layout)
        layout.addStretch()  # Espacio para el contenido principal

        self.setCentralWidget(central_widget)
