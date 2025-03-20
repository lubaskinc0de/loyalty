import logging

from fastapi import FastAPI
from sqlalchemy.exc import DBAPIError

from crudik.application.exceptions.base import ApplicationError
from crudik.presentation.fast_api.endpoint.root import router as root_router
from crudik.presentation.fast_api.exception_handlers import (
    app_exception_handler,
    dbapi_error_handler,
)


def include_routers(app: FastAPI) -> None:
    app.include_router(root_router)
    logging.debug("Routers was included.")


def include_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ApplicationError, app_exception_handler)  # type: ignore
    app.add_exception_handler(DBAPIError, dbapi_error_handler)  # type: ignore
    logging.debug("Exception handlers was included.")


__all__ = [
    "include_exception_handlers",
    "include_routers",
]
