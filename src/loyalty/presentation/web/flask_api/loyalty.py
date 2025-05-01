from uuid import UUID

from dishka import FromDishka
from flask import Blueprint, Response, jsonify, request

from loyalty.application.data_model.loyalty import LoyaltyForm
from loyalty.application.loyalty.create import CreateLoyalty
from loyalty.application.loyalty.delete import DeleteLoyalty
from loyalty.application.loyalty.read import ReadLoyalties, ReadLoyalty
from loyalty.application.loyalty.update import UpdateLoyalty
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
    time_frame = request.args.get("time_frame", default=LoyaltyTimeFrame.ALL, type=LoyaltyTimeFrame)
    business_id = request.args.get("business_id", default=None, type=UUID)

    result = interactor.execute(
        limit=limit,
        offset=offset,
        time_frame=time_frame,
        business_id=business_id,
    )

    loyalties: list[Loyalty] = [serializer.dump(loyalty) for loyalty in result.loyalties]

    return jsonify({"loyalties": loyalties})


@loyalty.route("/<uuid:loyalty_id>", methods=["PUT"], strict_slashes=False)
def update_loyalty(*, loyalty_id: UUID, interactor: FromDishka[UpdateLoyalty]) -> Response:
    interactor.execute(loyalty_id, LoyaltyForm(**request.get_json()))
    return Response(status=204)


@loyalty.route("/<uuid:loyalty_id>", methods=["DELETE"], strict_slashes=False)
def delete_loyalty(*, loyalty_id: UUID, interactor: FromDishka[DeleteLoyalty]) -> Response:
    interactor.execute(loyalty_id)
    return Response(status=204)
