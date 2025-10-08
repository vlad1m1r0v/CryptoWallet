from sqlalchemy import Column, String, Boolean, LargeBinary
from sqlalchemy.dialects.postgresql import UUID

from src.infrastructure.persistence.database.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True)
    username = Column(String(64), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(LargeBinary, nullable=False)
    avatar_url = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
