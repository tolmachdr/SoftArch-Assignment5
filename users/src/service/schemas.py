import datetime
from typing import Any
from typing_extensions import Self

from pydantic import BaseModel

from src.models import User


class UserSchema(BaseModel):
    id: str
    username: str
    password: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj: Any) -> Self:
        return cls(
                id=str(obj.id),
                username=obj.username,
                password=obj.password,
                created_at=obj.created_at
        )


class UserCreateEditSchema(BaseModel):
    username: str
    password: str

    def to_orm_model(self) -> User:
        return User(
                username=self.username,
                password=self.password
        )


class UserCreateEditHashedPasswordSchema(UserCreateEditSchema):
    ...


class TokenSchema(BaseModel):
    token: str
    token_type: str
    expires_in: int


class UserShowSchema(BaseModel):
    id: str
    username: str
    created_at: datetime.datetime


class UserProfileSchema(UserShowSchema):
    pass
