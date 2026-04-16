from app.models.database import get_db_connection
from app.schemas.product_schema import ProductCreate,ProductUpdate

def get_productos():
    """
    Obtiene todos los clientes
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id, nombre, descripcion, precio, stock, fecha_creacion FROM productos;")
            productos = cursor.fetchall()
            return [
                {"id": c[0], "nombre": c[1], "descripcion": c[2], "precio": c[3], "stock": c[4],
                 "fecha_creacion": c[5]} for c in productos
            ]


def get_producto(producto_id: int):
    """
    Obtiene un producto por su ID.
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id,nombre,descripcion,precio, "
                           "stock, fecha_creacion FROM productos WHERE id =%s;", (producto_id,))
            producto = cursor.fetchone()
            if producto:
                return {"id": producto[0], "nombre": producto[1], "descripcion": producto[2], "precio": producto[3],
                        "stock": producto[4], "fecha_creacion": producto[5]}
            return None


def create_producto(producto: ProductCreate):
    """
    Crea un producto en la base de datos
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO productos(nombre,descripcion,precio,stock,fecha_creacion) VALUES(%s,%s,%s,%s,%s) RETURNING id;",
                (producto.nombre, producto.descripcion, producto.precio, producto.stock, producto.fecha_creacion)
            )
            producto_id = cursor.fetchone()[0]
            conn.commit()
            return {"id": producto_id, **producto.dict()}


def update_producto(producto_id: int, producto: ProductUpdate):
    """
    Actualiza un producto en la base de datos
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE productos SET nombre = %s, descripcion =%s, precio = %s, stock = %s, fecha_creacion = %s WHERE id = %s RETURNING id;",
                (producto.nombre, producto.descripcion, producto.precio, producto.stock, producto.fecha_creacion, producto_id)
            )
            update_id = cursor.fetchone()
            conn.commit()
            return {"id": producto_id, **producto.dict()} if update_id else None


def delete_producto(producto_id: int):
    """
    Elimina un producto por su ID
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM productos WHERE id = %s RETURNING id;", (producto_id,))
            deleted_id = cursor.fetchone()
            conn.commit()
            return deleted_id is not None