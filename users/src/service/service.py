import datetime

import bcrypt
import httpx
import jwt
import sqlalchemy

from src.models import repository
from src.models.base import Session
from src.service.exceptions import ExternalServiceUnavailableError, UserNotFoundError, InvalidCredentialsError, \
    UsernameAlreadyExistsError
from src.service.schemas import TokenSchema, UserCreateEditHashedPasswordSchema, UserCreateEditSchema, \
    UserProfileSchema, UserSchema
from src.settings import jwt_settings


class UserService:
    def __init__(self, session: Session):
        self.session = session

    def get_user(self, user_id: str) -> UserSchema:
        return UserSchema.from_orm(repository.UserRepository(session=self.session).get_by_attr(id=user_id))

    def get_users(self, limit: int = 10, offset: int = 0) -> list[UserSchema]:
        return [
            UserSchema.from_orm(u) for u in
            repository.UserRepository(session=self.session).get_multi(limit=limit, offset=offset)
        ]

    def create_user(self, user: UserCreateEditHashedPasswordSchema) -> UserSchema:
        return UserSchema.from_orm(repository.UserRepository(session=self.session).save(user.to_orm_model()))

    @staticmethod
    def _hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def login(self, user: UserCreateEditSchema) -> TokenSchema:
        user_repo = repository.UserRepository(session=self.session)
        user_orm = user_repo.get_by_attr(username=user.username)
        if not user_orm:
            raise UserNotFoundError()
        if not bcrypt.checkpw(user.password.encode('utf-8'), user_orm.password.encode('utf-8')):
            raise InvalidCredentialsError()
        token = self._create_jwt_token(user_orm.id)
        return TokenSchema(token=token, token_type="bearer", expires_in=3600)

    @staticmethod
    def _create_jwt_token(user_id: str) -> str:
        expire = datetime.datetime.now() + datetime.timedelta(minutes=jwt_settings.access_token_expire_minutes)

        payload = {
            "sub": str(user_id),
            "exp": expire
        }

        token = jwt.encode(payload, jwt_settings.secret_key, algorithm=jwt_settings.algorithm)

        return token

    def register(self, user_create: UserCreateEditSchema) -> None:
        user = UserCreateEditHashedPasswordSchema(
                username=user_create.username,
                password=self._hash_password(user_create.password)
        )
        try:
            self.create_user(user)
        except sqlalchemy.exc.IntegrityError:
            raise UsernameAlreadyExistsError

    def profile(self, user_id: str) -> UserProfileSchema:
        user = self.get_user(user_id)
        return UserProfileSchema(**user.dict())

    @staticmethod
    def decode_jwt(token: str) -> dict:
        return jwt.decode(token, jwt_settings.secret_key, algorithms=[jwt_settings.algorithm])
