from __future__ import annotations

from abc import abstractmethod
from typing import Protocol, runtime_checkable

from game.structs import Position
from utils.settings import settings


@runtime_checkable
class EntityInt(Protocol):
    x: int
    y: int

    @abstractmethod
    def move(self) -> None:
        ...

    @abstractmethod
    def draw(self, screen) -> None:
        ...

    def get_position(self) -> Position:
        return Position(
            self.x // settings.TILE_LEN,
            self.y // settings.TILE_LEN,
        )