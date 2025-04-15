from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

import pygame

from game.behavoirs import Blinky, Pinky, Inky, Clyde
from game.structs import Position, Direction
from game.maze import Maze
from game.pacman import Pacman
from game.ghosts import TILE_LEN, Ghost, GhostModes
from game.algorithms import AStar
from utils.settings import Color, settings

if TYPE_CHECKING:
    from pygame import Surface
    from pygame.time import Clock
    from pygame.font import Font as PygameFont


class Game:
    maze: Maze
    pacman: Pacman
    ghosts: List[Ghost]
    score: int
    power: float
    power_count: int
    eaten_ghosts: List[bool]

    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()

        self.screen: Surface        = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.timer: Clock           = pygame.time.Clock()
        self.fps: int               = 60

        pygame.display.set_caption("Pac-Man Pathfinding")

        self.__init_game_objects()

        # Initialize game state variables
        self.font: PygameFont                       = pygame.font.Font("assets/fonts/ARCADE.TTF", 36)
        self.moving: bool                           = False
        self.startup_counter: int                   = 0
        self.power_start_time: Optional[int]        = None

        # Game Loop
        self.running: bool  = True
        self.paused: bool   = False

    def __init_game_objects(self) -> None:
        self.maze = Maze()
        self.pacman = Pacman(starting_position=Position(16, 24), maze=self.maze)

        self.ghosts = [
            blinky := Ghost(
                start_pos=Position(14, 15),
                color="red",
                pathfinding_algorithm=AStar,
                behavior=Blinky(),
                maze=self.maze,
                game=self
            ),  # Blinky
            Ghost(
                start_pos=Position(14, 16),
                color="pink",
                pathfinding_algorithm=AStar,
                behavior=Pinky(self.maze),
                maze=self.maze,
                game=self,
            ),  # Pinky (BFS)
            Ghost(
                start_pos=Position(12, 14),
                color="blue",
                pathfinding_algorithm=AStar,
                behavior=Inky(maze=self.maze, blinky=blinky),
                maze=self.maze,
                game=self
            ),  # Inky (DFS)
            Ghost(
                start_pos=Position(16, 14),
                color="orange",
                pathfinding_algorithm=AStar,
                behavior=Clyde(),
                maze=self.maze,
                game=self,
            ),  # Clyde
        ]

        self.score = 0
        self.power = False
        self.power_count = 0
        self.eaten_ghosts = [False, False, False, False]

    def display_game_over(self):
        game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))  # Red color
        text_rect = game_over_text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 3))
        self.screen.blit(game_over_text, text_rect)

        restart_text = self.font.render("Play Again? Y/N", True, (255, 255, 255))  # White color
        restart_rect = restart_text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2))
        self.screen.blit(restart_text, restart_rect)
    def restart_game(self):
    # Reset all game variables and objects
        self.pacman = Pacman(starting_position=Position(16, 24), maze=self.maze)
        self.ghosts = [
            blinky := Ghost(
                start_pos=Position(14, 15),
                color="red",
                pathfinding_algorithm=AStar,
                behavior=Blinky(),
                maze=self.maze,
                game=self
            ),  # Blinky
            Ghost(
                start_pos=Position(14, 16),
                color="pink",
                pathfinding_algorithm=AStar,
                behavior=Pinky(self.maze),
                maze=self.maze,
                game=self,
            ),  # Pinky (BFS)
            Ghost(
                start_pos=Position(12, 14),
                color="blue",
                pathfinding_algorithm=AStar,
                behavior=Inky(maze=self.maze, blinky=blinky),
                maze=self.maze,
                game=self
            ),  # Inky (DFS)
            Ghost(
                start_pos=Position(16, 14),
                color="orange",
                pathfinding_algorithm=AStar,
                behavior=Clyde(),
                maze=self.maze,
                game=self,
            ),  # Clyde
        ]
        self.score = 0
        self.power = False
        self.power_count = 0
        self.eaten_ghosts = [False, False, False, False]

        # Reset maze grid to its initial state
        self.maze = Maze()  # Reinitialize the maze to reset the grid

        # Reset ghosts' positions
        self.reset_ghosts()
    def reset_ghosts(self):
        for ghost in self.ghosts:
            ghost.reset()
            print(f"{ghost.color} position in pixels: ({ghost.x}, {ghost.y})")
            print(f"{ghost.color} leave_timer: {ghost.leave_timer}")

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
                self.activate_frightened_mode()
                
                # Ensure that target positions are set to None to prevent errors
                for ghost in self.ghosts:
                    ghost.target_pos = None 
                # self.eaten_ghosts = [False, False, False, False]  # Reset eaten ghosts
                
    def activate_frightened_mode(self):
        self.power = True  # Set power mode to active
        self.power_count = 0  
        self.eaten_ghosts = [False, False, False, False]
        self.power_start_time = pygame.time.get_ticks()
        # Set all ghosts to 'frightened' mode
        for ghost in self.ghosts:
            ghost.mode = GhostModes.Frightened  # Ghosts are now in frightened mode
            
           
            # ghost.speed = ghost.normal_speed // 2  # Slow down ghosts in frightened mode
    def deactivate_frightened_mode(self):
        self.power = False 
        for ghost in self.ghosts:
            if ghost.mode == GhostModes.Frightened:
                ghost.mode = GhostModes.Chase
              
                # ghost.speed = ghost.normal_speed  # Restore normal speed

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
            for ghost in self.ghosts:
                ghost.draw(self.screen)
            self.draw_misc()
            
            
            self.check_collisions()
            if self.power:
                elapsed_time = pygame.time.get_ticks() - self.power_start_time  # Time elapsed since power pellet was eaten
            
                # Deactivate power pellet effect after 10 seconds (10000 milliseconds)
                if elapsed_time > 10000:  # 10 seconds
                    self.deactivate_frightened_mode()

            
            if self.pacman.check_game_over():
                self.display_game_over()  # Display "GAME OVER"
                print("meow")
                pygame.display.flip()
                waiting_input=True
                while(waiting_input):
                    for event in pygame.event.get():
                        print(f"{event.type}")
                        if event.type==pygame.KEYDOWN:
                        
                            if event.key==pygame.K_y:
                                print(f"{event.key} pressed")
                                
                                self.restart_game()
                                waiting_input=False
                            elif event.key==pygame.K_n:
                                print(f"{event.key} pressed")
                                self.running=False
                                waiting_input=False


                
                # pygame.time.wait(3000)  # Optional: wait for 3 seconds before closing (adjust time as needed)
            # Check for pellet and power pellet collisions
            

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

            for ghost in self.ghosts:  # Only move the first three ghosts
                ghost.move(self.pacman.get_position())  # Pass Pac-Man's position to ghosts
                ghost.check_collision_with_pacman(self.pacman)


                # # 👻 Only move Blinky (ghosts[0])
            # self.ghosts[0].move(self.pacman.get_position())
            # self.ghosts[0].check_collision_with_pacman(self.pacman)

            # # Optionally check collisions for the others (even if they don't move)
            # for ghost in self.ghosts[1:]:
            #     ghost.check_collision_with_pacman(self.pacman)

            pygame.display.update()

    pygame.quit()



def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()