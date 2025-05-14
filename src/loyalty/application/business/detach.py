from dataclasses import dataclass

from loyalty.application.common.idp import BusinessIdProvider
from loyalty.application.common.uow import UoW


@dataclass(slots=True, frozen=True)
class DetachBusinessAvatar:
    uow: UoW
    idp: BusinessIdProvider

    def execute(self) -> None:
        business = self.idp.get_business()
        business.avatar_url = None
        self.uow.commit()
