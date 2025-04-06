from __future__ import annotations

from abc import abstractmethod
from typing import Protocol, runtime_checkable, overload, Optional, Any, TYPE_CHECKING

from game.structs import Position
from utils.settings import get_settings

if TYPE_CHECKING:
    from pygame import Surface
    from utils.settings import Settings
    from game.structs import Direction


@runtime_checkable
class EntityInt(Protocol):
    @overload
    @abstractmethod
    def move(self) -> None:
        ...

    @overload
    @abstractmethod
    def move(
            self,
            enemy_pos: Position,
    ) -> None:
        ...

    @abstractmethod
    def move(
            self,
            enemy_pos: Optional[Position] = None,
    ) -> None:
        ...

    @abstractmethod
    def draw(
            self,
            screen: Surface
    ) -> None:
        ...


class EntityMethods:
    x: int
    y: int

    def _is_centered(
            self,
            settings: Settings = get_settings(),
    ) -> bool:
        return self.x % settings.TILE_LEN == self.y % settings.TILE_LEN == settings.TILE_LEN//2

    def get_position(
            self,
            settings: Settings = get_settings(),
    ) -> Position:
        return Position(
            self.x // settings.TILE_LEN,
            self.y // settings.TILE_LEN,
        )

    def set_position(
            self,
            position: Position,
            settings: Settings = get_settings(),
    ) -> None:
        self.x = position.x * settings.TILE_LEN + settings.TILE_LEN // 2
        self.y = position.y * settings.TILE_LEN + settings.TILE_LEN // 2


@runtime_checkable
class BehaviourInt(Protocol):
    @abstractmethod
    def get_target_position(
            self,
            pacman_pos: Position,
            pacman_dir: Optional[Direction] = None,
            self_pos: Optional[Position] = None,
    ) -> Position:
        ...