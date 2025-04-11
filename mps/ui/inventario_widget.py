from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QMessageBox
from mps.controllers.inventario_controller import InventarioController
from mps.models.material import Material
from mps.services.auditoria import registrar_auditoria
from mps.services.session import Session
from mps.ui.ventana_con_estilo import VentanaConEstilo

class InventarioWidget(VentanaConEstilo):
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 600)

        # Layout principal
        layout = QVBoxLayout(self.main_widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # Tabla de materiales
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["ID", "Código", "Descripción", "Largo (mm)", "Stock Total", "Stock Disponible", "Stock Apartado"])
        layout.addWidget(self.table)

        # Botones de acción
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Agregar")
        self.add_button.clicked.connect(self.agregar_material)
        button_layout.addWidget(self.add_button)

        self.edit_button = QPushButton("Editar")
        self.edit_button.clicked.connect(self.editar_material)
        button_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton("Eliminar")
        self.delete_button.clicked.connect(self.eliminar_material)
        button_layout.addWidget(self.delete_button)

        self.entry_button = QPushButton("Registrar Entrada")
        self.entry_button.clicked.connect(self.registrar_entrada)
        button_layout.addWidget(self.entry_button)

        self.exit_button = QPushButton("Registrar Salida")
        self.exit_button.clicked.connect(self.registrar_salida)
        button_layout.addWidget(self.exit_button)

        self.apartar_button = QPushButton("Apartar")
        self.apartar_button.clicked.connect(self.apartar_material)
        button_layout.addWidget(self.apartar_button)

        layout.addLayout(button_layout)

        # Cargar datos iniciales
        self.cargar_datos()

    def cargar_datos(self):
        """
        Carga los materiales en la tabla desde el controlador.
        """
        try:
            materiales = self.controller.listar_materiales()
            self.table.setRowCount(len(materiales))
            for i, material in enumerate(materiales):
                self.table.setItem(i, 0, QTableWidgetItem(str(material.id)))
                self.table.setItem(i, 1, QTableWidgetItem(material.codigo))
                self.table.setItem(i, 2, QTableWidgetItem(material.descripcion))
                self.table.setItem(i, 3, QTableWidgetItem(str(material.largo_mm)))
                self.table.setItem(i, 4, QTableWidgetItem(str(material.stock_total)))
                self.table.setItem(i, 5, QTableWidgetItem(str(material.stock_disponible)))
                self.table.setItem(i, 6, QTableWidgetItem(str(material.stock_apartado)))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al cargar los materiales: {e}")

    def agregar_material(self):
        """
        Abre un diálogo para agregar un nuevo material.
        """
        # Aquí se implementaría un QDialog para capturar los datos del nuevo material.
        QMessageBox.information(self, "Acción", "Función para agregar material no implementada.")
        # Simulación de agregar material
        try:
            material = Material(0, "COD123", "Material de prueba", 1000, 50, 50, 0)
            self.controller.agregar_material(material)
            registrar_auditoria(Session.get_usuario_actual().nombre, "Inventario", "Agregar Material", f"Material: {material.descripcion}")
            self.cargar_datos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al agregar el material: {e}")

    def editar_material(self):
        """
        Abre un diálogo para editar el material seleccionado.
        """
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            material_id = int(self.table.item(selected_row, 0).text())
            # Aquí se implementaría un QDialog para editar el material.
            QMessageBox.information(self, "Acción", f"Función para editar material ID {material_id} no implementada.")
            # Simulación de edición
            try:
                nuevos_datos = {"codigo": "COD456", "descripcion": "Material Editado", "largo_mm": 1200, "stock_total": 60, "stock_disponible": 60, "stock_apartado": 0}
                self.controller.editar_material(material_id, nuevos_datos)
                registrar_auditoria(Session.get_usuario_actual().nombre, "Inventario", "Editar Material", f"ID: {material_id}, Nuevos Datos: {nuevos_datos}")
                self.cargar_datos()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al editar el material: {e}")
        else:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar un material para editar.")

    def eliminar_material(self):
        """
        Elimina el material seleccionado.
        """
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            material_id = int(self.table.item(selected_row, 0).text())
            try:
                self.controller.eliminar_material(material_id)
                registrar_auditoria(Session.get_usuario_actual().nombre, "Inventario", "Eliminar Material", f"ID: {material_id}")
                QMessageBox.information(self, "Éxito", "Material eliminado correctamente.")
                self.cargar_datos()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al eliminar el material: {e}")
        else:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar un material para eliminar.")

    def registrar_entrada(self):
        """
        Registra una entrada de stock para el material seleccionado.
        """
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            material_id = int(self.table.item(selected_row, 0).text())
            # Aquí se implementaría un QDialog para capturar la cantidad de entrada.
            QMessageBox.information(self, "Acción", f"Función para registrar entrada en material ID {material_id} no implementada.")
            # Simulación de entrada
            try:
                cantidad = 10
                self.controller.registrar_entrada(material_id, cantidad)
                registrar_auditoria(Session.get_usuario_actual().nombre, "Inventario", "Registrar Entrada", f"ID: {material_id}, Cantidad: {cantidad}")
                self.cargar_datos()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al registrar la entrada: {e}")
        else:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar un material para registrar entrada.")

    def registrar_salida(self):
        """
        Registra una salida de stock para el material seleccionado.
        """
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            material_id = int(self.table.item(selected_row, 0).text())
            # Aquí se implementaría un QDialog para capturar la cantidad de salida.
            QMessageBox.information(self, "Acción", f"Función para registrar salida en material ID {material_id} no implementada.")
            # Simulación de salida
            try:
                cantidad = 5
                self.controller.registrar_salida(material_id, cantidad)
                registrar_auditoria(Session.get_usuario_actual().nombre, "Inventario", "Registrar Salida", f"ID: {material_id}, Cantidad: {cantidad}")
                self.cargar_datos()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al registrar la salida: {e}")
        else:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar un material para registrar salida.")

    def apartar_material(self):
        """
        Aparta una cantidad de material para una obra específica.
        """
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            material_id = int(self.table.item(selected_row, 0).text())
            # Aquí se implementaría un QDialog para capturar la cantidad y la obra.
            QMessageBox.information(self, "Acción", f"Función para apartar material ID {material_id} no implementada.")
            # Simulación de apartado
            try:
                cantidad = 3
                obra = "Obra A"
                self.controller.apartar_material(material_id, cantidad, obra)
                registrar_auditoria(Session.get_usuario_actual().nombre, "Inventario", "Apartar Material", f"ID: {material_id}, Cantidad: {cantidad}, Obra: {obra}")
                self.cargar_datos()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al apartar el material: {e}")
        else:
            QMessageBox.warning(self, "Advertencia", "Debe seleccionar un material para apartar.")
