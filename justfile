set windows-powershell := true

up:
    just down
    docker compose -f docker-compose.dev.yml up --build

test:
    docker compose -f docker-compose.test.yml up --build --abort-on-container-exit tests
    just down

down:
    docker compose -f docker-compose.dev.yml down
    docker compose -f docker-compose.test.yml down

clear:
    docker compose -f docker-compose.dev.yml down -v

lint:
    ruff format
    ruff check --fix
    mypy

migration ARG1:
    docker exec -it api crudik migrations autogenerate {{ARG1}}

check:
    just lint
    just e2e
