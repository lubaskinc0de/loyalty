from uuid import UUID

from dishka import FromDishka
from flask import Blueprint, Response, jsonify, request

from loyalty.application.business_branch.create import BusinessBranchForm, CreateBusinessBranch
from loyalty.application.business_branch.delete import DeleteBusinessBranch
from loyalty.application.business_branch.read import ReadBusinessBranch
from loyalty.application.business_branch.update import UpdateBusinessBranch
from loyalty.presentation.web.serializer import serializer

business_branch = Blueprint("business_branch", __name__)


@business_branch.route("/", methods=["POST"], strict_slashes=False)
def create_business_branch(*, interactor: FromDishka[CreateBusinessBranch]) -> Response:
    interactor.execute(BusinessBranchForm(**request.get_json()))
    return Response(status=204)


@business_branch.route("/<uuid:business_id>", methods=["GET"], strict_slashes=False)
def read_business(business_id: UUID, interactor: FromDishka[ReadBusinessBranch]) -> Response:
    result = interactor.execute(business_id)
    return jsonify(serializer.dump(result))


@business_branch.route("/<uuid:business_id>", methods=["PUT"], strict_slashes=False)
def update_business_branch(business_branch_id: UUID, interactor: FromDishka[UpdateBusinessBranch]) -> Response:
    interactor.execute(business_branch_id, BusinessBranchForm(**request.get_json()))
    return Response(status=204)


@business_branch.route("/<uuid:business_branch_id>", methods=["DELETE"], strict_slashes=False)
def delete_business_branch(business_branch_id: UUID, interactor: FromDishka[DeleteBusinessBranch]) -> Response:
    interactor.execute(business_branch_id)
    return Response(status=204)
