import pygame
from game.maze import Maze  # ✅ Import Maze first
from game.pacman import Pacman  # ✅ Now it works
from game.ghosts import Ghost
from utils.settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
timer = pygame.time.Clock()
fps = 60
pygame.display.set_caption("Pac-Man Pathfinding")

# Game Objects
maze = Maze()
pacman = Pacman(450, 663, maze)  # ✅ No more import loop
ghosts = [Ghost(200, 200, "BFS"), Ghost(300, 300, "DFS"), Ghost(400, 400, "A*")]

# Game Loop
run = True
while run:
    timer.tick(fps)
    screen.fill(BLACK)

    # Draw maze
    maze.draw(screen)
    pacman.draw(screen)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                pacman.direction_command = 0
            elif event.key == pygame.K_LEFT:
                pacman.direction_command = 1
            elif event.key == pygame.K_UP:
                pacman.direction_command = 2
            elif event.key == pygame.K_DOWN:
                pacman.direction_command = 3

    pacman.move()
    pygame.display.update()

pygame.quit()
