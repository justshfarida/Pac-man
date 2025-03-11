from typing import List, Tuple

import pygame

from game.abstract import Entity
from utils.settings import settings

TILE_LEN = settings.TILE_LEN

class Pacman(Entity):
    def __init__(self, starting_position: Tuple[int, int], maze):
        self.x: int = starting_position[0]*TILE_LEN
        self.y: int = starting_position[1]*TILE_LEN
        self.maze = maze
        self.speed: int = 2 # TODO: There is a bug when odd number used as speed
        self.direction = 0  # 0: RIGHT, 1: LEFT, 2: UP, 3: DOWN
        self.direction_command = 0  
        self.counter: int = 0
        self.centerx: int = self.x + TILE_LEN//2
        self.centery: int = self.y + TILE_LEN//2
        self.turns: List[bool] = [False, False, False, False]  # Ensure it's always initialized

        # Load Pac-Man images (animation frames)
        self.player_images = []
        for i in range(1, 5):  
            image = pygame.image.load(f'./assets/player_images/{i}.png')
            self.player_images.append(pygame.transform.scale(image, (36, 36)))

    def _is_centered(self) -> bool:
        return self.centerx % TILE_LEN == self.centery % TILE_LEN == TILE_LEN//2

    def move(self):
        """Moves Pac-Man in the allowed direction."""
        self.centerx = self.x + TILE_LEN//2
        self.centery = self.y + TILE_LEN//2

        # Check allowed movements
        if self._is_centered():
            self.turns = self.maze.check_position(self.centerx, self.centery, self.direction_command)

            if self.turns[self.direction_command]:
                self.direction = self.direction_command

        if self.direction == 0 and self.turns[0]:  # RIGHT
            self.x += self.speed
        elif self.direction == 1 and self.turns[1]:  # LEFT
            self.x -= self.speed
        elif self.direction == 2 and self.turns[2]:  # UP
            self.y -= self.speed
        elif self.direction == 3 and self.turns[3]:  # DOWN
            self.y += self.speed

        if self.x > 900: # TODO: Fix values
            self.x = -47
        if self.x < -50:
            self.x = 897

    def draw(self, screen):
        """Draws the animated Pac-Man sprite with direction adjustments."""

        # Update animation frame
        self.counter = (self.counter + 1) % 20  
        frame_index = (self.counter // 5) % 4  

        if self.direction == 0:  
            screen.blit(self.player_images[frame_index], (self.x, self.y))
        elif self.direction == 1:  
            screen.blit(pygame.transform.flip(self.player_images[frame_index], True, False), (self.x, self.y))
        elif self.direction == 2:  
            screen.blit(pygame.transform.rotate(self.player_images[frame_index], 90), (self.x, self.y))
        elif self.direction == 3: 
            screen.blit(pygame.transform.rotate(self.player_images[frame_index], 270), (self.x, self.y))
