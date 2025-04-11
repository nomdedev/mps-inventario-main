# Archivo para la ventana principal de la aplicación.
# Contendrá la clase MainWindow con un menú lateral y un QStackedWidget para cambiar entre módulos.

import sys
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QHBoxLayout, QMessageBox, QFrame
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QCoreApplication, QFile, QTextStream
from mps.services.backup_manager import backup_todas
from mps.ui.restore_dialog import RestoreDialog
from mps.ui.ventana_con_estilo import VentanaConEstilo

class MainWindow(VentanaConEstilo):
    def __init__(self, usuario_actual):
        super().__init__()
        self.resize(1024, 768)

        # Layout principal
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Header con botones personalizados
        header = QHBoxLayout()
        minimize_button = QPushButton("–")
        minimize_button.clicked.connect(self.showMinimized)
        maximize_button = QPushButton("□")
        maximize_button.clicked.connect(self.showMaximized)
        close_button = QPushButton("X")
        close_button.setStyleSheet("color: red; font-weight: bold;")
        close_button.clicked.connect(self.close)
        header.addWidget(minimize_button)
        header.addWidget(maximize_button)
        header.addWidget(close_button)
        layout.addLayout(header)

        # Centrar la ventana
        screen_geometry = QCoreApplication.instance().primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

        # Configurar diseño
        central_layout = QHBoxLayout(self.main_widget)

        # Menú lateral (sidebar)
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebar")
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)

        # Logo o nombre de la app
        logo_label = QLabel()
        pixmap = QPixmap("mps/resources/logo.png")
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(logo_label)

        # Botones del menú lateral
        botones = ["Dashboard", "Inventario", "Órdenes", "Aprobaciones", "Configuración"]
        for texto in botones:
            boton = QPushButton(texto)
            boton.setFixedWidth(200)
            boton.setObjectName("menuButton")  # Aplicar estilo desde style.qss
            sidebar_layout.addWidget(boton)

        # Botón para backup manual
        self.backup_button = QPushButton("Backup Manual")
        self.backup_button.setObjectName("menuButton")  # Aplicar estilo desde style.qss
        self.backup_button.clicked.connect(self.realizar_backup_manual)
        sidebar_layout.addWidget(self.backup_button)

        # Botón para restaurar base de datos (solo admin)
        if usuario_actual["role"] == "admin":
            self.restore_button = QPushButton("Restaurar base desde backup")
            self.restore_button.setObjectName("menuButton")  # Aplicar estilo desde style.qss
            self.restore_button.clicked.connect(self.abrir_restore_dialog)
            sidebar_layout.addWidget(self.restore_button)

        # Agregar sidebar al layout principal
        central_layout.addWidget(self.sidebar)
        central_layout.addStretch()  # Espacio para el contenido principal

        self.setCentralWidget(self.main_widget)

    def cargar_estilo_global(self):
        """
        Carga la hoja de estilo global desde el archivo style.qss.
        """
        try:
            file = QFile("mps/assets/styles/style.qss")
            if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
                stream = QTextStream(file)
                stylesheet = stream.readAll()
                self.setStyleSheet(stylesheet)
                print("Hoja de estilo cargada correctamente.")
            else:
                print("Advertencia: No se pudo abrir el archivo style.qss.")
        except Exception as e:
            print(f"Error al cargar el archivo de estilos: {e}")

    def realizar_backup_manual(self):
        """
        Realiza un backup manual de todas las bases de datos.
        """
        try:
            backups = backup_todas()
            if backups:
                QMessageBox.information(self, "Backup Exitoso", f"Backups realizados:\n" + "\n".join(backups))
            else:
                QMessageBox.warning(self, "Backup Fallido", "No se pudieron realizar los backups.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al realizar el backup: {e}")

    def abrir_restore_dialog(self):
        """
        Abre el diálogo para restaurar una base de datos.
        """
        dialog = RestoreDialog()
        if dialog.exec():
            QMessageBox.information(self, "Sesión cerrada", "La base de datos fue restaurada. Por favor, vuelva a iniciar sesión.")
            self.close()  # Cerrar la ventana principal para forzar reconexión

    def closeEvent(self, event):
        """
        Sobrescribe el evento de cierre para realizar backups automáticos.
        """
        try:
            backups = backup_todas()
            if backups:
                QMessageBox.information(self, "Backup Automático", "Se realizó backup automático antes de cerrar.")
            else:
                QMessageBox.warning(self, "Backup Fallido", "No se pudo realizar el backup automático.")
        except Exception as e:
            print(f"Error al realizar el backup automático: {e}")
        event.accept()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
