import pytest
from mps.config.db_config import decrypt_password

def test_decrypt_password():
    # Clave y contraseña de prueba
    key = b'YOUR_SECRET_KEY_HERE'  # Reemplazar con la clave real usada en el proyecto
    encrypted_password = "ENCRYPTED_PASSWORD_HERE"  # Reemplazar con una contraseña cifrada válida

    # Simular descifrado
    from cryptography.fernet import Fernet
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password.encode()).decode()

    # Verificar que la contraseña descifrada sea correcta
    assert decrypted_password == "mps.1887"
