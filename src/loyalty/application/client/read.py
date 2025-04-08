from dataclasses import dataclass

from loyalty.application.common.idp import ClientIdProvider
from loyalty.domain.entity.client import Client


@dataclass(slots=True, frozen=True)
class ReadClient:
    idp: ClientIdProvider

    def execute(self) -> Client:
        return self.idp.get_client()
