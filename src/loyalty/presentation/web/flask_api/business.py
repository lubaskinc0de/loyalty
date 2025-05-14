from uuid import UUID

from dishka import FromDishka
from flask import Blueprint, Response, jsonify

from loyalty.application.business.create import BusinessForm, CreateBusiness
from loyalty.application.business.read import PreviewBusiness, ReadBusiness
from loyalty.bootstrap.di.providers.data import Body
from loyalty.presentation.web.serializer import serializer

business = Blueprint("business", __name__)


@business.route("/", methods=["POST"], strict_slashes=False)
def create_business(*, interactor: FromDishka[CreateBusiness], form: Body[BusinessForm]) -> Response:
    interactor.execute(form.data)
    return Response(status=204)


@business.route("/<uuid:business_id>", methods=["GET"], strict_slashes=False)
def read_business(business_id: UUID, interactor: FromDishka[ReadBusiness]) -> Response:
    result = interactor.execute(business_id)
    return jsonify(serializer.dump(result))


@business.route("/", methods=["GET"], strict_slashes=False)
def read_businesses(*, interactor: FromDishka[PreviewBusiness]) -> Response:
    result = interactor.execute()

    return jsonify(serializer.dump(result))
