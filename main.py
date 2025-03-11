import pygame
from game.maze import Maze
from game.pacman import Pacman
from game.ghosts import Ghost
from utils.settings import Color, settings


class Game:
    def __init__(
            self,
    ) -> None:
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.timer = pygame.time.Clock()
        self.fps = 60

        pygame.display.set_caption("Pac-Man Pathfinding")

        # Game Objects
        self.maze = Maze()
        self.pacman = Pacman(starting_position=(16, 24), maze=self.maze)
        self.ghosts = [
            Ghost(200, 200, "BFS"),
            Ghost(300, 300, "DFS"),
            Ghost(400, 400, "A*")
        ]

        # Initialize game state variables
        self.font = pygame.font.Font("assets/fonts/ARCADE.TTF", 36)
        self.score = 0
        self.power = False
        self.power_count = 0
        self.eaten_ghosts = [False, False, False, False]
        self.moving = False
        self.startup_counter = 0

        # Game Loop
        self.running = True
        self.paused = False

    def draw_misc(self):
        score_text = self.font.render(f"Score {self.score}", True, 'white')
        self.screen.blit(score_text, (10, 920))

    def check_collisions(self):
        """Checks if Pac-Man eats a pellet or power pellet and updates game state."""
        tile_height = (settings.SCREEN_HEIGHT - 50) // 32
        tile_width = settings.SCREEN_WIDTH // 30

        center_x = self.pacman.centerx // tile_width
        center_y = self.pacman.centery // tile_height

        # Check if Pac-Man is within bounds
        if 0 < self.pacman.x < 870:
            if self.maze.grid[center_y][center_x] == 1:  # Normal Pellet
                self.maze.grid[center_y][center_x] = 0
                self.score += 10
            elif self.maze.grid[center_y][center_x] == 2:  # Power Pellet
                self.maze.grid[center_y][center_x] = 0
                self.score += 50
                self.power = True
                self.power_count = 0
                self.eaten_ghosts = [False, False, False, False]  # Reset eaten ghosts

    def pause_game(self):
        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # Press 'P' to resume
                        self.paused = False

    def run(self) -> None:
        while self.running:
            self.timer.tick(self.fps)
            self.screen.fill(Color.BLACK)

            # Draw maze
            self.maze.draw(self.screen)
            self.pacman.draw(self.screen)
            self.draw_misc()

            # Check for pellet and power pellet collisions
            self.check_collisions()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.pacman.direction_command = 0
                    elif event.key == pygame.K_LEFT:
                        self.pacman.direction_command = 1
                    elif event.key == pygame.K_UP:
                        self.pacman.direction_command = 2
                    elif event.key == pygame.K_DOWN:
                        self.pacman.direction_command = 3
                    elif event.key == pygame.K_p:
                        self.paused = True
                        self.pause_game()

            self.pacman.move()
            pygame.display.update()

        pygame.quit()


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()