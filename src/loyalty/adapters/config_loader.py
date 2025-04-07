import logging
import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DBConnectionConfig:
    postgres_username: str
    postgres_password: str
    postgres_host: str
    postgres_port: int
    postgres_database: str

    @property
    def postgres_conn_url(self) -> str:
        user = self.postgres_username
        password = self.postgres_password
        host = self.postgres_host
        db_name = self.postgres_database

        return f"postgresql+psycopg://{user}:{password}@{host}/{db_name}"


@dataclass(frozen=True, slots=True)
class JWTConfig:
    secret_key: str


@dataclass(frozen=True, slots=True)
class Config:
    db_connection: DBConnectionConfig
    jwt: JWTConfig

    @classmethod
    def load_from_environment(cls: type["Config"]) -> "Config":
        db = DBConnectionConfig(
            postgres_username=os.environ["POSTGRES_USERNAME"],
            postgres_password=os.environ["POSTGRES_PASSWORD"],
            postgres_host=os.environ["POSTGRES_HOST"],
            postgres_port=int(os.environ["POSTGRES_PORT"]),
            postgres_database=os.environ["POSTGRES_DATABASE"],
        )
        jwt = JWTConfig(
            secret_key=os.environ["JWT_SECRET_KEY"],
        )
        logging.debug("Config loaded.")
        return cls(
            db_connection=db,
            jwt=jwt,
        )
