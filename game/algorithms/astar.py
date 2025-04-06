from __future__ import annotations

from typing import TYPE_CHECKING
import heapq

from game.abstract import PathFinderInt

if TYPE_CHECKING:
    from game.maze import Maze
    from game.structs import Position


class AStar(PathFinderInt):
    @classmethod
    def _algorithm(
            cls,
            start: Position,
            goal: Position,
            maze: Maze,
    ):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: cls.__heuristic(start, goal)}

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == goal:
                return cls.__reconstruct_path(came_from, current)

            for neighbor in maze.get_neighbors_for_ghost(current):
                # print(f"[A*] {self.color} ghost neighbors at {current}: {self.maze.get_neighbors_for_ghost(current)}")
                temp_g_score = g_score[current] + 1
                if neighbor not in g_score or temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + cls.__heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []

    @staticmethod
    def __reconstruct_path(came_from, current):
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    @staticmethod
    def __heuristic(
            pos: Position,
            goal: Position
    ):
        return abs(pos[0] - goal[0]) + abs(pos[0] - goal[1])
