from cryptography.fernet import Fernet

# Generar una clave segura
key = Fernet.generate_key()

# Guardar la clave en un archivo
with open("encryption_key.key", "wb") as key_file:
    key_file.write(key)

print("Clave de cifrado generada y guardada en 'encryption_key.key'.")
