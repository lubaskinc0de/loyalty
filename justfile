set windows-powershell := true

dev:
    just down
    docker compose -f docker-compose.dev.yml up --build

e2e:
    docker compose -f docker-compose.test.yml up --build --abort-on-container-exit
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