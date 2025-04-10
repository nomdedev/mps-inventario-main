CREATE DATABASE inventario_db;

USE inventario_db;

-- Tabla de inventario
CREATE TABLE inventario (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100),
    cantidad INT,
    precio DECIMAL(10, 2)
);

ALTER TABLE inventario
ADD apartado INT DEFAULT 0,
    observaciones NVARCHAR(255);

INSERT INTO inventario (nombre, cantidad, precio, apartado, observaciones)
VALUES 
    ('Perfil PVC A', 100, 25.50, 0, 'Sin observaciones'),
    ('Perfil PVC B', 200, 30.00, 0, 'Sin observaciones'),
    ('Perfil PVC C', 150, 20.75, 0, 'Sin observaciones');

-- Tabla de usuarios
CREATE TABLE usuarios (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100),  -- Asegúrate de que este nombre sea correcto
    rol NVARCHAR(50)       -- Asegúrate de que este nombre sea correcto
);

INSERT INTO usuarios (nombre, rol)
VALUES ('Admin', 'Administrador'),
       ('Juan Pérez', 'Operador'),
       ('Ana López', 'Supervisor');

-- Tabla de obras
CREATE TABLE obras (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100),
    cliente NVARCHAR(100)
);

INSERT INTO obras (nombre, cliente)
VALUES ('Obra A', 'Cliente 1'),
       ('Obra B', 'Cliente 2'),
       ('Obra C', 'Cliente 3');

-- Tabla de auditoría
CREATE TABLE auditoria (
    id INT PRIMARY KEY IDENTITY(1,1),
    usuario_id INT FOREIGN KEY REFERENCES usuarios(id),
    accion NVARCHAR(255),
    fecha DATETIME DEFAULT GETDATE()
);

ALTER TABLE auditoria
ADD tabla_afectada NVARCHAR(50),
    estado NVARCHAR(50) DEFAULT 'Pendiente',
    justificativo NVARCHAR(255),
    admin_id INT NULL,
    razon NVARCHAR(255);

-- Crear la tabla de auditoría si no existe
CREATE TABLE IF NOT EXISTS Auditoria (
    id INT IDENTITY(1,1) PRIMARY KEY,
    usuario NVARCHAR(100) NOT NULL,
    modulo NVARCHAR(100) NOT NULL,
    accion NVARCHAR(255) NOT NULL,
    detalle NVARCHAR(MAX),
    fecha DATETIME NOT NULL DEFAULT GETDATE()
);

-- Crear la tabla de aprobaciones si no existe
CREATE TABLE IF NOT EXISTS Aprobaciones (
    id INT IDENTITY(1,1) PRIMARY KEY,
    tipo NVARCHAR(100) NOT NULL,
    id_referencia INT NOT NULL,
    usuario_solicitante NVARCHAR(100) NOT NULL,
    usuario_aprobador NVARCHAR(100),
    estado NVARCHAR(50) NOT NULL DEFAULT 'Pendiente',
    comentario NVARCHAR(MAX),
    fecha DATETIME NOT NULL DEFAULT GETDATE()
);

-- Tabla de órdenes de compra
CREATE TABLE ordenes (
    id INT PRIMARY KEY IDENTITY(1,1),
    obra_id INT FOREIGN KEY REFERENCES obras(id),
    usuario_id INT FOREIGN KEY REFERENCES usuarios(id),
    fecha DATETIME DEFAULT GETDATE(),
    total DECIMAL(10, 2)
);

-- Tabla de detalles de órdenes
CREATE TABLE orden_detalles (
    id INT PRIMARY KEY IDENTITY(1,1),
    orden_id INT FOREIGN KEY REFERENCES ordenes(id),
    inventario_id INT FOREIGN KEY REFERENCES inventario(id),
    cantidad INT,
    precio_unitario DECIMAL(10, 2)
);

-- Tabla de logística
CREATE TABLE logistica (
    id INT PRIMARY KEY IDENTITY(1,1),
    obra_id INT FOREIGN KEY REFERENCES obras(id),
    fecha_entrega DATE,
    estado NVARCHAR(50)
);

-- Tabla de vidrios
CREATE TABLE vidrios (
    id INT PRIMARY KEY IDENTITY(1,1),
    obra_id INT FOREIGN KEY REFERENCES obras(id),
    ancho DECIMAL(10, 2),
    alto DECIMAL(10, 2),
    tipologia NVARCHAR(100),
    observaciones NVARCHAR(255),
    estado NVARCHAR(50) DEFAULT 'Pendiente'
);

INSERT INTO vidrios (obra_id, ancho, alto, tipologia, observaciones, estado)
VALUES 
    (1, 1.20, 2.50, 'Vidrio Templado', 'Sin observaciones', 'Pendiente'),
    (2, 1.50, 2.00, 'Vidrio Laminado', 'Sucio al entregar', 'Reposición');
