from typing import Generic, TypeVar

import sqlalchemy
from sqlalchemy import desc
from sqlalchemy.orm import Session

from src.db import Tweet, Likes
from src.db import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):

    orm_model: T

    def __init__(self, session: Session):
        self.session = session

    def get_by_attr(self, **kwargs):
        stmt = sqlalchemy.select(self.orm_model).filter_by(**kwargs)
        return self.session.execute(stmt).scalars().first()

    def get_multi(self, limit: int = 10, offset: int = 0, **kwargs):
        stmt = sqlalchemy.select(self.orm_model).filter_by(**kwargs).order_by(desc('created_at')).limit(limit).offset(offset)
        return self.session.execute(stmt).scalars().all()

    def save(self, obj: T):
        self.session.add(obj)
        self.session.flush()
        return obj

    def delete(self, obj: T):
        self.session.delete(obj)
        self.session.flush()

    def update(self, obj: T):
        self.session.merge(obj)
        self.session.flush()


class TweetRepository(BaseRepository[Tweet]):
    orm_model = Tweet


class LikesRepository(BaseRepository[Likes]):
    orm_model = Likes

    def get_likes(self, tweet_id):
        stmt = sqlalchemy.select(self.orm_model).filter_by(tweet_id=tweet_id)
        return len(self.session.execute(stmt).scalars().all())
