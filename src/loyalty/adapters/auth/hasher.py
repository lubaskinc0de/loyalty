from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


class Hasher(Protocol):
    @abstractmethod
    def hash(self, raw: str) -> str: ...

    @abstractmethod
    def compare(self, raw: str, hashed: str) -> bool: ...


@dataclass(slots=True, frozen=True)
class ArgonHasher(Hasher):
    argon: PasswordHasher

    def hash(self, raw: str) -> str:
        return self.argon.hash(raw)

    def compare(self, raw: str, hashed: str) -> bool:
        try:
            self.argon.verify(hashed, raw)
        except VerifyMismatchError:
            return False
        else:
            return True
