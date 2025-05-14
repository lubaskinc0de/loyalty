from abc import abstractmethod
from typing import BinaryIO, Protocol


class FileManager(Protocol):
    @abstractmethod
    def upload(self, file: BinaryIO, ext: str, size: int) -> str: ...
