from flask import Flask
from pydantic import ValidationError

from loyalty.presentation.web.flask_api.client import client
from loyalty.presentation.web.flask_api.exc_handler import validation_error_handler
from loyalty.presentation.web.flask_api.root import root


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(root)
    app.register_blueprint(client, url_prefix="/client")


def register_error_handlers(app: Flask) -> None:
    app.register_error_handler(ValidationError, validation_error_handler)
