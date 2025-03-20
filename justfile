dev:
    sudo docker compose -f docker-compose.dev.yml up --build

e2e:
    sudo docker compose -f docker-compose.test.yml up --build --abort-on-container-exit
    sudo docker compose -f docker-compose.test.yml down

down:
    sudo docker compose -f docker-compose.dev.yml down
    sudo docker compose -f docker-compose.test.yml down

clear:
    sudo docker compose -f docker-compose.dev.yml down -v

lint:
    ruff format
    ruff check --fix
    mypy