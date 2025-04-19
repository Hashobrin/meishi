# !/bin/sh

# poetry run uvicorn api.main:app \
#     --host=0.0.0.0 \
#     --port=8000 \
#     --log-level trace \
#     --reload

docker compose -f docker-compose.dev.yaml run --rm --entrypoint "poetry init --name demo-app --dependency fastapi --dependency uvicorn[standard]" backend

# docker-compose run --entrypoint "poetry install --no-root" demo-app
