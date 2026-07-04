from fastapi import FastAPI

from app.routes.health import router as health_router
from app.routes.pr import router as pr_router


app = FastAPI(title="DeploySage API", version="1.0.0")

app.include_router(health_router)
app.include_router(pr_router)
