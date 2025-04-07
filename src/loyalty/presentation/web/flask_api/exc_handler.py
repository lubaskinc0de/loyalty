import json

from flask import Response
from pydantic import ValidationError

from loyalty.application.exceptions.base import ApplicationError
from loyalty.application.exceptions.business import BusinessAlreadyExistsError
from loyalty.application.exceptions.user import UserAlreadyExistsError

status_code = {
    ApplicationError: 500,
    UserAlreadyExistsError: 409,
    BusinessAlreadyExistsError: 409,
}

message = {
    ApplicationError: "Unhanded application error",
    UserAlreadyExistsError: "User already exists",
    BusinessAlreadyExistsError: "Business already exists",
}

error_code = {
    ApplicationError: "UNHANDLED",
    UserAlreadyExistsError: "USER_ALREADY_EXISTS",
    BusinessAlreadyExistsError: "BUSINESS_ALREADY_EXISTS",
}

JSON_MIMETYPE = "application/json"


def validation_error_handler(e: ValidationError) -> Response:
    response = Response(e.json(), mimetype=JSON_MIMETYPE, status=422)
    return response


def app_error_handler(e: ApplicationError) -> Response:
    content = {
        "description": message[type(e)],
        "unique_code": error_code[type(e)],
    }
    response = Response(json.dumps(content), status=status_code[type(e)])
    return response
