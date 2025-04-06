from flask import Flask

from loyalty.presentation.web.flask_api.client import client
from loyalty.presentation.web.flask_api.root import root


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(root)
    app.register_blueprint(client, url_prefix="/client")
