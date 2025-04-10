from mps.services.db import DBConnection

def tiene_permiso(usuario: str, accion: str) -> bool:
    """
    Verifica si un usuario tiene permiso para realizar una acción específica según su rol.
    :param usuario: Nombre del usuario.
    :param accion: Acción a validar.
    :return: True si tiene permiso, False en caso contrario.
    """
    permisos_por_rol = {
        "admin": ["ver_aprobaciones", "aprobar_solicitud", "rechazar_solicitud"],
        "supervisor": ["ver_aprobaciones", "aprobar_solicitud", "rechazar_solicitud"],
        "operador": []
    }

    db = DBConnection()
    try:
        db.conectar(base="users")
        query = "SELECT rol FROM Usuarios WHERE usuario = ?"
        resultado = db.ejecutar_query(query, [usuario])

        if not resultado:
            return False  # Usuario no encontrado

        rol = resultado[0][0]
        acciones_permitidas = permisos_por_rol.get(rol, [])
        return accion in acciones_permitidas
    except Exception as e:
        print(f"Error al verificar permisos: {e}")
        return False
    finally:
        db.cerrar()
