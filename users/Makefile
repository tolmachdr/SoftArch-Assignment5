
lint:
	poetry run isort .
	poetry run flake8 src
	poetry run pylint src
	poetry run mypy src

run:
	poetry run uvicorn src.api.main:create_app --host 0.0.0.0 --port 8002
