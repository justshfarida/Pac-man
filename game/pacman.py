import pygame
from utils.settings import YELLOW

class Pacman:
    def __init__(self, x, y, maze):
        self.x = x
        self.y = y
        self.maze = maze
        self.speed = 2  
        self.direction = 0  # 0: RIGHT, 1: LEFT, 2: UP, 3: DOWN
        self.direction_command = 0  
        self.counter = 0  
        self.centerx = x + 23
        self.centery = y + 24
        self.turns = [False, False, False, False]  # Ensure it's always initialized

        # Load Pac-Man images (animation frames)
        self.player_images = []
        for i in range(1, 5):  
            image = pygame.image.load(f'./assets/player_images/{i}.png')
            self.player_images.append(pygame.transform.scale(image, (45, 45)))

    def move(self):
        """Moves Pac-Man in the allowed direction."""
        self.centerx = self.x + 23
        self.centery = self.y + 24

        # Check allowed movements
        self.turns = self.maze.check_position(self.centerx, self.centery, self.direction_command)

        # ✅ Update direction if movement is allowed
        if self.turns[self.direction_command]:  
            self.direction = self.direction_command

        # ✅ Move Pac-Man
        if self.direction == 0 and self.turns[0]:  # RIGHT
            self.x += self.speed
        elif self.direction == 1 and self.turns[1]:  # LEFT
            self.x -= self.speed
        elif self.direction == 2 and self.turns[2]:  # UP
            self.y -= self.speed
        elif self.direction == 3 and self.turns[3]:  # DOWN
            self.y += self.speed

        # ✅ Handle teleporting at edges
        if self.x > 900:
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
