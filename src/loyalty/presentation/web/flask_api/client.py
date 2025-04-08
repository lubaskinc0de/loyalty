from dishka import FromDishka
from flask import Blueprint, Response, jsonify, request

from loyalty.application.client.create import ClientForm, CreateClient
from loyalty.application.client.read import ReadClient
from loyalty.presentation.web.serializer import serializer

client = Blueprint("client", __name__)


@client.route("/", methods=["POST"], strict_slashes=False)
def create_client(*, interactor: FromDishka[CreateClient]) -> Response:
    interactor.execute(ClientForm(**request.get_json()))
    return Response(status=204)


@client.route("/", methods=["GET"], strict_slashes=False)
def read_client(*, interactor: FromDishka[ReadClient]) -> Response:
    result = interactor.execute()
    return jsonify(serializer.dump(result))
