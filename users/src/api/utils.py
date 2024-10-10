from fastapi import APIRouter

from src.settings import general_settings

router = APIRouter()


@router.get("/")
def root():
    return {
        "service": general_settings.service_name,
        "version": general_settings.version,
    }


@router.get("/healthz")
def healthz():
    return {"status": "ok"}


@router.get("/livez")
def livez():
    return {"status": "ok"}


@router.get("/readyz")
def readyz():
    return {"status": "ok"}
