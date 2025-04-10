set windows-powershell := true

dev:
    docker compose -f docker-compose.dev.yml up --build

e2e:
    docker compose -f docker-compose.test.yml up --build --abort-on-container-exit
    docker compose -f docker-compose.test.yml down

down:
    docker compose -f docker-compose.dev.yml down
    docker compose -f docker-compose.test.yml down

clear:
    docker compose -f docker-compose.dev.yml down -v

lint:
    ruff format
    ruff check --fix
    mypy