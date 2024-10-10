from src.service.exceptions import HttpError


class NoCredentialsError(HttpError):
    status_code = 401
    detail = "No credentials provided."
