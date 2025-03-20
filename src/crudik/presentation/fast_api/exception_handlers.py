import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import DBAPIError

from crudik.application.exceptions.base import (
    ApplicationError,
)

error_code = {
    ApplicationError: 500,
}


def get_http_error_response(
    err: ApplicationError,
) -> JSONResponse:
    err_type = type(err)
    err_http_code = error_code[err_type]

    return JSONResponse(
        status_code=err_http_code,
        content={},
    )


async def app_exception_handler(_request: Request, exc: ApplicationError) -> JSONResponse:
    return get_http_error_response(exc)


async def dbapi_error_handler(_request: Request, _exc: DBAPIError) -> JSONResponse:
    logging.exception("DBAPI Error:")
    return JSONResponse(
        status_code=400,
        content={
            "status": "db error",
        },
    )
