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

-- Crear tabla Usuarios en 'users'
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'users')
    CREATE DATABASE users;
GO

USE users;

IF NOT EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Usuarios]') AND type in (N'U'))
BEGIN
    CREATE TABLE Usuarios (
        id INT IDENTITY(1,1) PRIMARY KEY,
        usuario NVARCHAR(50) NOT NULL UNIQUE,
        contraseña NVARCHAR(255) NOT NULL,
        rol NVARCHAR(50) NOT NULL,
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

-- Crear tabla Auditoria en 'auditorias'
IF NOT EXISTS (SELECT * FROM sys.databases WHERE name = 'auditorias')
    CREATE DATABASE auditorias;
GO

USE auditorias;

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
