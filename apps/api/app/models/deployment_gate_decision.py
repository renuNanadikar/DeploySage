import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base


class DeploymentGateDecision(Base):
    __tablename__ = "deployment_gate_decisions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_run_id = Column(UUID(as_uuid=True), ForeignKey("analysis_runs.id"), nullable=False)
    decision = Column(String, nullable=False)
    reason = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
