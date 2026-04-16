from app.models.database import get_db_connection

def get_analytics_summary():
    """
    Obtiene un resumen de datos para el dashboard de analítica.
    """
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            # Total de clientes
            cursor.execute("SELECT COUNT(*) FROM clientes;")
            total_clientes = cursor.fetchone()[0]

            # Total de ventas (cantidad de transacciones)
            cursor.execute("SELECT COUNT(*) FROM ventas;")
            total_ventas_cantidad = cursor.fetchone()[0]

            # Suma total de ingresos por ventas
            cursor.execute("SELECT SUM(total) FROM ventas;")
            total_ventas_ingresos = cursor.fetchone()[0]

            # Productos más vendidos (Top 5)
            cursor.execute("""
                SELECT p.nombre, SUM(dv.cantidad) as total_vendido
                FROM detalle_ventas dv
                JOIN productos p ON dv.producto_id = p.id
                GROUP BY p.nombre
                ORDER BY total_vendido DESC
                LIMIT 5;
            """)
            productos_mas_vendidos = cursor.fetchall()

    return {
        "total_clientes": total_clientes or 0,
        "total_ventas_cantidad": total_ventas_cantidad or 0,
        "total_ventas_ingresos": float(total_ventas_ingresos) if total_ventas_ingresos else 0.0,
        "productos_mas_vendidos": [{
            "nombre": row[0],
            "total_vendido": row[1]
        } for row in productos_mas_vendidos]
    }
