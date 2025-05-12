from collections.abc import Sequence
from uuid import UUID

from dishka import FromDishka
from flask import Blueprint, Response, jsonify, request

from loyalty.application.membership.create import CreateMembership, MembershipForm
from loyalty.application.membership.delete import DeleteMembership
from loyalty.application.membership.dto import MembershipData
from loyalty.application.membership.read import ReadMembership, ReadMemberships
from loyalty.application.shared_types import DEFAULT_LIMIT, DEFAULT_OFFSET
from loyalty.bootstrap.di.providers.data import Body
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
    offset = request.args.get("offset", default=DEFAULT_OFFSET, type=int)
    limit = request.args.get("limit", default=DEFAULT_LIMIT, type=int)
    business_id = request.args.get("business_id", default=None, type=UUID)
    result = interactor.execute(offset, limit, business_id)

    return jsonify(serializer.dump(result, Sequence[MembershipData]))


@membership.route("/<uuid:membership_id>", methods=["DELETE"], strict_slashes=False)
def delete_membership(*, membership_id: UUID, interactor: FromDishka[DeleteMembership]) -> Response:
    interactor.execute(membership_id)
    return Response(status=204)
