import os
import requests
import subprocess
from PyQt6.QtWidgets import QMessageBox

APP_NAME = "MPS Inventario"
ICON_PATH = "icon.ico"
MAIN_SCRIPT = "main.py"
DIST_DIR = "dist/MPS Inventario/"
VERSION_FILE = "version.txt"
REMOTE_VERSION_URL = "https://raw.githubusercontent.com/usuario/repositorio/main/version.txt"
REMOTE_DOWNLOAD_URL = "https://github.com/usuario/repositorio/releases/latest/download/MPS_Inventario.exe"

def empaquetar_app():
    """
    Empaqueta la aplicación usando PyInstaller.
    """
    try:
        comando = [
            "pyinstaller",
            "--noconfirm",
            "--noconsole",
            f"--icon={ICON_PATH}",
            f"--name={APP_NAME}",
            MAIN_SCRIPT
        ]
        subprocess.run(comando, check=True)
        print(f"Aplicación empaquetada correctamente en {DIST_DIR}")
    except subprocess.CalledProcessError as e:
        print(f"Error al empaquetar la aplicación: {e}")

def verificar_actualizacion():
    """
    Verifica si hay una nueva versión disponible.
    """
    try:
        if not os.path.exists(VERSION_FILE):
            print("Archivo de versión local no encontrado.")
            return

        with open(VERSION_FILE, "r") as f:
            version_local = f.read().strip()

        response = requests.get(REMOTE_VERSION_URL)
        if response.status_code == 200:
            version_remota = response.text.strip()
            if version_remota > version_local:
                QMessageBox.information(None, "Actualización Disponible",
                                        f"Hay una nueva versión disponible: {version_remota}.")
                descargar_nueva_version()
            else:
                print("La aplicación está actualizada.")
        else:
            print("No se pudo verificar la versión remota.")
    except Exception as e:
        print(f"Error al verificar actualizaciones: {e}")

def descargar_nueva_version():
    """
    Descarga e instala la nueva versión de la aplicación.
    """
    try:
        response = requests.get(REMOTE_DOWNLOAD_URL, stream=True)
        if response.status_code == 200:
            nueva_version_path = os.path.join(DIST_DIR, "MPS_Inventario_Nueva.exe")
            with open(nueva_version_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
            print(f"Nueva versión descargada en {nueva_version_path}.")
            QMessageBox.information(None, "Actualización Completada",
                                    "La nueva versión ha sido descargada. Reinicie la aplicación para usarla.")
        else:
            print("Error al descargar la nueva versión.")
    except Exception as e:
        print(f"Error al descargar la nueva versión: {e}")
