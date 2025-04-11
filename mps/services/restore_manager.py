import os
import subprocess

def restaurar_base(nombre_base: str, archivo_bak: str):
    """
    Restaura una base de datos desde un archivo .bak.
    :param nombre_base: Nombre de la base de datos a restaurar.
    :param archivo_bak: Ruta completa del archivo .bak.
    :return: (bool, str) Resultado de la operación y mensaje.
    """
    if not os.path.exists(archivo_bak):
        return False, f"El archivo {archivo_bak} no existe o no es accesible."

    try:
        # Comando para restaurar la base de datos
        comandos = [
            f"ALTER DATABASE [{nombre_base}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;",
            f"RESTORE DATABASE [{nombre_base}] FROM DISK = '{archivo_bak}' WITH REPLACE;",
            f"ALTER DATABASE [{nombre_base}] SET MULTI_USER;"
        ]
        comando_sql = " ".join(comandos)

        resultado = subprocess.run(
            ["sqlcmd", "-S", "localhost\\SQLEXPRESS", "-U", "sa", "-P", "mps.1887", "-Q", comando_sql],
            capture_output=True,
            text=True
        )

        if resultado.returncode == 0:
            return True, f"La base de datos '{nombre_base}' fue restaurada correctamente desde {archivo_bak}."
        else:
            return False, f"Error al restaurar la base '{nombre_base}': {resultado.stderr}"
    except Exception as e:
        return False, f"Error inesperado al restaurar la base '{nombre_base}': {e}"
