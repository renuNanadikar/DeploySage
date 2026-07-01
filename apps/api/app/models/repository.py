import uuid

from sqlalchemy import Column, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base


class Repository(Base):
    __tablename__ = "repositories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    github_owner = Column(String, nullable=False)
    github_repo = Column(String, nullable=False)
    default_branch = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
