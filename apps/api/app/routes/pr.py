from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.pr_controller import handle_analyze_pr
from app.db.session import get_db
from app.schemas.pr import PRAnalyzeRequest, PRAnalyzeResponse

router = APIRouter(prefix="/api/pr", tags=["pr"])


@router.post("/analyze", response_model=PRAnalyzeResponse)
def analyze(payload: PRAnalyzeRequest, db: Session = Depends(get_db)) -> PRAnalyzeResponse:
    return handle_analyze_pr(payload, db)
