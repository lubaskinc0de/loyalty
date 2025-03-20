up:
    sudo docker compose up --build

e2e:
    sudo docker compose -f docker-compose.test.yml up --build --abort-on-container-exit

down:
    sudo docker compose down
    sudo docker compose -f docker-compose.test.yml down

clear:
    sudo docker compose down -v

lint:
    ruff format
    ruff check --fix
    mypy