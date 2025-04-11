CREATE DATABASE inventario_db;

USE inventario_db;

-- Tabla de inventario
CREATE TABLE inventario (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100), -- Nombre del producto
    cantidad INT, -- Cantidad disponible
    precio DECIMAL(10, 2), -- Precio unitario
    apartado INT DEFAULT 0, -- Cantidad apartada
    observaciones NVARCHAR(255), -- Observaciones generales
    proveedor NVARCHAR(100), -- Proveedor del producto
    fecha_ingreso DATE, -- Fecha de ingreso al inventario
    categoria NVARCHAR(100), -- Categoría del producto
    ubicacion NVARCHAR(100) -- Ubicación en el almacén
);

INSERT INTO inventario (nombre, cantidad, precio, apartado, observaciones)
VALUES 
    ('Perfil PVC A', 100, 25.50, 0, 'Sin observaciones'),
    ('Perfil PVC B', 200, 30.00, 0, 'Sin observaciones'),
    ('Perfil PVC C', 150, 20.75, 0, 'Sin observaciones');

-- Tabla de usuarios
CREATE TABLE usuarios (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100), -- Nombre del usuario
    apellido NVARCHAR(100), -- Apellido del usuario
    rol NVARCHAR(50), -- Rol del usuario
    telefono NVARCHAR(50), -- Teléfono del usuario
    email NVARCHAR(100), -- Email del usuario
    direccion NVARCHAR(255), -- Dirección del usuario
    fecha_registro DATE DEFAULT GETDATE() -- Fecha de registro del usuario
);

INSERT INTO usuarios (nombre, rol)
VALUES ('Admin', 'Administrador'),
       ('Juan Pérez', 'Operador'),
       ('Ana López', 'Supervisor');

-- Tabla de obras
CREATE TABLE obras (
    id INT PRIMARY KEY IDENTITY(1,1),
    nombre NVARCHAR(100), -- Nombre de la obra
    cliente NVARCHAR(100), -- Nombre del cliente
    apellido_cliente NVARCHAR(100), -- Apellido del cliente
    arquitecto NVARCHAR(100), -- Nombre del arquitecto
    telefono NVARCHAR(50), -- Teléfono de contacto
    direccion NVARCHAR(255), -- Dirección de la obra
    pago_adelantado DECIMAL(10, 2), -- Monto pagado por adelantado
    monto_final DECIMAL(10, 2), -- Monto total de la obra
    monto_colocacion DECIMAL(10, 2), -- Monto por colocación
    fecha_medicion DATE, -- Fecha de medición
    fecha_colocacion DATE -- Fecha de colocación
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
    fecha DATETIME DEFAULT GETDATE(),
    tabla_afectada NVARCHAR(50), -- Tabla afectada por la acción
    estado NVARCHAR(50) DEFAULT 'Pendiente', -- Estado de la acción
    justificativo NVARCHAR(255), -- Justificación de la acción
    admin_id INT NULL, -- ID del administrador que aprobó/rechazó
    razon NVARCHAR(255), -- Razón de la acción
    ip_origen NVARCHAR(50), -- Dirección IP de origen
    dispositivo NVARCHAR(100) -- Dispositivo desde el cual se realizó la acción
);

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
    total DECIMAL(10, 2),
    nombre_cliente NVARCHAR(100), -- Nombre del cliente
    apellido_cliente NVARCHAR(100), -- Apellido del cliente
    direccion_obra NVARCHAR(255), -- Dirección de la obra
    cantidad_aberturas INT, -- Cantidad de aberturas
    colocador NVARCHAR(100), -- Persona que colocó
    reviso NVARCHAR(100), -- Persona que revisó
    controlo NVARCHAR(100), -- Persona que controló
    entrego NVARCHAR(100), -- Persona que entregó
    problemas NVARCHAR(50), -- Indicar si hubo problemas (Sí/No)
    falta_material NVARCHAR(255), -- Material faltante para entregar
    observaciones NVARCHAR(MAX) -- Observaciones generales
);

-- Tabla de detalles de órdenes
CREATE TABLE orden_detalles (
    id INT PRIMARY KEY IDENTITY(1,1),
    orden_id INT FOREIGN KEY REFERENCES ordenes(id),
    inventario_id INT FOREIGN KEY REFERENCES inventario(id),
    cantidad INT,
    precio_unitario DECIMAL(10, 2),
    descuento DECIMAL(10, 2) DEFAULT 0, -- Descuento aplicado
    subtotal DECIMAL(10, 2) -- Subtotal calculado
);

-- Tabla de logística
CREATE TABLE logistica (
    id INT PRIMARY KEY IDENTITY(1,1),
    obra_id INT FOREIGN KEY REFERENCES obras(id),
    fecha_entrega DATE,
    estado NVARCHAR(50),
    nombre NVARCHAR(100), -- Nombre del cliente
    apellido NVARCHAR(100), -- Apellido del cliente
    arquitecto NVARCHAR(100), -- Nombre del arquitecto
    direccion_obra NVARCHAR(255), -- Dirección de la obra
    cantidad_aberturas INT, -- Cantidad de aberturas
    colocador NVARCHAR(100), -- Persona que colocó
    reviso NVARCHAR(100), -- Persona que revisó
    controlo NVARCHAR(100), -- Persona que controló
    entrego NVARCHAR(100), -- Persona que entregó
    problemas NVARCHAR(50), -- Indicar si hubo problemas (Sí/No)
    falta_material NVARCHAR(255), -- Material faltante para entregar
    observaciones NVARCHAR(MAX) -- Observaciones generales
);

-- Tabla de vidrios
CREATE TABLE vidrios (
    id INT PRIMARY KEY IDENTITY(1,1),
    obra_id INT FOREIGN KEY REFERENCES obras(id),
    ancho DECIMAL(10, 2),
    alto DECIMAL(10, 2),
    tipologia NVARCHAR(100),
    observaciones NVARCHAR(255),
    estado NVARCHAR(50) DEFAULT 'Pendiente',
    espesor DECIMAL(10, 2), -- Espesor del vidrio
    color NVARCHAR(50) -- Color del vidrio
);

INSERT INTO vidrios (obra_id, ancho, alto, tipologia, observaciones, estado)
VALUES 
    (1, 1.20, 2.50, 'Vidrio Templado', 'Sin observaciones', 'Pendiente'),
    (2, 1.50, 2.00, 'Vidrio Laminado', 'Sucio al entregar', 'Reposición');
