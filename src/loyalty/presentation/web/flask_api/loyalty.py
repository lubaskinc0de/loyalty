from uuid import UUID

from dishka import FromDishka
from flask import Blueprint, Response, jsonify, request

from loyalty.application.loyalty.create import CreateLoyalty, LoyaltyForm
from loyalty.application.loyalty.delete import DeleteLoyalty
from loyalty.application.loyalty.read import ReadLoyalties, ReadLoyalty
from loyalty.application.loyalty.update import UpdateLoyalty, UpdateLoyaltyForm
from loyalty.domain.entity.loyalty import Loyalty
from loyalty.domain.shared_types import LoyaltyTimeFrame
from loyalty.presentation.web.serializer import serializer

loyalty = Blueprint("loyalty", __name__)

DEFAULT_LOYALTIES_PAGE_LIMIT = 10


@loyalty.route("/", methods=["POST"], strict_slashes=False)
def create_loyalty(*, interactor: FromDishka[CreateLoyalty]) -> Response:
    loyalty_id = interactor.execute(LoyaltyForm(**request.get_json()))
    return jsonify({"loyalty_id": loyalty_id})


@loyalty.route("/<uuid:loyalty_id>", methods=["GET"], strict_slashes=False)
def read_loyalty(*, loyalty_id: UUID, interactor: FromDishka[ReadLoyalty]) -> Response:
    result = interactor.execute(loyalty_id)

    return jsonify(serializer.dump(result))


@loyalty.route("/", methods=["GET"], strict_slashes=False)
def read_loyalties(*, interactor: FromDishka[ReadLoyalties]) -> Response:
    offset = request.args.get("offset", default=0, type=int)
    limit = request.args.get("limit", default=DEFAULT_LOYALTIES_PAGE_LIMIT, type=int)
    active_arg = request.args.get("active", default=None, type=int)
    time_frame_arg = request.args.get("time_frame", default="ALL", type=str)
    business_id = request.args.get("business_id", default=None, type=UUID)

    active = bool(active_arg) if active_arg is not None else None
    time_frame = LoyaltyTimeFrame[time_frame_arg.upper()]

    result = interactor.execute(
        limit=limit,
        active=active,
        offset=offset,
        time_frame=time_frame,
        business_id=business_id,
    )

    loyalties: list[Loyalty] = [serializer.dump(loyalty) for loyalty in result.loyalties]

    return jsonify({"loyalties": loyalties})


@loyalty.route("/<uuid:loyalty_id>", methods=["PUT"], strict_slashes=False)
def update_loyalty(*, loyalty_id: UUID, interactor: FromDishka[UpdateLoyalty]) -> Response:
    interactor.execute(loyalty_id, UpdateLoyaltyForm(**request.get_json()))
    return Response(status=204)


@loyalty.route("/<uuid:loyalty_id>", methods=["DELETE"], strict_slashes=False)
def delete_loyalty(*, loyalty_id: UUID, interactor: FromDishka[DeleteLoyalty]) -> Response:
    interactor.execute(loyalty_id)
    return Response(status=204)
