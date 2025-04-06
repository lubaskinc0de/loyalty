from flask import Blueprint, Response, jsonify

root = Blueprint("root", __name__)


@root.route("/ping/", strict_slashes=False)
def ping() -> Response:
    return jsonify({"ping": "pong"})
