import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.db.base import Base


class RiskScoreVersion(Base):
    __tablename__ = "risk_score_versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_run_id = Column(UUID(as_uuid=True), ForeignKey("analysis_runs.id"), nullable=False)
    risk_score = Column(Integer, nullable=False)
    risk_level = Column(String, nullable=False)
    signals = Column(JSONB)
    explanation = Column(Text)
    recommendation = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
