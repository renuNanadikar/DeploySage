from sqlalchemy.orm import Session

from app.schemas.pr import PRAnalyzeRequest, PRAnalyzeResponse
from app.services.pr_analysis_service import analyze_pr


def handle_analyze_pr(payload: PRAnalyzeRequest, db: Session) -> PRAnalyzeResponse:
    result = analyze_pr(db, payload)
    return PRAnalyzeResponse(
        analysis_run_id=result.analysis_run_id,
        summary=result.summary,
        risk_score=result.risk_score,
        risk_level=result.risk_level,
        gate_decision=result.gate_decision,
    )
