import pygame
from game.maze import Maze
from game.pacman import Pacman
from game.ghosts import Ghost
from utils.settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
timer=pygame.time.Clock() # controls game speed
fps=60 # frames per second
pygame.display.set_caption("Pac-Man Pathfinding")
font=pygame.font.Font("freesansbold.ttf", 20)

# Game Objects
maze = Maze()
pacman = Pacman(450, 663)
ghosts = [Ghost(200, 200, "BFS"), Ghost(300, 300, "DFS"), Ghost(400, 400, "A*")]

# Game Loop
run = True
while run:
    timer.tick(fps)
    screen.fill(BLACK)
    
    # Draw maze
    maze.draw(screen)

    # Move and draw Pac-Man
    pacman.move()
    pacman.draw(screen)

    # Move and draw ghosts
    # for ghost in ghosts:
    #     ghost.move(pacman)  # Pass Pac-Man position for pathfinding
    #     ghost.draw(screen)

    # Handle Quit Event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
