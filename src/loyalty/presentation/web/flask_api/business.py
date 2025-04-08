from dishka import FromDishka
from flask import Blueprint, Response, jsonify, request

from loyalty.application.business.create_business import BusinessForm, CreateBusiness
from loyalty.presentation.web.flask_api.serializer import serializer

business = Blueprint("business", __name__)


@business.route("/", methods=["POST"], strict_slashes=False)
def create_business(*, interactor: FromDishka[CreateBusiness]) -> Response:
    result = interactor.execute(BusinessForm(**request.get_json()))
    return jsonify(serializer.dump(result))
