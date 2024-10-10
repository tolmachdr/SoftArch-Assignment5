# User service

## How to install

1) Install poetry
2) Run `poetry install`
3) Run `docker compose up`
4) Run `poetry run uvicorn src.api.main:create_app --host 0.0.0.0 --port 8001`
5) Open `http://localhost:8001/docs` in your browser

## How to run linter

1) Run `make lint`
