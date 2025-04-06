import json

from flask import Response
from pydantic import ValidationError

from loyalty.application.exceptions.base import ApplicationError
from loyalty.application.exceptions.user import UserAlreadyExistsError

status_code = {
    ApplicationError: 500,
    UserAlreadyExistsError: 409,
}

message = {
    ApplicationError: "Unhanded application error",
    UserAlreadyExistsError: "User already exists",
}

JSON_MIMETYPE = "application/json"


def validation_error_handler(e: ValidationError) -> Response:
    response = Response(e.json(), mimetype=JSON_MIMETYPE, status=422)
    return response


def app_error_handler(e: ApplicationError) -> Response:
    content = {
        "description": message[type(e)],
    }
    response = Response(json.dumps(content), status=status_code[type(e)])
    return response
