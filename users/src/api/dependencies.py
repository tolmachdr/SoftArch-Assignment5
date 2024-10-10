from typing import Annotated

import sqlalchemy.orm
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.api.exceptions import NoCredentialsError
from src.models.base import session_scope
from src.service import service

bearer_scheme = HTTPBearer(
        scheme_name="Bearer",
        description="Your JSON Web Token (JWT)",
        bearerFormat="JWT",
        auto_error=False,
)


def get_session():
    with session_scope() as session:
        yield session


def get_current_user_id(
        bearer: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> int:
    if not bearer:
        raise NoCredentialsError()
    token = bearer.credentials
    decoded_token = service.UserService.decode_jwt(token)
    return decoded_token["sub"]


CURRENT_USER_ID_DEPENDENCY = Annotated[int, Depends(get_current_user_id)]
