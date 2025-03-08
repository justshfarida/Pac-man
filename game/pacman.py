import pygame
from utils.settings import YELLOW

class Pacman:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 3  # Adjusted speed for smoother movement
        self.direction = 0  # 0: RIGHT, 1: LEFT, 2: UP, 3: DOWN
        self.counter = 0  # Animation frame counter

        # Load Pac-Man images (animation frames)
        self.player_images = []
        for i in range(1, 5):  # Load frames 1.png to 4.png
            image = pygame.image.load(f'./assets/player_images/{i}.png')
            self.player_images.append(pygame.transform.scale(image, (45, 45)))

        # Create a rect for collision detection
        self.rect = pygame.Rect(self.x, self.y, 45, 45)

    def move(self):
        """Handles player movement & direction tracking."""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  # Move left
            self.rect.x -= self.speed
            self.direction = 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:  # Move right
            self.rect.x += self.speed
            self.direction = 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:  # Move up
            self.rect.y -= self.speed
            self.direction = 2
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  # Move down
            self.rect.y += self.speed
            self.direction = 3

        # Update position
        self.x, self.y = self.rect.x, self.rect.y

        # Cycle through animation frames
        self.counter = (self.counter + 1) % 20  # Loops between 0-19

    def draw(self, screen):
        """Draws the animated Pac-Man sprite with direction adjustments."""
        frame_index = (self.counter // 5) % 4  # Switches between 4 frames

        if self.direction == 0:  # RIGHT
            screen.blit(self.player_images[frame_index], (self.x, self.y))
        elif self.direction == 1:  # LEFT
            screen.blit(pygame.transform.flip(self.player_images[frame_index], True, False), (self.x, self.y))
        elif self.direction == 2:  # UP
            screen.blit(pygame.transform.rotate(self.player_images[frame_index], 90), (self.x, self.y))
        elif self.direction == 3:  # DOWN
            screen.blit(pygame.transform.rotate(self.player_images[frame_index], 270), (self.x, self.y))
