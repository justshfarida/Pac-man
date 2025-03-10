import pygame
from game.maze import Maze  
from game.pacman import Pacman
from game.ghosts import Ghost
from utils.settings import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, TILE_LEN

# Initialize Pygame
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
timer = pygame.time.Clock()
fps = 60
pygame.display.set_caption("Pac-Man Pathfinding")

# Game Objects
maze = Maze()
pacman = Pacman(TILE_LEN*16, TILE_LEN*24, maze)
ghosts = [Ghost(200, 200, "BFS"), Ghost(300, 300, "DFS"), Ghost(400, 400, "A*")]

# Initialize game state variables
font = pygame.font.Font("assets/fonts/ARCADE.TTF", 36)
score = 0
power = False
power_count = 0
eaten_ghosts = [False, False, False, False]
moving=False
startup_counter=0
def draw_misc():
    score_text=font.render(f"Score {score}", True, 'white')
    screen.blit(score_text, (10,920))

def check_collisions(pacman, maze, score, power, power_count, eaten_ghosts):
    """Checks if Pac-Man eats a pellet or power pellet and updates game state."""
    tile_height = (SCREEN_HEIGHT - 50) // 32
    tile_width = SCREEN_WIDTH // 30

    center_x = pacman.centerx // tile_width
    center_y = pacman.centery // tile_height

    # Check if Pac-Man is within bounds
    if 0 < pacman.x < 870:
        if maze.grid[center_y][center_x] == 1:  # Normal Pellet
            maze.grid[center_y][center_x] = 0  
            score += 10
        elif maze.grid[center_y][center_x] == 2:  # Power Pellet
            maze.grid[center_y][center_x] = 0  
            score += 50
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]  # Reset eaten ghosts

    return score, power, power_count, eaten_ghosts
# Game Loop
run = True
paused = False

def pause_game():
    global paused

    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Press 'P' to resume
                    paused = False

while run:
    timer.tick(fps)
    screen.fill(BLACK)

    # Draw maze
    maze.draw(screen)
    pacman.draw(screen)
    draw_misc()
    # Check for pellet and power pellet collisions
    score, power, power_count, eaten_ghosts = check_collisions(pacman, maze, score, power, power_count, eaten_ghosts)
    
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
            elif event.key == pygame.K_p:
                paused = True
                pause_game()

        # if event.type == pygame.KEYUP:
        #     if event.key == pygame.K_RIGHT and pacman.direction_command == 0:
        #         pacman.direction_command = pacman.direction
        #     if event.key == pygame.K_LEFT and pacman.direction_command == 1:
        #         pacman.direction_command = pacman.direction
        #     if event.key == pygame.K_UP and pacman.direction_command == 2:
        #         pacman.direction_command = pacman.direction
        #     if event.key == pygame.K_DOWN and pacman.direction_command == 3:
        #         pacman.direction_command = pacman.direction
    pacman.move()
    pygame.display.update()

pygame.quit()
