from abc import abstractmethod
from typing import Protocol


class Hasher(Protocol):
    @abstractmethod
    def hash(self, raw: str) -> str: ...

    @abstractmethod
    def compare(self, raw: str, hashed: str) -> bool: ...
