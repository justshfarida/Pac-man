from __future__ import annotations

from typing import TYPE_CHECKING
from collections import deque

from game.abstract import PathFinderInt

if TYPE_CHECKING:
    from game.maze import Maze
    from game.structs import Position


class BFS(PathFinderInt):
    @classmethod
    def _algorithm(
            cls,
            start: Position,
            goal: Position,
            maze: Maze,
    ):
        visited = set()
        queue = deque([(start, [])])

        while queue:
            current, path = queue.popleft()
            if current == goal:
                return path

            for neighbor in maze.get_neighbors_for_ghost(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return []
