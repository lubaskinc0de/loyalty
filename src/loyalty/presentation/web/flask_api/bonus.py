from decimal import Decimal
from uuid import UUID

from dishka import FromDishka
from flask import Blueprint, Response, jsonify, request

from loyalty.application.bonus.discount import CalcDiscount, CalcDiscountData
from loyalty.application.bonus.read import ReadBonuses
from loyalty.presentation.web.serializer import serializer

bonus = Blueprint("bonus", __name__)


@bonus.route("/<uuid:membership_id>", methods=["GET"], strict_slashes=False)
def read_bonuses(membership_id: UUID, interactor: FromDishka[ReadBonuses]) -> Response:
    result = interactor.execute(membership_id)
    return jsonify(serializer.dump(result))


@bonus.route("/discount", methods=["GET"], strict_slashes=False)
def calc_discount(interactor: FromDishka[CalcDiscount]) -> Response:
    membership_id = request.args.get("membership_id", type=UUID)
    purchase_amount = request.args.get("purchase_amount", type=Decimal)

    calc_discount_data = CalcDiscountData.model_validate(
        {
            "membership_id": membership_id,
            "purchase_amount": purchase_amount,
        },
    )
    return jsonify(serializer.dump(interactor.execute(calc_discount_data)))
