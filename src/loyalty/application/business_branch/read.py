from dataclasses import dataclass
from uuid import UUID

from loyalty.application.business_branch.dto import BusinessBranches
from loyalty.application.common.gateway.business import BusinessGateway
from loyalty.application.common.gateway.business_branch import BusinessBranchGateway
from loyalty.application.common.idp import UserIdProvider
from loyalty.application.data_model.business_branch import (
    BusinessBranchData,
    convert_branch_to_dto,
)
from loyalty.application.exceptions.base import AccessDeniedError, InvalidPaginationQueryError, LimitIsTooHighError
from loyalty.application.exceptions.business import BusinessDoesNotExistError
from loyalty.application.exceptions.business_branch import BusinessBranchDoesNotExistError
from loyalty.application.shared_types import MAX_LIMIT
from loyalty.domain.entity.business_branch import BusinessBranch

DEFAULT_BRANCHES_PAGE_LIMIT = 10


@dataclass(slots=True, frozen=True)
class ReadBusinessBranch:
    idp: UserIdProvider
    gateway: BusinessBranchGateway

    def execute(self, business_branch_id: UUID) -> BusinessBranchData:
        user = self.idp.get_user()
        if (business_branch := self.gateway.get_by_id(business_branch_id)) is None:
            raise BusinessBranchDoesNotExistError

        if not business_branch.can_read(user):
            raise AccessDeniedError

        return convert_branch_to_dto(business_branch)


@dataclass(slots=True, frozen=True)
class ReadBusinessBranches:
    idp: UserIdProvider
    gateway: BusinessBranchGateway
    business_gateway: BusinessGateway

    def execute(self, business_id: UUID, offset: int, limit: int = DEFAULT_BRANCHES_PAGE_LIMIT) -> BusinessBranches:
        user = self.idp.get_user()
        if not BusinessBranch.can_read_list(user):
            raise AccessDeniedError

        if limit > MAX_LIMIT:
            raise LimitIsTooHighError

        if limit < 0 or offset < 0:
            raise InvalidPaginationQueryError

        if self.business_gateway.get_by_id(business_id) is None:
            raise BusinessDoesNotExistError

        if user.business and user.business.business_id != business_id:
            raise AccessDeniedError

        business_branches = self.gateway.get_business_branches(
            limit=limit,
            offset=offset,
            business_id=business_id,
        )
        return business_branches
