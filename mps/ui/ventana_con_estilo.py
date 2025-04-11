from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QMouseEvent

class VentanaConEstilo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Contenedor interno con estilo
        self.main_widget = QWidget(self)
        self.main_widget.setStyleSheet("""
            QWidget {
                background-color: #1E1E1E;  /* Fondo oscuro */
                border-radius: 15px;
            }
        """)

        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.main_widget)

        # Aplicar estilo global si está disponible
        try:
            with open("mps/assets/styles/style.qss", "r") as style_file:
                self.setStyleSheet(style_file.read())
        except FileNotFoundError:
            print("Archivo de estilo no encontrado. Usando estilos predeterminados.")

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
