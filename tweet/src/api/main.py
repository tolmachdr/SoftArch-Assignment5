from fastapi import FastAPI

from src.api.endpoints import router


def create_app():
    app = FastAPI()
    app.include_router(router)

    return app
