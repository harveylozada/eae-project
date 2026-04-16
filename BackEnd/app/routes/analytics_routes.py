from fastapi import APIRouter, Depends
from fastapi.security import HTTPBasicCredentials
from app.services.analytics_service import get_analytics_summary
from app.routes.client_routes import verify_credentials, security

router = APIRouter()

@router.get("/analytics/summary")
def get_summary(credentials: HTTPBasicCredentials = Depends(security)):
    verify_credentials(credentials)
    summary = get_analytics_summary()
    return summary
