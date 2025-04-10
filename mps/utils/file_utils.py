import os

def read_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El archivo {file_path} no existe.")
    with open(file_path, 'r') as file:
        return file.read()

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def is_file_accessible(file_path):
    return os.path.exists(file_path) and os.access(file_path, os.R_OK)
