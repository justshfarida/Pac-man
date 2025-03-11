import pygame
import random

from game.abstract import EntityInt


class Ghost(EntityInt):
    def __init__(self, x, y, algorithm="BFS"):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.color = (255, 0, 0)  # Red ghost
        self.algorithm = algorithm  # Choose BFS, DFS, or A*
        self.speed = 2


    def move(self):
        # Placeholder movement: random choice until pathfinding is added
        direction = random.choice(["left", "right", "up", "down"])
        if direction == "left":
            self.rect.x -= self.speed
        elif direction == "right":
            self.rect.x += self.speed
        elif direction == "up":
            self.rect.y -= self.speed
        elif direction == "down":
            self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.rect.center, 15)
