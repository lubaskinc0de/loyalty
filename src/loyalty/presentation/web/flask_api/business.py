from dishka.container import ContextWrapper
from flask import Blueprint, Response, g, jsonify, request

from loyalty.presentation.web.controller.sign_up_business import BusinessWebSignUp, BusinessWebSignUpForm
from loyalty.presentation.web.flask_api.serializer import serializer

business = Blueprint("client", __name__)


@business.route("/", methods=["POST"], strict_slashes=False)
def sign_up() -> Response:
    container: ContextWrapper = g.dishka_container_wrapper
    controller = BusinessWebSignUp(container)
    form = BusinessWebSignUpForm(**request.get_json())
    result = controller.execute(form)
    return jsonify(serializer.dump(result))
