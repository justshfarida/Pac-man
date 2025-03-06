import pygame
from utils.settings import YELLOW

class Pacman:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)  # Pac-Man's size & position
        self.speed = 1

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:  # Move left
            self.rect.x -= self.speed
        if keys[pygame.K_d]:  # Move right
            self.rect.x += self.speed
        if keys[pygame.K_w]:  # Move up
            self.rect.y -= self.speed
        if keys[pygame.K_s]:  # Move down
            self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, self.rect.center, 15)
