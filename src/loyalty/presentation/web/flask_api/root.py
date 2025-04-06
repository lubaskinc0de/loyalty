from flask import Blueprint

root = Blueprint("root", __name__)


@root.route("/ping/")
def ping() -> str:
    return "pong"
