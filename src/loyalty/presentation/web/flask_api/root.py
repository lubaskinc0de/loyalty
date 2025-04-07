from dishka import FromDishka
from flask import Blueprint, Response, jsonify, request

from loyalty.presentation.web.controller.login import WebLogin
from loyalty.presentation.web.controller.user import WebUserCredentials
from loyalty.presentation.web.flask_api.serializer import serializer

root = Blueprint("root", __name__)


@root.route("/ping/", strict_slashes=False)
def ping() -> Response:
    return jsonify({"ping": "pong"})


@root.route("/login/", methods=["POST"], strict_slashes=False)
def login(*, controller: FromDishka[WebLogin]) -> Response:
    form = WebUserCredentials(**request.get_json())
    result = controller.execute(form)
    return jsonify(serializer.dump(result))
