from dishka import Container
from flask import Blueprint, Response, g, jsonify, request

from loyalty.adapters.controller.sign_up import WebSignUp, WebSignUpForm
from loyalty.presentation.web.flask_api.serializer import serializer

client = Blueprint("client", __name__)


@client.route("/", methods=["POST"], strict_slashes=False)
def sign_up() -> Response:
    container: Container = g.dishka_container_wrapper
    controller = WebSignUp(container)
    form = WebSignUpForm(**request.get_json())
    result = controller.execute(form)
    return jsonify(serializer.dump(result))
