import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base


class FailureAnalysisVersion(Base):
    __tablename__ = "failure_analysis_versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_run_id = Column(UUID(as_uuid=True), ForeignKey("analysis_runs.id"), nullable=False)
    failure_type = Column(String)
    root_cause = Column(Text)
    suggested_fix = Column(Text)
    confidence = Column(Numeric)
    raw_log_excerpt = Column(Text)
    cleaned_log_excerpt = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
