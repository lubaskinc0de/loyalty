import logging
from collections.abc import Iterator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from loyalty.adapters.config_loader import DBConnectionConfig


def get_engine(config: DBConnectionConfig) -> Iterator[Engine]:
    connection_url = config.postgres_conn_url

    engine = create_engine(
        connection_url,
        future=True,
    )

    logging.debug("Engine was created.")

    yield engine

    engine.dispose()
    logging.debug("Engine was disposed.")


def get_sessionmaker(
    engine: Engine,
) -> sessionmaker[Session]:
    session_factory = sessionmaker(
        engine,
        expire_on_commit=False,
        class_=Session,
    )

    logging.debug("sessionmaker initialized")

    return session_factory


def get_session(
    session_factory: sessionmaker[Session],
) -> Iterator[Session]:
    with session_factory() as session:
        yield session
