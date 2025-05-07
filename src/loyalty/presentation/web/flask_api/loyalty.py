from uuid import UUID

from dishka import FromDishka
from flask import Blueprint, Response, jsonify, request

from loyalty.application.loyalty.create import CreateLoyalty, LoyaltyForm
from loyalty.application.loyalty.delete import DeleteLoyalty
from loyalty.application.loyalty.read import ReadLoyalties, ReadLoyalty
from loyalty.application.loyalty.update import UpdateLoyalty, UpdateLoyaltyForm
from loyalty.bootstrap.di.providers.data import Body
from loyalty.domain.shared_types import LoyaltyTimeFrame
from loyalty.presentation.web.serializer import serializer

loyalty = Blueprint("loyalty", __name__)


@loyalty.route("/", methods=["POST"], strict_slashes=False)
def create_loyalty(*, interactor: FromDishka[CreateLoyalty], form: Body[LoyaltyForm]) -> Response:
    loyalty_id = interactor.execute(form.data)
    return jsonify({"loyalty_id": loyalty_id})


@loyalty.route("/<uuid:loyalty_id>", methods=["GET"], strict_slashes=False)
def read_loyalty(*, loyalty_id: UUID, interactor: FromDishka[ReadLoyalty]) -> Response:
    result = interactor.execute(loyalty_id)

    return jsonify(serializer.dump(result))


@loyalty.route("/", methods=["GET"], strict_slashes=False)
def read_loyalties(*, interactor: FromDishka[ReadLoyalties]) -> Response:
    offset = request.args.get("offset", default=0, type=int)
    limit = request.args.get("limit", default=None, type=int)
    active_arg = request.args.get("active", default=None, type=int)
    time_frame_arg = request.args.get("time_frame", default="ALL", type=str)
    business_id = request.args.get("business_id", default=None, type=UUID)

    active = bool(active_arg) if active_arg is not None else None
    time_frame = LoyaltyTimeFrame[time_frame_arg.upper()]

    if limit is not None:
        result = interactor.execute(
            limit=limit,
            active=active,
            offset=offset,
            time_frame=time_frame,
            business_id=business_id,
        )
    else:
        result = interactor.execute(
            active=active,
            offset=offset,
            time_frame=time_frame,
            business_id=business_id,
        )

    return jsonify(serializer.dump(result))


@loyalty.route("/<uuid:loyalty_id>", methods=["PUT"], strict_slashes=False)
def update_loyalty(
    *,
    loyalty_id: UUID,
    interactor: FromDishka[UpdateLoyalty],
    form: Body[UpdateLoyaltyForm],
) -> Response:
    interactor.execute(loyalty_id, form.data)
    return Response(status=204)


@loyalty.route("/<uuid:loyalty_id>", methods=["DELETE"], strict_slashes=False)
def delete_loyalty(*, loyalty_id: UUID, interactor: FromDishka[DeleteLoyalty]) -> Response:
    interactor.execute(loyalty_id)
    return Response(status=204)
