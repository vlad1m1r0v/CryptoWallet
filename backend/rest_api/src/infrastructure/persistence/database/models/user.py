from typing import List, TYPE_CHECKING

from sqlalchemy import Column, String, Boolean, LargeBinary, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, relationship

from src.infrastructure.persistence.database.models.base import Base

if TYPE_CHECKING:
    from src.infrastructure.persistence.database.models.wallet import Wallet
    from src.infrastructure.persistence.database.models.permissions import Permissions


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True)
    username = Column(String(32), nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True, index=True)
    password_hash = Column(LargeBinary, nullable=False)
    avatar_filename = Column(String(50), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    total_messages = Column(Integer, default=0, nullable=False)

    wallets: Mapped[List["Wallet"]] = relationship(
        back_populates="user",
        uselist=True,
        cascade="all, delete-orphan",
    )

    permissions: Mapped["Permissions"] = relationship(back_populates="user")
