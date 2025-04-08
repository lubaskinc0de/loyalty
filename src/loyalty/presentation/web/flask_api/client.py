from dishka import FromDishka
from flask import Blueprint, Response, jsonify, request

from loyalty.application.client.create import ClientForm, CreateClient
from loyalty.application.client.read import ReadClient
from loyalty.presentation.web.flask_api.serializer import serializer

client = Blueprint("client", __name__)


@client.route("/", methods=["POST"], strict_slashes=False)
def create_client(*, interactor: FromDishka[CreateClient]) -> Response:
    result = interactor.execute(ClientForm(**request.get_json()))
    return jsonify(serializer.dump(result))


@client.route("/", methods=["GET"], strict_slashes=False)
def read_client(*, interactor: FromDishka[ReadClient]) -> Response:
    result = interactor.execute()
    return jsonify(serializer.dump(result))
