from collections.abc import Sequence
from uuid import UUID

from dishka import FromDishka
from flask import Blueprint, Response, jsonify, request

from loyalty.application.membership.create import CreateMembership, MembershipForm
from loyalty.application.membership.delete import DeleteMembership
from loyalty.application.membership.read import ReadMembership, ReadMemberships
from loyalty.bootstrap.di.providers.data import Body
from loyalty.domain.entity.membership import LoyaltyMembership
from loyalty.presentation.web.serializer import serializer

membership = Blueprint("membership", __name__)


@membership.route("/", methods=["POST"], strict_slashes=False)
def create_membership(*, interactor: FromDishka[CreateMembership], form: Body[MembershipForm]) -> Response:
    result = interactor.execute(form.data)
    return jsonify({"membership_id": serializer.dump(result)})


@membership.route("/<uuid:membership_id>", methods=["GET"], strict_slashes=False)
def read_membership(*, membership_id: UUID, interactor: FromDishka[ReadMembership]) -> Response:
    return jsonify(serializer.dump(interactor.execute(membership_id)))


@membership.route("/", methods=["GET"], strict_slashes=False)
def read_memberships(*, interactor: FromDishka[ReadMemberships]) -> Response:
    offset = request.args.get("offset", default=0, type=int)
    limit = request.args.get("limit", default=None, type=int)
    result = interactor.execute(offset, limit) if limit else interactor.execute(offset)

    return jsonify(serializer.dump(result, Sequence[LoyaltyMembership]))


@membership.route("/<uuid:membership_id>", methods=["DELETE"], strict_slashes=False)
def delete_membership(*, membership_id: UUID, interactor: FromDishka[DeleteMembership]) -> Response:
    interactor.execute(membership_id)
    return Response(status=204)
