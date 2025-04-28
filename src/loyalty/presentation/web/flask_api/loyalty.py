from uuid import UUID

from dishka import FromDishka
from flask import Blueprint, Response, jsonify, request

from loyalty.application.business_branch.create import (
    BusinessBranchForm,
    CreateBusinessBranch,
)
from loyalty.application.business_branch.delete import DeleteBusinessBranch
from loyalty.application.business_branch.read import ReadBusinessBranch, ReadBusinessBranches
from loyalty.application.business_branch.update import UpdateBusinessBranch
from loyalty.application.data_model.loyalty import LoyaltyForm
from loyalty.application.loyalty.create import CreateLoyalty
from loyalty.application.loyalty.update import UpdateLoyalty
from loyalty.domain.entity.business_branch import BusinessBranch
from loyalty.presentation.web.serializer import serializer

loyalty = Blueprint("loyalty", __name__)


@loyalty.route("/", methods=["POST"], strict_slashes=False)
def create_loyalty(*, interactor: FromDishka[CreateLoyalty]) -> Response:
    loyalty_id = interactor.execute(LoyaltyForm(**request.get_json()))
    return jsonify({"loyalty_id": loyalty_id})


@loyalty.route("/<uuid:loyalty_id>", methods=["PUT"], strict_slashes=False)
def update_loyalty(*, loyalty_id: UUID, interactor: FromDishka[UpdateLoyalty]) -> Response:
    interactor.execute(loyalty_id, LoyaltyForm(**request.get_json()))
    return Response(status=204)

