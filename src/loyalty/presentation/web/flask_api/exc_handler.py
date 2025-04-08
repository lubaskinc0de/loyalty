import json

from flask import Response
from pydantic import ValidationError

from loyalty.adapters.auth.idp.error import UnauthorizedError
from loyalty.application.exceptions.base import AccessDeniedError, ApplicationError
from loyalty.application.exceptions.business import BusinessAlreadyExistsError, BusinessDoesNotExistsError
from loyalty.application.exceptions.client import ClientAlreadyExistsError
from loyalty.application.exceptions.user import UserAlreadyExistsError

ERROR_HTTP_CODE = {
    ApplicationError: 500,
    UserAlreadyExistsError: 409,
    BusinessAlreadyExistsError: 409,
    AccessDeniedError: 403,
    UnauthorizedError: 401,
    ClientAlreadyExistsError: 409,
    BusinessDoesNotExistsError: 404,
}

ERROR_MESSAGE = {
    ApplicationError: "Unhanded application error",
    UserAlreadyExistsError: "User already exists",
    BusinessAlreadyExistsError: "Business already exists",
    AccessDeniedError: "Access denied",
    UnauthorizedError: "Your aren't authorized",
    ClientAlreadyExistsError: "Client already exists",
    BusinessDoesNotExistsError: "Business does not exists",
}

ERROR_CODE = {
    ApplicationError: "UNHANDLED",
    UserAlreadyExistsError: "USER_ALREADY_EXISTS",
    BusinessAlreadyExistsError: "BUSINESS_ALREADY_EXISTS",
    AccessDeniedError: "ACCESS_DENIED",
    UnauthorizedError: "UNAUTHORIZED",
    ClientAlreadyExistsError: "CLIENT_ALREADY_EXISTS",
    BusinessDoesNotExistsError: "BUSINESS_DOES_NOT_EXISTS",
}

JSON_MIMETYPE = "application/json"


def validation_error_handler(e: ValidationError) -> Response:
    response = Response(e.json(), mimetype=JSON_MIMETYPE, status=422)
    return response


def app_error_handler(e: ApplicationError) -> Response:
    content = {
        "description": ERROR_MESSAGE[type(e)],
        "unique_code": ERROR_CODE[type(e)],
    }
    response = Response(json.dumps(content), mimetype=JSON_MIMETYPE, status=ERROR_HTTP_CODE[type(e)])
    return response
