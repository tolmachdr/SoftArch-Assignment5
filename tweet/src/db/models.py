import uuid
from uuid import UUID

from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.functions import func

from src.db.base import Base


class CreatedAtMixin:
    created_at = Column(DateTime, default=func.now())


class UUIDMixin:
    id: Mapped[UUID] = Column(String, primary_key=True, default=uuid.uuid4)


class Tweet(Base, CreatedAtMixin, UUIDMixin):
    __tablename__ = "tweets"

    author_id: UUID = Column(String, nullable=False)
    text: str = Column(Text, nullable=False)


class Likes(Base, CreatedAtMixin, UUIDMixin):
    __tablename__ = "likes"

    user_id: UUID = Column(String, nullable=False)
    tweet_id: UUID = Column(String, nullable=False)
