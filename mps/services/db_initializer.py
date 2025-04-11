import subprocess
import os

def verificar_y_crear_bases():
    """
    Verifica la conexión a las bases de datos y las crea si no existen.
    """
    try:
        print("Verificando bases de datos...")
        resultado = subprocess.run(
            ["sqlcmd", "-S", "localhost\\SQLEXPRESS", "-U", "sa", "-P", "mps.1887", "-i", "setup_db.sql"],
            capture_output=True,
            text=True
        )
        if resultado.returncode == 0:
            print("Bases de datos verificadas/creadas correctamente.")
        else:
            print(f"Error al ejecutar setup_db.sql: {resultado.stderr}")
    except FileNotFoundError:
        print("ERROR: SQLCMD no está instalado o no está en el PATH.")
