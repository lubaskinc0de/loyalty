from flask import Response
from pydantic import ValidationError


def validation_error_handler(e: ValidationError) -> Response:
    response = Response(e.json(), mimetype="application/json", status=422)
    return response
