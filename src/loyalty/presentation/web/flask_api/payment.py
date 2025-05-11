from dishka import FromDishka
from flask import Blueprint, Response, jsonify

from loyalty.application.payment.create import CreatePayment, PaymentForm
from loyalty.bootstrap.di.providers.data import Body
from loyalty.presentation.web.serializer import serializer

payment = Blueprint("payment", __name__)


@payment.route("/", methods=["POST"], strict_slashes=False)
def create_payment(*, interactor: FromDishka[CreatePayment], form: Body[PaymentForm]) -> Response:
    result = interactor.execute(form.data)
    return jsonify(serializer.dump(result))
