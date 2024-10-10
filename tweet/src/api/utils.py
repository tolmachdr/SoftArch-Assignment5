from typing import Annotated

import httpx as httpx
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from httpx import Headers

from src.settings import users_service_settings

bearer_scheme = HTTPBearer(
        scheme_name="Bearer",
        description="Your JSON Web Token (JWT)",
        bearerFormat="JWT",
        auto_error=False,
)


def get_current_user_id(
        bearer: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)) -> str:
    if not bearer:
        raise HTTPException(status_code=401, detail="No credentials provided.")
    request = httpx.post(f"{users_service_settings.url}/users/profile",
                        headers={'Authorization': f"Bearer {bearer.credentials}"})
    try:
        request.raise_for_status()
    except httpx.HTTPStatusError:
        print(request.json())
        raise HTTPException(status_code=401, detail="Error authorizing")
    return request.json()['id']


CURRENT_USER_ID_DEPENDENCY = Annotated[str, Depends(get_current_user_id)]
