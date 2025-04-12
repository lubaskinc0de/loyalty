from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from loyalty.application.business_branch.dto import BusinessBranches
from loyalty.domain.entity.business_branch import BusinessBranch


class BusinessBranchGateway(Protocol):
    @abstractmethod
    def get_by_id(self, business_branch_id: UUID) -> BusinessBranch | None: ...

    @abstractmethod
    def get_business_branches(self, limit: int, offset: int, business_id: UUID) -> BusinessBranches: ...
