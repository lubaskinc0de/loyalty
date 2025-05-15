from dataclasses import dataclass

from loyalty.application.common.file_manager import FileManager
from loyalty.application.common.idp import BusinessIdProvider
from loyalty.application.common.uow import UoW


@dataclass(slots=True, frozen=True)
class DetachBusinessAvatar:
    uow: UoW
    idp: BusinessIdProvider
    file_manager: FileManager

    def execute(self) -> None:
        business = self.idp.get_business()
        if business.avatar_url is not None:
            self.file_manager.remove(business.avatar_url)
        business.avatar_url = None
        self.uow.commit()
