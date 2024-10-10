import urllib.parse

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def get_base_config(env_prefix: str) -> SettingsConfigDict:
    return SettingsConfigDict(
            env_file=".env",
            env_prefix=env_prefix,
            extra="ignore",
            env_file_encoding="utf-8",
    )


class GeneralSettings(BaseSettings):
    service_name: str = Field("template", description="Service name")
    version: str = Field("0.1.0", description="Service version")

    model_config = get_base_config("app_")


class DatabaseSettings(BaseSettings):
    host: str = Field("localhost", description="PostgreSQL host")
    port: int = Field(5432, description="PostgreSQL port")
    user: str = Field("postgres", description="PostgreSQL user")
    password: str = Field("postgres", description="PostgreSQL password")
    database: str = Field("tweet", description="PostgreSQL database")

    @property
    def dsn(self):
        return (f"postgresql+psycopg2://"
                f"{self.user}:{urllib.parse.quote_plus(self.password)}@"
                f"{self.host}:{self.port}/{self.database}")

    model_config = get_base_config("db_")


class JWTSettings(BaseSettings):
    secret_key: str = Field("secret", description="JWT secret")
    algorithm: str = Field("HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(30, description="Access token expiration time in minutes")

    model_config = get_base_config("jwt_")


class UsersServiceSettings(BaseSettings):
    url: str = Field("http://localhost:8002", description="Users service URL")

    model_config = get_base_config("users_")


general_settings = GeneralSettings()  # type: ignore
database_settings = DatabaseSettings()  # type: ignore
jwt_settings = JWTSettings()  # type: ignore
users_service_settings = UsersServiceSettings()  # type: ignore
