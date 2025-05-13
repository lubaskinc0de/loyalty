from uuid import UUID

from dishka import FromDishka
from flask import Blueprint, Response, jsonify

from loyalty.application.payment.create import CreatePayment, PaymentForm
from loyalty.application.payment.delete import DeletePayment
from loyalty.application.payment.read import ReadPayment
from loyalty.bootstrap.di.providers.data import Body
from loyalty.presentation.web.serializer import serializer

payment = Blueprint("payment", __name__)


@payment.route("/", methods=["POST"], strict_slashes=False)
def create_payment(*, interactor: FromDishka[CreatePayment], form: Body[PaymentForm]) -> Response:
    result = interactor.execute(form.data)
    return jsonify(serializer.dump(result))


@payment.route("/<uuid:payment_id>", methods=["DELETE"], strict_slashes=False)
def delete_payment(*, interactor: FromDishka[DeletePayment], payment_id: UUID) -> Response:
    interactor.execute(payment_id)
    return Response(status=204)


@payment.route("/<uuid:payment_id>", methods=["GET"], strict_slashes=False)
def read_payment(*, interactor: FromDishka[ReadPayment], payment_id: UUID) -> Response:
    return jsonify(serializer.dump(interactor.execute(payment_id)))
