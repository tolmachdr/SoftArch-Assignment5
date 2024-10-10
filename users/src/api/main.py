from fastapi import FastAPI

from src.api.utils import router as utils_router
from src.api.users import router as users_router


def create_app():
    app = FastAPI()
    app.include_router(users_router)

    app.include_router(utils_router)

    return app
