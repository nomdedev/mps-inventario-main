from mps.services.db import DBConnection

def insertar_usuarios_iniciales():
    usuarios = [
        {
            "usuario": "admin",
            "contraseña": "admin123",
            "rol": "admin",
            "nombre": "Admin",
            "apellido": "General"
        },
        {
            "usuario": "magostini",
            "contraseña": "supervisor123",
            "rol": "supervisor",
            "nombre": "Maximiliano",
            "apellido": "Agostini"
        }
    ]

    db = DBConnection()
    try:
        db.conectar(base="users")
        for usuario in usuarios:
            # Verificar si el usuario ya existe
            query_check = "SELECT COUNT(*) FROM Usuarios WHERE usuario = ?"
            resultado = db.ejecutar_query(query_check, [usuario["usuario"]])
            if resultado[0][0] > 0:
                print(f"El usuario '{usuario['usuario']}' ya existe. No se insertará.")
                continue

            # Insertar el usuario
            query_insert = """
                INSERT INTO Usuarios (usuario, contraseña, rol, nombre, apellido)
                VALUES (?, ?, ?, ?, ?)
            """
            db.ejecutar_insert(query_insert, [
                usuario["usuario"],
                usuario["contraseña"],
                usuario["rol"],
                usuario["nombre"],
                usuario["apellido"]
            ])
            print(f"Usuario '{usuario['usuario']}' insertado correctamente.")
    except Exception as e:
        print(f"Error al insertar usuarios iniciales: {e}")
    finally:
        db.cerrar()

if __name__ == "__main__":
    insertar_usuarios_iniciales()
