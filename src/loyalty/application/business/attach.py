from dataclasses import dataclass
from typing import BinaryIO

from loyalty.application.common.file_manager import FileManager
from loyalty.application.common.idp import BusinessIdProvider
from loyalty.application.common.uow import UoW


@dataclass(slots=True, frozen=True)
class BusinessImageData:
    avatar_url: str


@dataclass(slots=True, frozen=True)
class AttachBusinessAvatar:
    file_manager: FileManager
    uow: UoW
    idp: BusinessIdProvider

    def execute(
        self,
        file: BinaryIO,
        ext: str,
        size: int,
    ) -> BusinessImageData:
        business = self.idp.get_business()
        avatar_url = self.file_manager.upload(file, ext, size)
        business.avatar_url = avatar_url
        self.uow.commit()

        return BusinessImageData(avatar_url)
