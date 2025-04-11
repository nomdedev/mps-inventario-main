import os
from datetime import datetime
import subprocess

BACKUP_FOLDER = "backups"

def generar_nombre_backup(nombre_base):
    """
    Genera el nombre del archivo de backup con la fecha y hora actual.
    :param nombre_base: Nombre de la base de datos.
    :return: Ruta completa del archivo de backup.
    """
    if not os.path.exists(BACKUP_FOLDER):
        os.makedirs(BACKUP_FOLDER)
    fecha_hora = datetime.now().strftime("%Y-%m-%d_%H-%M")
    return os.path.join(BACKUP_FOLDER, f"{nombre_base}_{fecha_hora}.bak")

def backup_base(nombre_base):
    """
    Realiza un backup de la base de datos especificada.
    :param nombre_base: Nombre de la base de datos.
    """
    try:
        ruta_backup = generar_nombre_backup(nombre_base)
        comando = [
            "sqlcmd",
            "-S", "localhost\\SQLEXPRESS",
            "-U", "sa",
            "-P", "mps.1887",
            "-Q", f"BACKUP DATABASE [{nombre_base}] TO DISK='{ruta_backup}'"
        ]
        resultado = subprocess.run(comando, capture_output=True, text=True)
        if resultado.returncode == 0:
            print(f"Backup de la base '{nombre_base}' realizado correctamente en: {ruta_backup}")
            return ruta_backup
        else:
            print(f"Error al realizar el backup de la base '{nombre_base}': {resultado.stderr}")
            return None
    except Exception as e:
        print(f"Error inesperado al realizar el backup de la base '{nombre_base}': {e}")
        return None

def backup_todas():
    """
    Realiza un backup de todas las bases de datos (inventario, users, auditorias).
    """
    bases = ["inventario", "users", "auditorias"]
    backups_realizados = []
    for base in bases:
        ruta_backup = backup_base(base)
        if ruta_backup:
            backups_realizados.append(ruta_backup)
    if backups_realizados:
        print("Backups realizados correctamente:")
        for ruta in backups_realizados:
            print(f"- {ruta}")
    else:
        print("No se pudieron realizar los backups.")
    return backups_realizados
