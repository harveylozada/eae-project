-- Crear la base de datos si no existe
SELECT 'CREATE DATABASE empresa_amiga'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'empresa_amiga')\gexec

-- Conectar a la base de datos
\c empresa_amiga;

-- Crear las tablas solo si no existen
-- Tabla de Géneros (0: Masculino, 1: Femenino)
CREATE TABLE IF NOT EXISTS generos (
    id INT PRIMARY KEY,
    valor VARCHAR(20) NOT NULL
);

-- Tabla de Países
CREATE TABLE IF NOT EXISTS paises (
    codigo VARCHAR(5) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Tabla de Ciudades
CREATE TABLE IF NOT EXISTS ciudades (
    codigo VARCHAR(5) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo_pais VARCHAR(5),
    FOREIGN KEY (codigo_pais) REFERENCES paises(codigo)
);

--CREATE TABLE IF NOT EXISTS clientes (
--    id SERIAL PRIMARY KEY,
--    nombre VARCHAR(100) NOT NULL,
--    apellido VARCHAR(100) NOT NULL,
--    email VARCHAR(150) UNIQUE NOT NULL,
--    telefono VARCHAR(25),
--    direccion TEXT,
--    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
--);
CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telefono VARCHAR(25),
    direccion TEXT,
    edad INT, -- Campo nuevo
    genero_id INT, -- Relación con géneros
    codigo_pais VARCHAR(5), -- Relación con países
    codigo_ciudad VARCHAR(5), -- Relación con ciudades
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (genero_id) REFERENCES generos(id),
    FOREIGN KEY (codigo_pais) REFERENCES paises(codigo),
    FOREIGN KEY (codigo_ciudad) REFERENCES ciudades(codigo)
);

CREATE TABLE IF NOT EXISTS productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL CHECK (precio > 0),
    stock INT NOT NULL CHECK (stock >= 0),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ventas (
    id SERIAL PRIMARY KEY,
    cliente_id INT NOT NULL,
    fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL(10,2) CHECK (total >= 0),
    FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS detalle_ventas (
    id SERIAL PRIMARY KEY,
    venta_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(10,2) NOT NULL CHECK (precio_unitario > 0),
    subtotal DECIMAL(10,2) GENERATED ALWAYS AS (cantidad * precio_unitario) STORED,
    FOREIGN KEY (venta_id) REFERENCES ventas(id) ON DELETE CASCADE,
    FOREIGN KEY (producto_id) REFERENCES productos(id) ON DELETE CASCADE
);

-- Crear índices solo si no existen
CREATE INDEX IF NOT EXISTS idx_cliente_email ON clientes(email);
CREATE INDEX IF NOT EXISTS idx_producto_nombre ON productos(nombre);
CREATE INDEX IF NOT EXISTS idx_venta_fecha ON ventas(fecha_venta);

-- Índices para las nuevas tablas maestras
-- CREATE INDEX IF NOT EXISTS idx_paises_nombre ON paises(nombre);
-- CREATE INDEX IF NOT EXISTS idx_ciudades_nombre ON ciudades(nombre);
-- CREATE INDEX IF NOT EXISTS idx_ciudades_pais ON ciudades(codigo_pais);

-- Índices para los nuevos campos de búsqueda en clientes
CREATE INDEX IF NOT EXISTS idx_cliente_pais ON clientes(codigo_pais);
CREATE INDEX IF NOT EXISTS idx_cliente_ciudad ON clientes(codigo_ciudad);
CREATE INDEX IF NOT EXISTS idx_cliente_genero ON clientes(genero_id);
CREATE INDEX IF NOT EXISTS idx_cliente_edad ON clientes(edad);
