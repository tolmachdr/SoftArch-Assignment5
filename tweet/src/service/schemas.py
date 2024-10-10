from datetime import datetime
from typing import Self, Any

from pydantic import BaseModel, Field


class TweetSchema(BaseModel):
    id: str
    author_id: str
    text: str = Field(max_length=400)
    created_at: datetime
    likes_count: int

    @classmethod
    def build_from_orm(cls, obj, likes: int) -> Self:
        return cls(
            id=str(obj.id),
            author_id=obj.author_id,
            text=obj.text,
            created_at=obj.created_at,
            likes_count=likes
        )


class PostTweetSchema(BaseModel):
    text: str = Field(max_length=400)
    author_id: str
