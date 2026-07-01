import uuid

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.analysis_run import AnalysisRun


def get_next_analysis_version(db: Session, pull_request_id: uuid.UUID) -> int:
    latest = (
        db.query(func.max(AnalysisRun.analysis_version))
        .filter(AnalysisRun.pull_request_id == pull_request_id)
        .scalar()
    )
    return (latest or 0) + 1
