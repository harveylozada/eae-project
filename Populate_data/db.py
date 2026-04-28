# db.py
import os
import random
from dotenv import load_dotenv
from faker import Faker
import psycopg2

print("cargando varuables")
# Cargar variables de entorno desde el archivo .env
load_dotenv()

print("cargando variables de conexion")
# Variables de conexión
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "2323")
DB_NAME = os.getenv("DB_NAME", "empresa_amiga")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "el amigo23")

print("condigurando Faker")
# Configuración de Faker
FAKER_LANG = os.getenv("FAKER_LANG", "es_ES")
fake = Faker(FAKER_LANG)

print("def get_connection")
def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

print("def insert_cliente")
def insert_cliente(conn):
    cursor = conn.cursor()
    nombre = fake.first_name()
    apellido = fake.last_name()
    email = fake.unique.email()
    telefono = fake.phone_number()
    direccion = fake.address().replace("\n", ", ")

    query = """
        INSERT INTO clientes (nombre, apellido, email, telefono, direccion)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id;
    """
    cursor.execute(query, (nombre, apellido, email, telefono, direccion))
    client_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return client_id

print("def insert producto")
def insert_producto(conn):
    """
    Inserta un registro en la tabla 'productos' utilizando datos generados por Faker.
    Retorna el id del producto insertado.
    """
    cursor = conn.cursor()
    nombre = fake.word().capitalize()
    descripcion = fake.sentence(nb_words=10)
    precio = round(random.uniform(10, 500), 2)
    stock = random.randint(1, 100)

    query = """
        INSERT INTO productos (nombre, descripcion, precio, stock)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
    """
    cursor.execute(query, (nombre, descripcion, precio, stock))
    producto_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return producto_id

print("def insert_venta")
def insert_venta(conn, cliente_id):
    """
    Inserta un registro en la tabla 'ventas' para un cliente dado.
    Inicialmente se establece el total en 0, que se actualizará posteriormente.
    Retorna el id de la venta insertada.
    """
    cursor = conn.cursor()
    query = """
        INSERT INTO ventas (cliente_id, total)
        VALUES (%s, %s)
        RETURNING id;
    """
    cursor.execute(query, (cliente_id, 0))
    venta_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return venta_id

print("def insert_detalle_venta")
def insert_detalle_venta(conn, venta_id, producto_id, cantidad, precio_unitario):
    """
    Inserta un registro en la tabla 'detalle_ventas' para relacionar una venta con un producto.
    """
    cursor = conn.cursor()
    query = """
        INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio_unitario)
        VALUES (%s, %s, %s, %s);
    """
    cursor.execute(query, (venta_id, producto_id, cantidad, precio_unitario))
    conn.commit()
    cursor.close()

print("def insert_detalle_venta")
def insert_detalle_venta(conn, venta_id, producto_id, cantidad, precio_unitario):
    cursor = conn.cursor()
    
    # --- 1. VALIDAR STOCK ACTUAL (Requerimiento Profe) ---
    cursor.execute("SELECT stock FROM productos WHERE id = %s", (producto_id,))
    resultado = cursor.fetchone()
    
    if resultado and resultado[0] >= cantidad:
        # --- 2. REGISTRAR LA VENTA ---
        query_insert = """
            INSERT INTO detalle_ventas (venta_id, producto_id, cantidad, precio_unitario)
            VALUES (%s, %s, %s, %s);
        """
        cursor.execute(query_insert, (venta_id, producto_id, cantidad, precio_unitario))
        
        # --- 3. DESCONTAR DEL STOCK (Control de Inventario) ---
        nuevo_stock = resultado[0] - cantidad
        cursor.execute("UPDATE productos SET stock = %s WHERE id = %s", (nuevo_stock, producto_id))
        
        conn.commit()
        print(f"Venta registrada. Stock actualizado de {resultado[0]} a {nuevo_stock}")
    else:
        print(f"Error: Stock insuficiente para producto {producto_id}. (Disponible: {resultado[0] if resultado else 0})")
    cursor.close()

print("update_venta_total")
def update_venta_total(conn, venta_id):
    """
    Calcula la suma de los subtotales de la venta (cantidad * precio_unitario de cada detalle)
    y actualiza el campo 'total' de la tabla 'ventas'.
    """
    cursor = conn.cursor()
    query = """
        SELECT COALESCE(SUM(cantidad * precio_unitario), 0)
        FROM detalle_ventas
        WHERE venta_id = %s;
    """
    cursor.execute(query, (venta_id,))
    total = cursor.fetchone()[0]

    update_query = "UPDATE ventas SET total = %s WHERE id = %s;"
    cursor.execute(update_query, (total, venta_id))
    conn.commit()
    cursor.close()

print("Proceso Terminado")
