from dishka import FromDishka
from dishka.container import ContextWrapper
from flask import Blueprint, Response, g, jsonify, request

from loyalty.adapters.auth.provider import WebUserCredentials
from loyalty.application.user.read import ReadUser
from loyalty.presentation.web.controller.login import WebLogin
from loyalty.presentation.web.controller.sign_up import WebSignUp
from loyalty.presentation.web.flask_api.serializer import serializer

user = Blueprint("user", __name__)


@user.route("/login", methods=["POST"], strict_slashes=False)
def login(*, controller: FromDishka[WebLogin]) -> Response:
    form = WebUserCredentials(**request.get_json())
    result = controller.execute(form)
    return jsonify(serializer.dump(result))


@user.route("/web", methods=["POST"], strict_slashes=False)
def web_sign_up() -> Response:
    container: ContextWrapper = g.dishka_container_wrapper
    controller = WebSignUp(container)
    form = WebUserCredentials(**request.get_json())
    result = controller.execute(form)
    return jsonify(serializer.dump(result))


@user.route("/", methods=["GET"], strict_slashes=False)
def read_user(*, interactor: FromDishka[ReadUser]) -> Response:
    result = interactor.execute()
    return jsonify(serializer.dump(result))
