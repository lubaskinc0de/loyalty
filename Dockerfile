FROM python:3.13.1-slim

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

ENV APP_HOME=/home/app/
WORKDIR $APP_HOME

RUN mkdir ./src

RUN pip install uv
COPY ./pyproject.toml $APP_HOME
RUN uv pip install -e . --system

COPY ./src/ $APP_HOME/src/
