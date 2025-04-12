from uuid import UUID

from dishka import FromDishka
from flask import Blueprint, Response, jsonify, request

from loyalty.application.business.create import BusinessForm, CreateBusiness
from loyalty.application.business.read import ReadBusiness, ReadBusinessBranches
from loyalty.presentation.web.serializer import serializer

business = Blueprint("business", __name__)

DEFAULT_BRANCHES_PAGE_LIMIT = 10


@business.route("/", methods=["POST"], strict_slashes=False)
def create_business(*, interactor: FromDishka[CreateBusiness]) -> Response:
    interactor.execute(BusinessForm(**request.get_json()))
    return Response(status=204)


@business.route("/<uuid:business_id>", methods=["GET"], strict_slashes=False)
def read_business(business_id: UUID, interactor: FromDishka[ReadBusiness]) -> Response:
    result = interactor.execute(business_id)
    return jsonify(serializer.dump(result))


@business.route("/<uuid:business_id>/branches", methods=["GET"], strict_slashes=False)
def read_business_branches(business_id: UUID, interactor: FromDishka[ReadBusinessBranches]) -> Response:
    offset = request.args.get("offset", default=0, type=int)
    limit = request.args.get("limit", default=DEFAULT_BRANCHES_PAGE_LIMIT, type=int)
    result = interactor.execute(
        business_id=business_id,
        limit=limit,
        offset=offset,
    )
    return jsonify({"branches": result.business_branches})
