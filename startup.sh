docker-compose run \
--entrypoint "poetry init \
    --name dev-app \
    --dependency fastapi \
    --dependency uvicorn[standard]" \
dev-app

docker-compose run --entrypoint "poetry install --no-root" dev-app
