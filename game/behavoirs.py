from __future__ import annotations

from typing import Optional, overload, TYPE_CHECKING

from game.abstract import BehaviourInt
from game.structs import Position, Direction

if TYPE_CHECKING:
    from game.maze import Maze
    from game.ghosts import Ghost


direction_vectors = {
            Direction.RIGHT: (1, 0),
            Direction.LEFT:  (-1, 0),
            Direction.UP:    (0, -1),
            Direction.DOWN:  (0, 1),
        }


class Blinky(BehaviourInt):
    def get_target_position(
            self,
            pacman_pos: Position,
            *args, **kwargs,
    ) -> Position:
        return pacman_pos


class Pinky(BehaviourInt):
    last_pacman_dir = None
    target_pos = None

    def __init__(self, maze: Maze):
        self._maze = maze

    def get_target_position(
            self,
            pacman_pos: Position,
            pacman_dir: Optional[Direction] = None,
            *args, **kwargs
    ) -> Position:
        if self.last_pacman_dir != pacman_dir or self.target_pos is None or 1:
            self.last_pacman_dir = pacman_dir
            self.target_pos = self._predict_pacman_position(
                pacman_pos,
                pacman_dir,
            )

        return self.target_pos

    def _predict_pacman_position(
            self,
            pacman_pos,
            pacman_dir,
            max_steps=4,
    ):
        dx, dy = direction_vectors.get(pacman_dir, (0, 0))
        grid_x, grid_y = pacman_pos

        for steps in range(max_steps, 0, -1):
            tx = grid_x + dx * steps
            ty = grid_y + dy * steps

            # Bounds check
            if (
                    0 <= ty < len(self._maze.grid) and
                    0 <= tx < len(self._maze.grid[0]) and
                    (
                            (cell := self._maze.grid[ty][tx] < 3) or
                            cell == 9
                    )
            ):
                return Position(tx, ty)

        # If all ahead tiles are walls or out-of-bounds, fallback to Pac-Man’s current tile
        return pacman_pos


class Inky(BehaviourInt):
    last_pacman_dir = None
    target_pos = None

    def __init__(
            self,
            maze: Maze,
            blinky: Ghost,
    ):
        self._maze = maze
        self.__blinky = blinky

    def get_target_position(
            self,
            pacman_pos: Position,
            pacman_dir: Optional[Direction] = None,
            *args, **kwargs
    ):
        blinky_pos = self.__blinky.get_position()
        max_map_size = (30, 31)

        dx, dy = direction_vectors.get(pacman_dir, (0, 0))
        ahead_x = pacman_pos.x + dx * 2
        ahead_y = pacman_pos.y + dy * 2

        # Vector from Blinky to 2-ahead position
        vx = ahead_x - blinky_pos[0]
        vy = ahead_y - blinky_pos[1]

        # Double the vector and get final target
        target_x = blinky_pos[0] + 2 * vx
        target_y = blinky_pos[1] + 2 * vy

        #Keep target within map bounds
        max_x, max_y = max_map_size
        target_x = max(0, min(target_x, max_x - 1))
        target_y = max(0, min(target_y, max_y - 1))

        #Make sure target is not a wall
        if (cell:=self._maze.grid[target_y][target_x] >= 3 )and cell!=9:
            # fallback to a nearby walkable tile or Pac-Man
            self.target_pos = pacman_pos
            return self.target_pos

        self.target_pos = Position(target_x, target_y)

        return self.target_pos


class Clyde(BehaviourInt):
    def get_target_position(
            self,
            pacman_pos: Position,
            pacman_dir: Optional[Direction] = None,
            self_pos: Optional[Position] = None,
    ):
        px, py = pacman_pos
        cx, cy = self_pos
        distance = abs(px - cx) + abs(py - cy)

        if distance < 8:
            return Position(2,30)

        return pacman_pos
