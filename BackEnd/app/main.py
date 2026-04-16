from fastapi import FastAPI
from app.routes.client_routes import router as client_router
from app.routes.product_routes import router as product_router
from app.routes.venta_routes import router as venta_router
from app.routes.analytics_routes import router as analytics_router

app = FastAPI()

app.include_router(client_router, prefix = "/api", tags = ["Clientes"])
app.include_router(product_router, prefix = "/api", tags = ["Productos"])
app.include_router(venta_router, prefix = "/api", tags = ["Ventas"])
app.include_router(analytics_router, prefix = "/api", tags = ["Analytics"])
