from fastapi import APIRouter

from app.controllers.health_controller import health_check
from app.schemas.health import HealthResponse


router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def get_health() -> HealthResponse:
    return health_check()
