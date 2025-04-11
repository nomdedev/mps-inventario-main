# MPS Inventario

Este proyecto es una aplicación para la gestión de inventarios con soporte para múltiples bases de datos y manejo seguro de credenciales.

## Requisitos

- Python 3.8 o superior
- PyQt5
- python-dotenv
- pyodbc
- cryptography

## Instalación

1. Clonar el repositorio.
2. Crear un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
3. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Generar la clave de cifrado:
   ```bash
   python mps/config/generate_key.py
   ```
5. Configurar las credenciales iniciales en el archivo `.env`.

## Uso

1. Ejecutar la aplicación:
   ```bash
   python main.py
   ```
2. Configurar la base de datos desde la interfaz gráfica si es necesario.

## Seguridad

- Las contraseñas se cifran utilizando `cryptography` y se almacenan en el archivo `.env`.
- El archivo `.env` y la clave de cifrado (`encryption_key.key`) están excluidos del control de versiones mediante `.gitignore`.

## Seguridad adicional

Para proteger el archivo `.env` y la clave de cifrado (`encryption_key.key`), asegúrate de restringir los permisos de archivo:

### En Linux/MacOS
```bash
chmod 600 .env encryption_key.key
```

### En Windows
```powershell
icacls .env /inheritance:r /grant:r "%username%:F"
icacls encryption_key.key /inheritance:r /grant:r "%username%:F"
```

Esto asegura que solo el usuario actual pueda leer o escribir estos archivos.

## Registro

Los eventos y errores se registran en el archivo `app.log` para facilitar la depuración.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la licencia MIT.

