from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.dependencies import CURRENT_USER_ID_DEPENDENCY, get_session
from src.api.schemas import LoginTokenApiModel, UserLoginApiModel, UserProfileApiModel
from src.service import service

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/login")
def login(user: UserLoginApiModel, session: Session = Depends(get_session)) -> LoginTokenApiModel:
    return LoginTokenApiModel.from_service_schema(service.UserService(session).login(user.to_service_schema()))


@router.post("/register")
def register(user: UserLoginApiModel, session: Session = Depends(get_session)) -> None:
    service.UserService(session).register(user.to_service_schema())


@router.post("/profile")
def profile(user_id: CURRENT_USER_ID_DEPENDENCY, session: Session = Depends(get_session)) -> UserProfileApiModel:
    return UserProfileApiModel.from_service_schema(service.UserService(session).profile(user_id))
