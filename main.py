from __future__ import annotations

from typing import TYPE_CHECKING, List

import pygame

from game.structs import Position, Direction
from game.maze import Maze
from game.pacman import Pacman
from game.ghosts import Ghost
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
        self.ghosts: List[Ghost]    = [
            Ghost(200, 200, "BFS"),
            Ghost(300, 300, "DFS"),
            Ghost(400, 400, "A*")
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

    def run(self) -> None:
        while self.running:
            self.timer.tick(self.fps)
            self.screen.fill(Color.BLACK)

            # Draw game
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

            self.pacman.move()
            pygame.display.update()

        pygame.quit()


def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()