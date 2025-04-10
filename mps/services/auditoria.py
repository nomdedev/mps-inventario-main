# Servicio para manejar la auditoría del sistema.
# Incluirá métodos para registrar acciones y consultar el historial de auditoría.

from datetime import datetime
from mps.services.db import DBConnection

def registrar_auditoria(usuario: str, modulo: str, accion: str, detalle: str):
    """
    Registra una acción en la tabla de auditoría.
    :param usuario: Nombre del usuario que realiza la acción.
    :param modulo: Módulo donde se realiza la acción.
    :param accion: Acción realizada.
    :param detalle: Detalle adicional de la acción.
    """
    db = DBConnection()
    try:
        db.conectar()
        query = """
            INSERT INTO Auditoria (usuario, modulo, accion, detalle, fecha)
            VALUES (?, ?, ?, ?, ?)
        """
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.ejecutar_insert(query, [usuario, modulo, accion, detalle, fecha_actual])
        print(f"Auditoría registrada: Usuario={usuario}, Módulo={modulo}, Acción={accion}, Detalle={detalle}")
    except Exception as e:
        print(f"Error al registrar la auditoría: {e}")
        raise RuntimeError(f"Error al registrar la auditoría: {e}")
    finally:
        db.cerrar()
