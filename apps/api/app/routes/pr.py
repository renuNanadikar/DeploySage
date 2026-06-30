from fastapi import APIRouter

from app.controllers.pr_controller import analyze_pr
from app.schemas.pr_analysis import PRAnalyzeRequest, PRAnalyzeResponse


router = APIRouter(prefix="/api/pr", tags=["Pull Requests"])


@router.post("/analyze", response_model=PRAnalyzeResponse)
def post_analyze_pr(payload: PRAnalyzeRequest) -> PRAnalyzeResponse:
    return analyze_pr(payload)