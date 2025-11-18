from typing import TYPE_CHECKING

from sqlalchemy import Column, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship

from src.infrastructure.persistence.database.models.base import Base

if TYPE_CHECKING:
    from src.infrastructure.persistence.database.models.user import User


class Permissions(Base):
    __tablename__ = "permissions"

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    has_chat_access = Column(Boolean, default=False, nullable=False)

    user: Mapped["User"] = relationship(back_populates="permissions")

