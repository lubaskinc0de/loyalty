from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Ping:
    def execute(self) -> str:
        return "pong"
