from PyQt6.QtWidgets import QVBoxLayout, QLabel, QComboBox, QPushButton, QFileDialog, QMessageBox
from mps.services.backup_manager import backup_todas
from mps.services.restore_manager import restaurar_base
from mps.ui.ventana_con_estilo import VentanaConEstilo

class RestoreDialog(VentanaConEstilo):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 200)

        # Layout principal
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # Selección de base de datos
        layout.addWidget(QLabel("Seleccione la base de datos a restaurar:"))
        self.base_combo = QComboBox()
        self.base_combo.addItems(["inventario", "users", "auditorias"])
        layout.addWidget(self.base_combo)

        # Botón para seleccionar archivo .bak
        self.select_file_button = QPushButton("Seleccionar archivo .bak")
        self.select_file_button.clicked.connect(self.seleccionar_archivo)
        layout.addWidget(self.select_file_button)

        # Mostrar ruta seleccionada
        self.selected_file_label = QLabel("Archivo seleccionado: Ninguno")
        layout.addWidget(self.selected_file_label)

        # Botón para restaurar
        self.restore_button = QPushButton("Restaurar")
        self.restore_button.clicked.connect(self.restaurar_base)
        layout.addWidget(self.restore_button)

        self.archivo_bak = None

    def seleccionar_archivo(self):
        """
        Abre un QFileDialog para seleccionar un archivo .bak.
        """
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo .bak", "", "Archivos .bak (*.bak)")
        if archivo:
            self.archivo_bak = archivo
            self.selected_file_label.setText(f"Archivo seleccionado: {archivo}")

    def restaurar_base(self):
        """
        Realiza el proceso de restauración de la base de datos seleccionada.
        """
        if not self.archivo_bak:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar un archivo .bak.")
            return

        nombre_base = self.base_combo.currentText()

        # Realizar backup antes de restaurar
        backups = backup_todas()
        if not backups:
            QMessageBox.warning(self, "Error", "No se pudieron realizar los backups previos. Restauración cancelada.")
            return

        # Restaurar la base de datos
        exito, mensaje = restaurar_base(nombre_base, self.archivo_bak)
        if exito:
            QMessageBox.information(self, "Éxito", mensaje)
            self.accept()  # Cerrar el diálogo
        else:
            QMessageBox.critical(self, "Error", mensaje)
