from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class Ping:
    async def execute(self) -> str:
        return "pong"
