from __future__ import annotations

from typing import List, TYPE_CHECKING

import pygame

from game.abstract import EntityInt
from game.structs import Direction
from utils.settings import settings

if TYPE_CHECKING:
    from game.maze import Maze
    from game.structs import Position

TILE_LEN = settings.TILE_LEN


class Pacman(EntityInt):
    def __init__(
            self,
            starting_position: Position,
            maze: Maze
    ) -> None:
        self.x: int                         = starting_position.x * TILE_LEN + TILE_LEN//2
        self.y: int                         = starting_position.y * TILE_LEN + TILE_LEN//2
        self.maze: Maze                     = maze
        self.speed: int                     = 2 # TODO: There is a bug when odd number used as speed
        self.direction: Direction           = Direction.RIGHT
        self.direction_command: Direction   = self.direction
        self.counter: int                   = 0
        self.turns: List[bool]              = [False, False, False, False]  # Ensure it's always initialized

        # Load Pac-Man images (animation frames)
        self.player_images = []
        for i in range(1, 5):  
            image = pygame.image.load(f'./assets/player_images/{i}.png')
            self.player_images.append(pygame.transform.scale(image, (36, 36)))

    def _is_centered(self) -> bool:
        return self.x % TILE_LEN == self.y % TILE_LEN == TILE_LEN//2

    def move(self) -> None:
        """Moves Pac-Man in the allowed direction."""
        # Check allowed movements
        if self._is_centered():
            self.turns = self.maze.check_position(self.get_position())

            if self.turns[self.direction_command.value]:
                self.direction = self.direction_command

        if self.direction == Direction.RIGHT and self.turns[0]:
            self.x += self.speed
        elif self.direction == Direction.LEFT and self.turns[1]:
            self.x -= self.speed
        elif self.direction == Direction.UP and self.turns[2]:
            self.y -= self.speed
        elif self.direction == Direction.DOWN and self.turns[3]:
            self.y += self.speed

        x_pos = self.x // TILE_LEN
        if x_pos >= 30:
            self.x = 0 - TILE_LEN
        elif x_pos <= -2:
            self.x = settings.SCREEN_WIDTH

    def draw(self, screen) -> None:
        """Draws the animated Pac-Man sprite with direction adjustments."""

        # Update animation frame
        self.counter = (self.counter + 1) % 20  
        frame_index = (self.counter // 5) % 4

        x = self.x - TILE_LEN//2
        y = self.y - TILE_LEN//2

        match self.direction:
            case Direction.RIGHT:
                screen.blit(self.player_images[frame_index], (x, y))
            case Direction.LEFT:
                screen.blit(pygame.transform.flip(self.player_images[frame_index], True, False), (x, y))
            case Direction.UP:
                screen.blit(pygame.transform.rotate(self.player_images[frame_index], 90), (x, y))
            case Direction.DOWN:
                screen.blit(pygame.transform.rotate(self.player_images[frame_index], 270), (x, y))
