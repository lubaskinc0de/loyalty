from abc import abstractmethod
from typing import Protocol
from uuid import UUID


class BranchAffilationGateway(Protocol):
    @abstractmethod
    def is_belong_to_loyalty(self, branch_id: UUID, loyalty_id: UUID) -> bool: ...
