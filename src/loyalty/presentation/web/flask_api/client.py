from dishka.container import ContextWrapper
from flask import Blueprint, Response, g, jsonify, request

from loyalty.presentation.web.controller.sign_up import ClientWebSignUp, ClientWebSignUpForm
from loyalty.presentation.web.flask_api.serializer import serializer

client = Blueprint("client", __name__)


@client.route("/", methods=["POST"], strict_slashes=False)
def sign_up() -> Response:
    container: ContextWrapper = g.dishka_container_wrapper
    controller = ClientWebSignUp(container)
    form = ClientWebSignUpForm(**request.get_json())
    result = controller.execute(form)
    return jsonify(serializer.dump(result))
