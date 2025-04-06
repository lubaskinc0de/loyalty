from dishka import FromDishka
from flask import Blueprint, Response, jsonify
from flask_pydantic import validate  # type: ignore

from loyalty.adapters.controller.sign_up import WebSignUp, WebSignUpForm
from loyalty.presentation.web.flask_api.serializer import serializer

client = Blueprint("client", __name__)


@client.route("/", methods=["POST"], strict_slashes=False)
@validate()  # type: ignore
def sign_up(form: WebSignUpForm, controller: FromDishka[WebSignUp]) -> Response:
    result = controller.execute(form)
    return jsonify(serializer.dump(result))
