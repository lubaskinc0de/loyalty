from dishka import FromDishka
from flask import Blueprint, Response, jsonify

from loyalty.application.client.create import ClientForm, CreateClient
from loyalty.application.client.read import ReadClient
from loyalty.application.membership.read import ReadMembership
from loyalty.bootstrap.di.providers.data import Body
from loyalty.presentation.web.serializer import serializer

client = Blueprint("client", __name__)


@client.route("/", methods=["POST"], strict_slashes=False)
def create_client(*, interactor: FromDishka[CreateClient], form: Body[ClientForm]) -> Response:
    interactor.execute(form.data)
    return Response(status=204)


@client.route("/", methods=["GET"], strict_slashes=False)
def read_client(*, interactor: FromDishka[ReadClient]) -> Response:
    result = interactor.execute()
    return jsonify(serializer.dump(result))


@client.route("/membership", methods=["GET"], strict_slashes=False)
def read_membership(*, interactor: FromDishka[ReadMembership]) -> Response:
    return jsonify(serializer.dump(interactor.execute()))
