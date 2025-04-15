from __future__ import annotations

from typing import TYPE_CHECKING

from game.abstract import PathFinderInt

if TYPE_CHECKING:
    from game.maze import Maze
    from game.structs import Position


class DFS(PathFinderInt):
    @classmethod
    def __algorithm(
            cls,
            start: Position,
            goal: Position,
            maze: Maze,
    ):
        visited = set()
        stack = [(start, [])]

        while stack:
            current, path = stack.pop()

            if current == goal:
                return path

            for neighbor in maze.get_neighbors_for_ghost(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor]))

        return []
