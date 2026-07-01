import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base


class AnalysisRun(Base):
    __tablename__ = "analysis_runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pull_request_id = Column(UUID(as_uuid=True), ForeignKey("pull_requests.id"), nullable=False)
    commit_sha = Column(String, nullable=False)
    workflow_run_id = Column(String)
    analysis_version = Column(Integer, nullable=False)
    status = Column(String, nullable=False)
    model_name = Column(String)
    prompt_version = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
