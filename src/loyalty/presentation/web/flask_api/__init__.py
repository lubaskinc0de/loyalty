from flask import Flask
from pydantic import ValidationError

from loyalty.application.exceptions.base import ApplicationError
from loyalty.presentation.web.flask_api.bonus import bonus
from loyalty.presentation.web.flask_api.business import business
from loyalty.presentation.web.flask_api.business_branch import branch, branch_with_business
from loyalty.presentation.web.flask_api.client import client
from loyalty.presentation.web.flask_api.exc_handler import app_error_handler, validation_error_handler
from loyalty.presentation.web.flask_api.loyalty import loyalty
from loyalty.presentation.web.flask_api.membership import membership
from loyalty.presentation.web.flask_api.payment import payment
from loyalty.presentation.web.flask_api.root import root
from loyalty.presentation.web.flask_api.user import user


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(root)
    app.register_blueprint(client, url_prefix="/client")
    app.register_blueprint(business, url_prefix="/business")
    app.register_blueprint(branch_with_business, url_prefix="/business/<uuid:business_id>/branch")
    app.register_blueprint(branch, url_prefix="/branch")
    app.register_blueprint(loyalty, url_prefix="/loyalty")
    app.register_blueprint(user, url_prefix="/user")
    app.register_blueprint(membership, url_prefix="/membership")
    app.register_blueprint(payment, url_prefix="/payment")
    app.register_blueprint(bonus, url_prefix="/bonus")


def register_error_handlers(app: Flask) -> None:
    app.register_error_handler(ValidationError, validation_error_handler)
    app.register_error_handler(ApplicationError, app_error_handler)
