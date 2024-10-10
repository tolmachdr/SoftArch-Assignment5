from datetime import datetime

from pydantic import BaseModel

from src.service.schemas import TokenSchema, UserCreateEditSchema, UserProfileSchema


class UserLoginApiModel(BaseModel):
    username: str
    password: str

    def to_service_schema(self) -> UserCreateEditSchema:
        return UserCreateEditSchema(
                username=self.username,
                password=self.password
        )


class LoginTokenApiModel(BaseModel):
    token: str
    token_type: str
    expires_in: int

    @classmethod
    def from_service_schema(cls, service_schema: TokenSchema) -> "LoginTokenApiModel":
        values = service_schema.dict()
        return cls(**values)


class UserProfileApiModel(BaseModel):
    id: str
    username: str
    created_at: datetime

    @classmethod
    def from_service_schema(cls, service_schema: UserProfileSchema) -> "UserProfileApiModel":
        values = service_schema.dict()
        return cls(**values)
