-- Crear base de datos 'inventario' si no existe
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'inventario')
    CREATE DATABASE inventario;
GO

USE inventario;

-- Crear tabla Materiales
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Materiales]') AND type in (N'U'))
BEGIN
    CREATE TABLE Materiales (
        id INT IDENTITY(1,1) PRIMARY KEY,
        codigo NVARCHAR(50) NOT NULL UNIQUE,
        descripcion NVARCHAR(255) NOT NULL,
        largo_mm INT NOT NULL,
        stock_total INT NOT NULL DEFAULT 0,
        stock_disponible INT NOT NULL DEFAULT 0,
        stock_apartado INT NOT NULL DEFAULT 0
    );
END;

-- Crear tabla Movimientos
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Movimientos]') AND type in (N'U'))
BEGIN
    CREATE TABLE Movimientos (
        id INT IDENTITY(1,1) PRIMARY KEY,
        material_id INT NOT NULL FOREIGN KEY REFERENCES Materiales(id),
        cantidad INT NOT NULL,
        tipo NVARCHAR(50) NOT NULL, -- entrada, salida, apartado
        usuario NVARCHAR(50) NOT NULL,
        obra_id INT NULL,
        fecha DATETIME NOT NULL DEFAULT GETDATE(),
        estado NVARCHAR(50) NOT NULL DEFAULT 'aprobado'
    );
END;

-- Crear tabla Obras
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Obras]') AND type in (N'U'))
BEGIN
    CREATE TABLE Obras (
        id INT IDENTITY(1,1) PRIMARY KEY,
        nombre NVARCHAR(255) NOT NULL,
        cliente NVARCHAR(255) NOT NULL,
        estado NVARCHAR(50) NOT NULL DEFAULT 'En Progreso',
        fecha_inicio DATE NOT NULL DEFAULT GETDATE(),
        fecha_fin DATE NULL
    );
END;

-- Crear tabla Ordenes
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Ordenes]') AND type in (N'U'))
BEGIN
    CREATE TABLE Ordenes (
        id INT IDENTITY(1,1) PRIMARY KEY,
        obra_id INT NOT NULL FOREIGN KEY REFERENCES Obras(id),
        fecha DATETIME NOT NULL DEFAULT GETDATE(),
        estado NVARCHAR(50) NOT NULL DEFAULT 'pendiente',
        total_items INT NOT NULL,
        creado_por NVARCHAR(50) NOT NULL
    );
END;

-- Crear base de datos 'users' si no existe
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'users')
    CREATE DATABASE users;
GO

USE users;

-- Crear tabla Usuarios
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Usuarios]') AND type in (N'U'))
BEGIN
    CREATE TABLE Usuarios (
        id INT IDENTITY(1,1) PRIMARY KEY,
        usuario NVARCHAR(50) NOT NULL UNIQUE,
        contraseña NVARCHAR(255) NOT NULL,
        rol NVARCHAR(50) NOT NULL, -- admin, supervisor, operador
        nombre NVARCHAR(255) NOT NULL,
        apellido NVARCHAR(255) NOT NULL,
        activo BIT NOT NULL DEFAULT 1
    );

    -- Insertar usuarios por defecto
    INSERT INTO Usuarios (usuario, contraseña, rol, nombre, apellido)
    VALUES 
        ('admin', 'admin123', 'admin', 'Admin', 'General'),
        ('supervisor', 'supervisor123', 'supervisor', 'Supervisor', 'General');
END;

-- Crear base de datos 'auditorias' si no existe
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'auditorias')
    CREATE DATABASE auditorias;
GO

USE auditorias;

-- Crear tabla Auditoria
IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Auditoria]') AND type in (N'U'))
BEGIN
    CREATE TABLE Auditoria (
        id INT IDENTITY(1,1) PRIMARY KEY,
        usuario NVARCHAR(50) NOT NULL,
        modulo NVARCHAR(50) NOT NULL,
        accion NVARCHAR(255) NOT NULL,
        descripcion NVARCHAR(MAX) NULL,
        fecha DATETIME NOT NULL DEFAULT GETDATE()
    );
END;
