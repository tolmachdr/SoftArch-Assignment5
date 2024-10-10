from fastapi import HTTPException


class HttpError(HTTPException):
    """Base http exception."""

    status_code: int = NotImplemented
    detail: str = "Http exception."

    def __init__(self, detail: str = ""):
        """."""
        super().__init__(status_code=self.status_code, detail=detail or self.detail)


class UserNotFoundError(HttpError):
    """User not found error."""

    status_code = 404
    detail = "User not found."


class InvalidCredentialsError(HttpError):
    """Invalid credentials error."""

    status_code = 400
    detail = "Wrong password."


class UsernameAlreadyExistsError(HttpError):
    """Username already exists error."""

    status_code = 400
    detail = "Username already exists."


class ExternalServiceUnavailableError(HttpError):
    """External service unavailable error."""

    status_code = 503
    detail = "External service unavailable."
