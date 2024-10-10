import datetime
import uuid
from uuid import UUID

from sqlalchemy import Column, DateTime, String
from sqlalchemy.orm import Mapped

from src.models.base import Base


class CreatedAtMixin:
    created_at: Mapped[datetime.datetime] = Column(DateTime,
                                                   nullable=False,
                                                   server_default="now()")


class UUIDMixin:
    id: Mapped[UUID] = Column(String, primary_key=True, default=uuid.uuid4)


class User(Base, CreatedAtMixin, UUIDMixin):
    __tablename__ = "user"

    username: str = Column(String, unique=True)
    password: str = Column(String, nullable=False)
