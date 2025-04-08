from uuid import UUID

from dishka import FromDishka
from flask import Blueprint, Response, jsonify, request

from loyalty.application.business.create import BusinessForm, CreateBusiness
from loyalty.application.business.read import ReadBusiness
from loyalty.presentation.web.flask_api.serializer import serializer

business = Blueprint("business", __name__)


@business.route("/", methods=["POST"], strict_slashes=False)
def create_business(*, interactor: FromDishka[CreateBusiness]) -> Response:
    result = interactor.execute(BusinessForm(**request.get_json()))
    return jsonify(serializer.dump(result))


@business.route("/<uuid:business_id>", methods=["GET"], strict_slashes=False)
def read_business(business_id: UUID, interactor: FromDishka[ReadBusiness]) -> Response:
    result = interactor.execute(business_id)
    return jsonify(serializer.dump(result))
