-- Crear la base de datos "auditoria" si no existe
IF NOT EXISTS(SELECT * FROM sys.databases WHERE name = 'auditoria')
BEGIN
    CREATE DATABASE auditoria;
    PRINT 'Base de datos auditoria creada.';
END
GO

USE auditoria;
GO

-- Crear la tabla "auditoria" si no existe
IF OBJECT_ID('dbo.auditoria', 'U') IS NULL
BEGIN
    CREATE TABLE dbo.auditoria (
        id INT IDENTITY(1,1) PRIMARY KEY,
        usuario_id INT NOT NULL,
        accion NVARCHAR(255) NOT NULL,
        tabla_afectada NVARCHAR(255) NOT NULL,
        fecha DATETIME NOT NULL DEFAULT GETDATE(),
        estado NVARCHAR(50) DEFAULT 'Completada',
        justificativo NVARCHAR(MAX) NULL,
        admin_id INT NULL,
        razon NVARCHAR(MAX) NULL
    );
    PRINT 'Tabla auditoria creada.';
END
GO
