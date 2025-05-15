FROM python:3.13.3-alpine3.21

RUN apk add --no-cache curl

ENV APP_HOME=/home/app/
WORKDIR $APP_HOME

RUN mkdir ./src

RUN pip install uv
COPY ./pyproject.toml $APP_HOME
RUN uv pip install -e . --system

COPY ./src/ $APP_HOME/src/
