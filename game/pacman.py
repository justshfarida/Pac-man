from __future__ import annotations

from typing import List, TYPE_CHECKING, Dict

import pygame

from game.abstract import EntityInt, EntityMethods
from game.structs import Direction
from utils.settings import settings
from game.structs import Position

if TYPE_CHECKING:
    from game.maze import Maze

TILE_LEN = settings.TILE_LEN


class Pacman(EntityInt, EntityMethods):
    def __init__(
            self,
            starting_position: Position,
            maze: Maze
    ) -> None:
        self.set_position(starting_position)

        self.maze: Maze                     = maze
        self.speed: int                     = settings.PACMAN_SPEED # TODO: There is a bug when odd number used as speed
        self.direction: Direction           = Direction.RIGHT
        self.direction_command: Direction   = self.direction
        self.counter: int                   = 0
        self.turns: List[bool]              = [False, False, False, False]  # Ensure it's always initialized
        self.lives: int = 3  # Pac-Man starts with 3 lives

        # Load Pac-Man images (animation frames)
        self.player_images: Dict[Direction, List[pygame.Surface]] = {
            Direction.RIGHT: [],
            Direction.LEFT: [],
            Direction.UP: [],
            Direction.DOWN: [],
        }
        for i in range(1, 5):
            image = pygame.image.load(f'./assets/player_images/{i}.png')
            scaled = pygame.transform.scale(image, (36, 36))

            self.player_images[Direction.RIGHT].append(scaled)
            self.player_images[Direction.LEFT].append(pygame.transform.flip(scaled, True, False))
            self.player_images[Direction.DOWN].append(pygame.transform.rotate(scaled, 270))
            self.player_images[Direction.UP].append(pygame.transform.rotate(scaled, 90))

    def move(self, *args, **kwargs) -> None:
        """Moves Pac-Man in the allowed direction, unless not alive (e.g., after being caught)."""

        if not hasattr(self, "alive"):
            self.alive = True  # Default to alive if not set

        if not self.alive:
            return  # Pac-Man was caught; don't move

        # Check allowed movements at center of tile
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


        # Handle wrap-around logic
        x_pos = self.x // TILE_LEN
        if x_pos >= 30:
            self.x = 0 - TILE_LEN
        elif x_pos <= -2:
            self.x = settings.SCREEN_WIDTH


    def draw(
            self,
            screen: pygame.Surface
    ) -> None:
        """Draws the animated Pac-Man sprite with direction adjustments."""

        # Update animation frame
        self.counter = (self.counter + 1) % 20  
        frame_index = (self.counter // 5) % 4

        dest = (self.x - TILE_LEN//2, self.y - TILE_LEN//2)
        image = self.player_images[self.direction][frame_index]
        screen.blit(source=image, dest=dest)

    def lose_life(self):
        """Handle the logic when Pac-Man loses a life."""
        self.lives -= 1
        print(f"💀 Pac-Man lost a life! Lives remaining: {self.lives}")
        if self.lives > 0:
            self.reset_position()  # Reset Pac-Man's position after losing a life

    def check_game_over(self) -> bool:
        """Checks if the game is over."""
        return self.lives <= 0

    def reset_position(self):
        """Resets Pac-Man's position to the starting point."""
        self.set_position(Position(16, 24))
