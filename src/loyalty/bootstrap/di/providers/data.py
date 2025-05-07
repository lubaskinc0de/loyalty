from dataclasses import dataclass
from typing import Generic, TypeVar

from dishka import FromDishka, Provider, Scope, provide
from flask import Request
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


@dataclass
class Parsed(Generic[T]):
    data: T


Body = FromDishka[Parsed[T]]


class DataProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def parse(self, request: Request, type_: type[T]) -> Parsed[T]:
        return Parsed(type_(**request.get_json()))
