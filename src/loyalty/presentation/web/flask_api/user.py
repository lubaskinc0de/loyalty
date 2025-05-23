from dishka import FromDishka
from dishka.container import ContextWrapper
from flask import Blueprint, Response, g, jsonify

from loyalty.adapters.auth.provider import WebUserCredentials
from loyalty.application.user.read import ReadUser
from loyalty.bootstrap.di.providers.data import Body
from loyalty.presentation.web.controller.login import WebLogin
from loyalty.presentation.web.controller.logout import Logout
from loyalty.presentation.web.controller.sign_up import WebSignUp
from loyalty.presentation.web.serializer import serializer

user = Blueprint("user", __name__)


@user.route("/login", methods=["POST"], strict_slashes=False)
def login(*, controller: FromDishka[WebLogin], form: Body[WebUserCredentials]) -> Response:
    result = controller.execute(form.data)
    return jsonify(serializer.dump(result))


@user.route("/web", methods=["POST"], strict_slashes=False)
def web_sign_up(form: Body[WebUserCredentials]) -> Response:
    container: ContextWrapper = g.dishka_container_wrapper
    controller = WebSignUp(container)
    result = controller.execute(form.data)
    return jsonify(serializer.dump(result))


@user.route("/", methods=["GET"], strict_slashes=False)
def read_user(*, interactor: FromDishka[ReadUser]) -> Response:
    result = interactor.execute()
    dumped = serializer.dump(result)
    return jsonify(dumped)


@user.route("/logout", methods=["DELETE"], strict_slashes=False)
def logout(*, interactor: FromDishka[Logout]) -> Response:
    interactor.execute()
    return Response(status=204)
