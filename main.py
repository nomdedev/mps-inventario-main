import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QFile, QTextStream
from mps.ui.login import LoginWindow
from mps.ui.main_window import MainWindow
from mps.config.design_config import DESIGN_CONFIG

def load_stylesheet(app):
    """
    Carga la hoja de estilo global desde el archivo style.qss.
    """
    try:
        file = QFile("mps/assets/styles/style.qss")
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            stylesheet = stream.readAll()
            app.setStyleSheet(stylesheet)
            print("Hoja de estilo cargada correctamente.")
        else:
            print("Advertencia: No se pudo abrir el archivo style.qss.")
    except Exception as e:
        print(f"Error al cargar el archivo de estilos: {e}")

def main():
    try:
        print("Iniciando la aplicación...")  # Confirmación de inicio
        app = QApplication(sys.argv)
        load_stylesheet(app)

        # Crear instancia de LoginWindow
        login_window = LoginWindow()
        main_window = None

        def on_login_successful(usuario_actual):
            """
            Maneja el evento de login exitoso.
            Oculta la ventana de login y muestra la ventana principal.
            """
            nonlocal main_window
            print(f"Usuario autenticado: {usuario_actual}")
            login_window.hide()
            main_window = MainWindow(usuario_actual)
            main_window.show()

        # Conectar la señal de login exitoso
        login_window.login_successful.connect(on_login_successful)

        # Mostrar la ventana de login
        login_window.show()

        sys.exit(app.exec())
    except Exception as e:
        # Manejar excepciones globales y mostrar un mensaje de error
        error_message = f"Se produjo un error inesperado: {e}"
        print(error_message)
        QMessageBox.critical(None, "Error Crítico", error_message)
        raise

if __name__ == "__main__":
    main()
