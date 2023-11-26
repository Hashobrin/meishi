docker-compose run --entrypoint \
    "poetry run uvicorn api.main:app --host 0.0.0.0 --reload" dev-app

docker-compose run --entrypoint \
    "poetry init \
        --name dev-app \
        --dependency fastapi \
        --dependency uvicorn[standard]" \
    dev-app

docker-compose run --entrypoint "poetry install --no-root" dev-app
