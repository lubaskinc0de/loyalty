from uuid import UUID

from dishka import FromDishka
from flask import Blueprint, Response, jsonify

from loyalty.application.membership.create import CreateMembership, MembershipForm
from loyalty.application.membership.delete import DeleteMembership
from loyalty.bootstrap.di.providers.data import Body
from loyalty.presentation.web.serializer import serializer

membership = Blueprint("membership", __name__)


@membership.route("/", methods=["POST"], strict_slashes=False)
def create_membership(*, interactor: FromDishka[CreateMembership], form: Body[MembershipForm]) -> Response:
    result = interactor.execute(form.data)
    return jsonify({"membership_id": serializer.dump(result)})


@membership.route("/<uuid:membership_id>", methods=["DELETE"], strict_slashes=False)
def delete_membership(*, membership_id: UUID, interactor: FromDishka[DeleteMembership]) -> Response:
    interactor.execute(membership_id)
    return Response(status=204)
