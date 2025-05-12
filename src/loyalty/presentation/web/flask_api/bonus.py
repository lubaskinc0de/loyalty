from uuid import UUID

from dishka import FromDishka
from flask import Blueprint, Response, jsonify

from loyalty.application.bonus.read import ReadBonuses
from loyalty.presentation.web.serializer import serializer

bonus = Blueprint("bonus", __name__)


@bonus.route("/<uuid:membership_id>", methods=["GET"], strict_slashes=False)
def read_bonuses(membership_id: UUID, interactor: FromDishka[ReadBonuses]) -> Response:
    result = interactor.execute(membership_id)
    return jsonify(serializer.dump(result))
