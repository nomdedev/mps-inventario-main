CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    rol TEXT CHECK(rol IN ('admin', 'usuario')) NOT NULL,
    modulos TEXT NOT NULL -- Lista de módulos permitidos, separados por comas
);

CREATE TABLE IF NOT EXISTS historial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario TEXT NOT NULL,
    accion TEXT NOT NULL,
    fecha TEXT NOT NULL,
    detalles TEXT  -- Agregar la columna 'detalles'
);

-- Tabla principal de inventario (ya existente)
CREATE TABLE IF NOT EXISTS inventario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo TEXT UNIQUE NOT NULL,
    descripcion TEXT NOT NULL,
    stock INTEGER DEFAULT 0,
    pedido INTEGER DEFAULT 0
);

-- Tabla para gestionar las obras
CREATE TABLE IF NOT EXISTS obras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT UNIQUE NOT NULL,
    fecha_inicio TEXT NOT NULL,
    fecha_fin TEXT,
    responsable TEXT NOT NULL
);

-- Tabla para gestionar el inventario de cada obra
CREATE TABLE IF NOT EXISTS inventario_obras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    obra_id INTEGER NOT NULL,
    codigo TEXT NOT NULL,
    descripcion TEXT NOT NULL,
    stock INTEGER DEFAULT 0,
    pedido INTEGER DEFAULT 0,
    FOREIGN KEY (obra_id) REFERENCES obras (id),
    FOREIGN KEY (codigo) REFERENCES inventario (codigo)
);

-- Trigger para actualizar la tabla principal de inventario
CREATE TRIGGER IF NOT EXISTS actualizar_inventario_principal
AFTER UPDATE ON inventario_obras
FOR EACH ROW
BEGIN
    UPDATE inventario
    SET pedido = (
        SELECT SUM(pedido)
        FROM inventario_obras
        WHERE codigo = NEW.codigo
    ),
    stock = stock - (NEW.pedido - OLD.pedido)
    WHERE codigo = NEW.codigo;
END;

-- Trigger para recalcular el stock disponible en la tabla principal
CREATE TRIGGER IF NOT EXISTS recalcular_disponible
AFTER UPDATE ON inventario
FOR EACH ROW
BEGIN
    -- Aquí puedes agregar lógica adicional si necesitas calcular algo más
END;

-- Tabla para registrar el historial de cambios en las obras
CREATE TABLE IF NOT EXISTS historial_obras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    obra_id INTEGER NOT NULL,
    usuario TEXT NOT NULL,
    accion TEXT NOT NULL,
    fecha TEXT NOT NULL,
    detalles TEXT,
    FOREIGN KEY (obra_id) REFERENCES obras (id)
);
