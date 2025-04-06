from abc import abstractmethod
from collections.abc import Sequence
from typing import Any, Protocol


class UoW(Protocol):
    @abstractmethod
    def commit(self) -> None: ...

    @abstractmethod
    def add(self, instance: object) -> None: ...

    @abstractmethod
    def delete(self, instance: object) -> None: ...

    @abstractmethod
    def flush(self, objects: Sequence[Any] | None = None) -> None: ...
