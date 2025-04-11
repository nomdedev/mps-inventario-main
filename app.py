from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
import sys

class RoundedWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(400, 300)

        # Widget principal con estilo de bordes redondeados
        main_widget = QWidget(self)
        main_widget.setStyleSheet("""
            QWidget {
                background-color: #ffffff;
                border-radius: 15px;
            }
        """)

        # Layout principal
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(main_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RoundedWindow()
    window.show()
    sys.exit(app.exec())
