from abc import abstractmethod
from typing import Protocol


class GeoFinder(Protocol):
    @abstractmethod
    def find_city(self, city: str) -> str | None: ...
