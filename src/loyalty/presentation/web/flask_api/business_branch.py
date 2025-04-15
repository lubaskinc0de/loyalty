from typing import Any
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
from loyalty.domain.entity.business_branch import BusinessBranch
from loyalty.presentation.web.serializer import serializer

business_branch = Blueprint("business_branch", __name__)

DEFAULT_BRANCHES_PAGE_LIMIT = 10


@business_branch.route("/", methods=["POST"], strict_slashes=False)
def create_business_branch(*, interactor: FromDishka[CreateBusinessBranch], **_: dict[Any, Any]) -> Response:
    interactor.execute(BusinessBranchForm(**request.get_json()))
    return Response(status=204)


@business_branch.route("/<uuid:business_branch_id>", methods=["GET"], strict_slashes=False)
def read_business_branch(
    business_branch_id: UUID,
    interactor: FromDishka[ReadBusinessBranch],
    **_: dict[Any, Any],
) -> Response:
    result = interactor.execute(business_branch_id)

    return jsonify(serializer.dump(result))


@business_branch.route("/", methods=["GET"], strict_slashes=False)
def read_business_branches(*, business_id: UUID, interactor: FromDishka[ReadBusinessBranches]) -> Response:
    offset = request.args.get("offset", default=0, type=int)
    limit = request.args.get("limit", default=DEFAULT_BRANCHES_PAGE_LIMIT, type=int)

    result = interactor.execute(
        business_id=business_id,
        limit=limit,
        offset=offset,
    )

    business_branches: list[BusinessBranch] = [serializer.dump(branch) for branch in result.business_branches]

    return jsonify({"branches": business_branches})


@business_branch.route("/<uuid:business_branch_id>", methods=["PUT"], strict_slashes=False)
def update_business_branch(
    *,
    business_branch_id: UUID,
    interactor: FromDishka[UpdateBusinessBranch],
    **_: dict[Any, Any],
) -> Response:
    interactor.execute(business_branch_id, BusinessBranchForm(**request.get_json()))
    return Response(status=204)


@business_branch.route("/<uuid:business_branch_id>", methods=["DELETE"], strict_slashes=False)
def delete_business_branch(
    *,
    business_branch_id: UUID,
    interactor: FromDishka[DeleteBusinessBranch],
    **_: dict[Any, Any],
) -> Response:
    interactor.execute(business_branch_id)
    return Response(status=204)
