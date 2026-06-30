from app.schemas.health import HealthResponse


def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        service="DeploySage API",
        version="1.0.0",
    )
