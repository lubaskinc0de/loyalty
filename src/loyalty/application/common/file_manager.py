from abc import abstractmethod
from typing import BinaryIO, Protocol


class FileManager(Protocol):
    @abstractmethod
    def upload(self, file: BinaryIO, ext: str, size: int) -> str: ...

    @abstractmethod
    def remove(self, file_url: str) -> None: ...
