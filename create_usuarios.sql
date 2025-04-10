-- Crear la base de datos "usuarios" si no existe
IF NOT EXISTS(SELECT * FROM sys.databases WHERE name = 'usuarios')
BEGIN
    CREATE DATABASE usuarios;
    PRINT 'Base de datos usuarios creada.';
END
GO

USE usuarios;
GO

-- Crear la tabla "usuarios" si no existe
IF OBJECT_ID('dbo.usuarios', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.usuarios (
        id INT IDENTITY(1,1) PRIMARY KEY,
        username NVARCHAR(255) NOT NULL UNIQUE,
        password NVARCHAR(255) NOT NULL,
        role NVARCHAR(50) NOT NULL
    );
    PRINT 'Tabla usuarios creada.';
END
GO
