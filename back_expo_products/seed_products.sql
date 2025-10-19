-- Script SQL para insertar 40 productos de tecnología
-- Ejecutar en PostgreSQL

-- Crear tabla si no existe
CREATE TABLE IF NOT EXISTS products (
    id VARCHAR PRIMARY KEY,
    name VARCHAR NOT NULL,
    description VARCHAR NOT NULL,
    price FLOAT NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Limpiar datos existentes (opcional)
-- TRUNCATE TABLE products;

-- Insertar productos
INSERT INTO products (id, name, description, price, stock) VALUES
-- Periféricos de Oficina
('S001', 'Silla Ergonómica Pro', 'Silla de oficina con soporte lumbar ajustable y malla transpirable.', 299.99, 15),
('T010', 'Teclado Mecánico RGB', 'Teclado con switches táctiles y luz de fondo personalizable.', 99.99, 40),
('M001', 'Mouse Inalámbrico Gamer', 'Mouse ergonómico con sensor óptico de 16000 DPI y batería de larga duración.', 59.99, 75),
('W002', 'Webcam Full HD 1080p', 'Cámara web con micrófono integrado y enfoque automático.', 79.99, 30),
('H003', 'Audífonos Bluetooth Premium', 'Auriculares con cancelación de ruido activa y 30 horas de batería.', 199.99, 22),

-- Monitores y Pantallas
('M005', 'Monitor 4K Curvo', 'Monitor ultra ancho ideal para trabajo multitarea y gaming.', 549.99, 0),
('M006', 'Monitor 27 pulgadas QHD', 'Pantalla IPS con tecnología HDR10 y frecuencia de 144Hz.', 349.99, 18),
('M007', 'Monitor Portátil USB-C', 'Pantalla táctil de 15.6 pulgadas ideal para trabajar en movilidad.', 229.99, 12),

-- Laptops y Computadoras
('L001', 'Laptop Ultrabook 14 pulgadas', 'Intel Core i7, 16GB RAM, SSD 512GB, pantalla Full HD.', 1299.99, 8),
('L002', 'Laptop Gaming RGB', 'RTX 4060, AMD Ryzen 9, 32GB RAM, SSD 1TB, pantalla 165Hz.', 1899.99, 5),
('L003', 'MacBook Air M2', 'Chip M2, 8GB RAM, SSD 256GB, pantalla Retina 13 pulgadas.', 1199.99, 0),
('D001', 'PC Escritorio Gamer', 'RTX 4070, Intel i9, 64GB RAM, SSD 2TB + HDD 4TB.', 2499.99, 3),
('D002', 'Mini PC Office', 'Procesador Intel i5, 16GB RAM, SSD 512GB, WiFi 6.', 599.99, 25),

-- Almacenamiento
('S101', 'SSD NVMe 1TB', 'Unidad de estado sólido con velocidades de hasta 7000 MB/s.', 129.99, 50),
('S102', 'Disco Duro Externo 4TB', 'HDD portátil USB 3.0 con cifrado por hardware.', 99.99, 35),
('U001', 'Memoria USB 128GB', 'Pendrive USB 3.2 con velocidades de lectura de 200 MB/s.', 24.99, 100),

-- Networking
('R001', 'Router WiFi 6 Mesh', 'Router de doble banda con cobertura de hasta 300m².', 179.99, 20),
('R002', 'Switch Gigabit 8 Puertos', 'Switch de red no administrado con puertos Ethernet 1000 Mbps.', 49.99, 45),
('A001', 'Adaptador WiFi USB', 'Antena WiFi dual band con velocidades de hasta 1200 Mbps.', 29.99, 60),

-- Audio y Video
('M201', 'Micrófono Condensador USB', 'Micrófono profesional para streaming y podcasting con soporte.', 89.99, 28),
('S201', 'Bocinas Gaming RGB', 'Sistema de altavoces 2.1 con subwoofer y luces LED.', 69.99, 32),
('S202', 'Barra de Sonido Bluetooth', 'Soundbar compacta con Dolby Audio y conexión inalámbrica.', 149.99, 15),

-- Accesorios Gaming
('G001', 'Silla Gaming Reclinable', 'Silla con respaldo ergonómico, reposabrazos 4D y soporte lumbar.', 349.99, 10),
('G002', 'Mouse Pad XXL RGB', 'Alfombrilla extra grande con iluminación LED personalizable.', 39.99, 55),
('G003', 'Control Xbox Inalámbrico', 'Gamepad compatible con PC y consola, batería recargable incluida.', 59.99, 40),
('G004', 'Volante de Carreras', 'Volante con force feedback, pedales y cambio de marchas.', 299.99, 7),

-- Cables y Adaptadores
('C001', 'Cable HDMI 2.1 4K', 'Cable de 2 metros compatible con 8K a 60Hz y 4K a 120Hz.', 19.99, 80),
('C002', 'Hub USB-C 7 en 1', 'Adaptador con HDMI, USB 3.0, lector SD y puerto Ethernet.', 49.99, 42),
('C003', 'Cable USB-C Magnético', 'Cable de carga magnético de 1.5m con transferencia de datos.', 24.99, 65),

-- Energía y Respaldos
('P001', 'UPS 1500VA', 'Sistema de alimentación ininterrumpida con 8 tomas y protección.', 179.99, 12),
('P002', 'Regleta con Protección', 'Multicontacto con 10 tomas, USB y protección contra sobretensión.', 34.99, 48),
('B001', 'Power Bank 20000mAh', 'Batería portátil con carga rápida y salidas USB-C y USB-A.', 39.99, 70),

-- Iluminación y Ambiente
('L101', 'Tira LED RGB 5 metros', 'Luces LED inteligentes controlables por app y asistente de voz.', 29.99, 90),
('L102', 'Lámpara de Escritorio LED', 'Lámpara con 3 modos de iluminación y puerto USB para carga.', 44.99, 35),
('L103', 'Panel LED Hexagonal', 'Set de 6 paneles modulares RGB con sincronización musical.', 79.99, 18),

-- Refrigeración
('F001', 'Base Enfriadora para Laptop', 'Cooler con 5 ventiladores silenciosos y altura ajustable.', 34.99, 38),
('F002', 'Ventilador de Torre USB', 'Ventilador portátil con 3 velocidades y rotación 360°.', 24.99, 52),

-- Seguridad
('K001', 'Cerradura Inteligente Bluetooth', 'Candado con huella digital y control por smartphone.', 69.99, 22),
('K002', 'Cable de Seguridad Kensington', 'Cable antirrobo para laptop con llave de combinación.', 19.99, 45)

ON CONFLICT (id) DO NOTHING;

-- Verificar inserción
SELECT COUNT(*) as total_productos FROM products;
SELECT id, name, stock FROM products ORDER BY id;