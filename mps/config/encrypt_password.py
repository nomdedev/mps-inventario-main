from cryptography.fernet import Fernet
import base64

# Generar una clave segura (hacer esto una sola vez y guardarla)
key = Fernet.generate_key()
print(f"Clave generada: {key.decode()}")  # Guardar esta clave en un lugar seguro

# Cifrar la contraseña
def encrypt_password(password):
    fernet = Fernet(key)
    return base64.b64encode(fernet.encrypt(password.encode())).decode()

# Ejemplo de uso
if __name__ == "__main__":
    password = "mps.1887"  # Reemplaza con la contraseña real
    encrypted_password = encrypt_password(password)
    print(f"Contraseña cifrada: {encrypted_password}")
