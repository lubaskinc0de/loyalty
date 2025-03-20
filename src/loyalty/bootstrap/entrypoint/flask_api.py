import sys

from dishka.integrations.flask import setup_dishka
from flask import Flask

from loyalty.bootstrap.di.container import get_container
from loyalty.presentation.web.flask_api.root import include_root


def main(_args: list[str]) -> None:
    flask_app = Flask(__name__)
    include_root(flask_app)

    setup_dishka(container=get_container(), app=flask_app, auto_inject=True)
    flask_app.run(port=5000, host="0.0.0.0")


if __name__ == "__main__":
    main(sys.argv)
