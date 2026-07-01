import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.db.base import Base


class PRSummaryVersion(Base):
    __tablename__ = "pr_summary_versions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    analysis_run_id = Column(UUID(as_uuid=True), ForeignKey("analysis_runs.id"), nullable=False)
    summary_markdown = Column(Text, nullable=False)
    key_changes = Column(JSONB)
    testing_notes = Column(Text)
    deployment_notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
