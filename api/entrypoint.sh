docker compose run \
    --entrypoint \
        "poetry run uvicorn api.main:app \
        --host=0.0.0.0 \
        --port=8000 \
        --log-level \
        trace \
        --reload" \
    backend

# docker-compose run --entrypoint \
#     "poetry init \
#         --name demo-app \
#         --dependency fastapi \
#         --dependency uvicorn[standard]" \
#     demo-app

# docker-compose run --entrypoint "poetry install --no-root" demo-app
