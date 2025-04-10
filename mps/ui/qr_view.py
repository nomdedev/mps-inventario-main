from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFileDialog, QMessageBox
from mps.controllers.qr_controller import QRController

class QRView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestión de Códigos QR")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.label = QLabel("Generar y Escanear Códigos QR")
        layout.addWidget(self.label)

        # Generar QR
        self.data_input = QLineEdit()
        self.data_input.setPlaceholderText("Ingrese los datos para el QR")
        layout.addWidget(self.data_input)

        self.generate_button = QPushButton("Generar QR")
        self.generate_button.clicked.connect(self.generar_qr)
        layout.addWidget(self.generate_button)

        # Escanear QR
        self.scan_button = QPushButton("Escanear QR desde imagen")
        self.scan_button.clicked.connect(self.escanear_qr)
        layout.addWidget(self.scan_button)

        self.result_label = QLabel("Resultado del escaneo: ")
        layout.addWidget(self.result_label)

        self.setLayout(layout)
        self.controller = QRController()

    def generar_qr(self):
        data = self.data_input.text()
        if data:
            output_path, _ = QFileDialog.getSaveFileName(self, "Guardar QR", "", "PNG Files (*.png)")
            if output_path:
                try:
                    self.controller.generar_qr(data, output_path)
                    QMessageBox.information(self, "Éxito", f"Código QR guardado en {output_path}")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error al generar el QR: {e}")
        else:
            QMessageBox.warning(self, "Advertencia", "Por favor, ingrese datos para generar el QR.")

    def escanear_qr(self):
        image_path, _ = QFileDialog.getOpenFileName(self, "Abrir imagen QR", "", "Image Files (*.png *.jpg *.jpeg)")
        if image_path:
            try:
                result = self.controller.escanear_qr(image_path)
                self.result_label.setText(f"Resultado del escaneo: {result}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al escanear el QR: {e}")
