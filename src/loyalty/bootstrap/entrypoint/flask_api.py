import logging
import multiprocessing
import sys

import gunicorn.app.wsgiapp  # type: ignore
from dishka.integrations.flask import setup_dishka
from flask import Flask
from flask_json import FlaskJSON  # type: ignore

from loyalty.bootstrap.di.container import get_container
from loyalty.presentation.web.flask_api import register_blueprints, register_error_handlers


def setup_logging() -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


json_app = FlaskJSON()
flask_app = Flask(__name__)
flask_app.config["JSON_JSONIFY_HTTP_ERRORS"] = True
json_app.init_app(flask_app)


def main(_args: list[str]) -> None:
    setup_logging()

    register_blueprints(flask_app)
    register_error_handlers(flask_app)
    setup_dishka(container=get_container(), app=flask_app, auto_inject=True)

    sys.argv = [
        "gunicorn",
        "-b",
        "0.0.0.0:5000",
        "-w",
        str(multiprocessing.cpu_count() * 2),
        "--log-level",
        "info",
        "--access-logfile",
        "-",
        "--error-logfile",
        "-",
        "--capture-output",
        "--enable-stdio-inheritance",
        "loyalty.bootstrap.entrypoint.flask_api:flask_app",
    ]

    gunicorn_logger = logging.getLogger("gunicorn.error")
    flask_app.logger.handlers = gunicorn_logger.handlers
    flask_app.logger.setLevel(gunicorn_logger.level)

    root_logger = logging.getLogger()
    root_logger.handlers = gunicorn_logger.handlers

    gunicorn.app.wsgiapp.run()


if __name__ == "__main__":
    main(sys.argv)
