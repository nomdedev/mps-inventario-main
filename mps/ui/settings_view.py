from PyQt6.QtWidgets import QVBoxLayout, QLabel, QPushButton, QColorDialog, QMessageBox
from mps.config.design_config import DESIGN_CONFIG
from mps.config.theme_manager import generate_theme
from mps.ui.ventana_con_estilo import VentanaConEstilo

class SettingsView(VentanaConEstilo):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 400)

        # Layout principal
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        self.label = QLabel("Configuración de la Aplicación")
        layout.addWidget(self.label)

        self.change_theme_button = QPushButton("Cambiar Color Base del Tema")
        self.change_theme_button.clicked.connect(self.cambiar_tema)
        layout.addWidget(self.change_theme_button)

    def cambiar_tema(self):
        color = QColorDialog.getColor()
        if color.isValid():
            base_color = color.name()
            try:
                new_theme = generate_theme(base_color)
                DESIGN_CONFIG.update(new_theme)
                QMessageBox.information(self, "Éxito", "El tema se ha actualizado correctamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al actualizar el tema: {e}")
