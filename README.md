# MPS Inventario App

Sistema de gestión de inventario y logística de obras, desarrollado en **Python + PyQt6**, con base de datos **SQL Server**. Inspirado en arquitectura SAP.

---

## 📦 Funcionalidades principales

- **Gestión de inventario**: Control de stock disponible, total y apartado.
- **Módulo de obras**: Etapas definidas (medición, fabricación, colocación).
- **Órdenes y pedidos**: Creación, seguimiento y aprobación de materiales.
- **Sistema de usuarios**: Roles definidos (`admin`, `supervisor`, `operador`).
- **Aprobaciones**: Validación de acciones sensibles.
- **Auditoría**: Registro completo de cada operación.
- **Dashboard**: KPIs, gráficos y entregas recientes.
- **Exportación**: Reportes en Excel y PDF.
- **Actualizador remoto**: Verificación y descarga de nuevas versiones.

---

## 🚀 Cómo correr el proyecto (modo desarrollo)

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/nomdedev/mps-inventario.git
   cd mps-inventario
   ```

2. **Activar el entorno virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la app**:
   ```bash
   python main.py
   ```

---

## 🏗 Cómo compilar en .exe

Usar **PyInstaller** para generar un ejecutable:
```bash
pyinstaller --noconfirm --noconsole --icon=icon.ico --name "MPS Inventario" main.py
```
El ejecutable estará en la carpeta `dist/MPS Inventario/`.

---

## 🔁 Actualizaciones

La app incluye un módulo de actualización que:
- Verifica la versión online.
- Descarga automáticamente la nueva versión si está disponible.
- Permite forzar actualizaciones solo para usuarios `admin`.

---

## 🧪 Ramas y control de versiones

| Rama         | Descripción                                      |
|--------------|--------------------------------------------------|
| **main**     | Desarrollo activo.                              |
| **release**  | Versión estable (solo se mergea desde `main`).   |
| **feature/** | Funcionalidades nuevas por módulo.               |

**Importante**: Nunca trabajar directamente en `release`.

---

## 🛠️ Agregar nuevas funcionalidades

1. **Crear una nueva rama**:
   ```bash
   git checkout -b feature/nombre
   ```

2. **Implementar el módulo**:
   - Ubicarlo en `controllers/`, `models/`, `ui/` o `services/`.

3. **Evitar modificar directamente**:
   - `main.py`
   - `login`
   - `session`
   - `permisos`
   - Conexión global a la base de datos.

4. **Probar y validar**:
   - Si funciona correctamente, hacer merge a `main`.

---

## 🧠 Roles y permisos

| Rol          | Permisos                                                                 |
|--------------|--------------------------------------------------------------------------|
| **admin**    | Acceso completo: gestión de usuarios, roles y actualizaciones.           |
| **supervisor** | Aprobación de acciones, gestión de logística y órdenes.                |
| **operador** | Uso básico: inventario y pedidos (sin acceso a usuarios ni roles).       |

---

## 📁 Estructura del proyecto

```plaintext
mps-inventario/
│
├── main.py
├── /mps/
│   ├── ui/              # Interfaz PyQt6
│   ├── models/          # Clases de datos
│   ├── controllers/     # Lógica de negocio
│   ├── services/        # Conexiones, sesiones, permisos
│   ├── utils/           # Exportación, logs, herramientas
│
├── requirements.txt
├── README.md
└── exports/             # Archivos generados (Excel, PDF)
```

---

## ✨ Autor

**Martín Nomdedeu**  
🔧 Desarrollador, líder de implementación técnica y visión SAP-style.

