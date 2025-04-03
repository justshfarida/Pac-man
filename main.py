from __future__ import annotations
from typing import TYPE_CHECKING, List
import pygame
from game.structs import Position, Direction
from game.maze import Maze
from game.pacman import Pacman
from game.ghosts import TILE_LEN, Ghost
from utils.settings import Color, settings

if TYPE_CHECKING:
    from pygame import Surface
    from pygame.time import Clock
    from pygame.font import Font as PygameFont


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()

        self.screen: Surface        = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.timer: Clock           = pygame.time.Clock()
        self.fps: int               = 60

        pygame.display.set_caption("Pac-Man Pathfinding")

        # Game Objects
        self.maze: Maze             = Maze()
        self.pacman: Pacman         = Pacman(starting_position=Position(16, 24), maze=self.maze)

        # (self, name, start_pos, color, speed, behavior, maze)
        self.ghosts: List[Ghost] = [
            Ghost(Position(14, 15), "red", 2, "blinky", self.maze, self),  # Blinky
            Ghost(Position(14, 16), "pink", 2, "pinky", self.maze, self),  # Pinky (BFS)
            Ghost(Position(12, 14), "blue", 2, "inky", self.maze, self),  # Inky (DFS)
            Ghost(Position(16, 14), "orange", 2, "clyde", self.maze, self),  # Clyde
        ]

        # Initialize game state variables
        self.font: PygameFont           = pygame.font.Font("assets/fonts/ARCADE.TTF", 36)
        self.score: int                 = 0
        self.power: bool                = False
        self.power_count: int           = 0
        self.eaten_ghosts: List[bool]   = [False, False, False, False]
        self.moving: bool               = False
        self.startup_counter: int       = 0

        # Game Loop
        self.running: bool  = True
        self.paused: bool   = False

    def display_game_over(self):
        game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))  # Red color
        text_rect = game_over_text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 3))
        self.screen.blit(game_over_text, text_rect)

        restart_text = self.font.render("Play Again? Y/N", True, (255, 255, 255))  # White color
        restart_rect = restart_text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2))
        self.screen.blit(restart_text, restart_rect)

    def reset_ghosts(self):
        # Define the initial positions of each ghost by color
        initial_positions = {
            "red": Position(14, 15),  # Blinky's initial position
            "pink": Position(14, 16),  # Pinky's initial position
            "blue": Position(12, 14),  # Inky's initial position
            "orange": Position(16, 14) # Clyde's initial position
        }

        # Define the leave times for each ghost (in frames or time units)
        ghost_leave_times = {
            "red": 0,      # Blinky leaves immediately
            "pink": 180,   # Pinky leaves after 180 units of time
            "blue": 360,   # Inky leaves after 360 units of time
            "orange": 540  # Clyde leaves after 540 units of time
        }

        for ghost in self.ghosts:
            initial_position = initial_positions.get(ghost.color)

            if initial_position:
                ghost.x = initial_position.x * TILE_LEN + TILE_LEN // 2
                ghost.y = initial_position.y * TILE_LEN + TILE_LEN // 2
                ghost.rect.center = (ghost.x, ghost.y)

            ghost.leave_timer = ghost_leave_times.get(ghost.color, 0)

            ghost.mode = "waiting"

    def check_collision_with_pacman(self, pacman):
        for ghost in self.ghosts:
            ghost.check_collision_with_pacman(pacman)

    def draw_misc(self) -> None:
        score_text = self.font.render(f"Score {self.score}", True, 'white')
        self.screen.blit(score_text, (10, 920))

    def check_collisions(self) -> None:
        """Checks if Pac-Man eats a pellet or power pellet and updates game state."""
        pos = self.pacman.get_position()
        x, y = pos.x, pos.y

        # Check if Pac-Man is within bounds
        if 0 <= x <= 28:
            if self.maze.grid[y][x] == 1:  # Normal Pellet
                self.maze.grid[y][x] = 0
                self.score += 10
            elif self.maze.grid[y][x] == 2:  # Power Pellet
                self.maze.grid[y][x] = 0
                self.score += 50
                self.power = True
                self.power_count = 0
                self.eaten_ghosts = [False, False, False, False]  # Reset eaten ghosts

    def pause_game(self) -> None:
        while self.paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:  # Press 'P' to resume
                        self.paused = False

    def restart_game(self):
    # Reset all game variables and objects
        self.pacman = Pacman(starting_position=Position(16, 24), maze=self.maze)
        self.ghosts = [
            Ghost(Position(14, 15), "red", 2, "blinky", self.maze, self),  # Blinky
            Ghost(Position(14, 16), "pink", 2, "pinky", self.maze, self),  # Pinky
            Ghost(Position(12, 14), "blue", 2, "inky", self.maze, self),  # Inky
            Ghost(Position(16, 14), "orange", 2, "clyde", self.maze, self),  # Clyde
        ]
        self.score = 0
        self.power = False
        self.power_count = 0
        self.eaten_ghosts = [False, False, False, False]

        # Reset maze grid to its initial state
        self.maze = Maze()  # Reinitialize the maze to reset the grid

        # Reset ghosts' positions
        self.reset_ghosts()


    def run(self) -> None:
        while self.running:
            self.timer.tick(self.fps)
            self.screen.fill(Color.BLACK)

            # Draw game
            self.maze.draw(self.screen)
            self.pacman.draw(self.screen)
            for ghost in self.ghosts:
                ghost.draw(self.screen)
            self.draw_misc()

            if self.pacman.check_game_over():
                self.display_game_over()  # Display "GAME OVER"
                pygame.display.flip()  # Update the screen to show the new text

                # Wait for player input to restart or quit
                waiting_for_input = True
                while waiting_for_input:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.running = False
                            waiting_for_input = False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_y:  # If 'Y' is pressed, restart the game
                                self.restart_game()  # Reset game
                                waiting_for_input = False  # Exit the loop and restart the game
                            elif event.key == pygame.K_n:  # If 'N' is pressed, quit
                                self.running = False
                                waiting_for_input = False

            # Check for pellet and power pellet collisions
            self.check_collisions()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.pacman.direction_command = Direction.RIGHT
                    elif event.key == pygame.K_LEFT:
                        self.pacman.direction_command = Direction.LEFT
                    elif event.key == pygame.K_UP:
                        self.pacman.direction_command = Direction.UP
                    elif event.key == pygame.K_DOWN:
                        self.pacman.direction_command = Direction.DOWN
                    elif event.key == pygame.K_p:
                        self.paused = True
                        self.pause_game()

            # Move Pac-Man
            self.pacman.move()

            blinky_pos = self.ghosts[0].get_position()

            for ghost in self.ghosts:  # Only move the first three ghosts
                ghost.move(self.pacman.get_position(), blinky_pos)  # Pass Pac-Man's position to ghosts
                ghost.check_collision_with_pacman(self.pacman)

            pygame.display.update()

        pygame.quit()


def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
