from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from game.ghosts import Ghost
    from game.maze import Maze
    from game.structs import Position


@runtime_checkable
class PathFinderInt(Protocol):
    @classmethod
    def find_path(
            cls,
            start: Position,
            goal: Position,
            maze: Maze,
    ):
        return cls._algorithm(start, goal, maze)

    @classmethod
    @abstractmethod
    def _algorithm(
            cls,
            start: Position,
            goal: Position,
            maze: Maze,
    ):
        ...
