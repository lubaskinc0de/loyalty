from abc import abstractmethod
from typing import Protocol
from uuid import UUID

from loyalty.domain.entity.business_branch import BusinessBranch


class BusinessBranchGateway(Protocol):
    @abstractmethod
    def get_by_id(self, business_branch_id: UUID) -> BusinessBranch | None: ...
