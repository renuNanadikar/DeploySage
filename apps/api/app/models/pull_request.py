import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base


class PullRequest(Base):
    __tablename__ = "pull_requests"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    repository_id = Column(UUID(as_uuid=True), ForeignKey("repositories.id"), nullable=False)
    pr_number = Column(Integer, nullable=False)
    title = Column(String)
    author = Column(String)
    base_branch = Column(String)
    head_branch = Column(String)
    latest_commit_sha = Column(String)
    state = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
