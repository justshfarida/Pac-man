from __future__ import annotations

from enum import Enum

import pygame

from game.abstract import EntityInt, EntityMethods, PathFinderInt, BehaviourInt
from game.structs import Direction, Position
from utils.settings import settings
from typing import List, Dict, TYPE_CHECKING, Tuple
import random

if TYPE_CHECKING:
    from game.pacman import Pacman

TILE_LEN = settings.TILE_LEN


ghost_leave_times = {
            "red": 0,      # Blinky leaves immediately
            "pink": 180,   # Pinky leaves after 180 units of time
            "blue": 360,   # Inky leaves after 360 units of time
            "orange": 540  # Clyde leaves after 540 units of time
        }


class GhostModes(Enum):
    Waiting = 0
    Eaten = 1
    Frightened = 2
    LeavingHouse = 3
    Chase = 4
    Scatter = 5


class Ghost(EntityInt, EntityMethods):
    def __init__(
            self,
            start_pos: Position,
            color,
            pathfinding_algorithm: PathFinderInt,
            behavior: BehaviourInt,
            maze,
            game,
            speed: int = settings.GHOST_SPEED,
    ):
        self._initial_position      = start_pos
        self._modes                 = GhostModes

        self.set_position(start_pos)
        self.rect                   = pygame.Rect(self.x - 18, self.y - 18, 36, 36)
        self.direction              = Direction.LEFT
        self.speed                  = speed
        self.color                  = color
        self.behavior               = behavior
        self.pathfinding_algorithm  = pathfinding_algorithm
        self.counter                = 0
        self.ghost_images: Dict[str, pygame.Surface] = {}
        self.maze                   = maze
        self.game                   = game
        self.path                   = []
        self.last_pacman_dir        = None

        
        self.leave_timer            = self.get_leave_time()
        self.mode                   = self._modes.Waiting
        self.target_pos             = None

        self._load_images()


    def draw(self, screen):
        match self.mode:
            case self._modes.Eaten:
                image = self.ghost_images["dead"]
            case self._modes.Frightened:
                image = self.ghost_images["frightened"]
            case _:
                image = self.ghost_images[self.color]

        screen.blit(image, (self.x - TILE_LEN // 2, self.y - TILE_LEN // 2))

    def move(self, pacman_pos = None):
        if not pacman_pos: raise ValueError("pacman_pos is None")

        if self.mode == self._modes.Waiting:
            self.leave_timer -= 1
            if self.leave_timer <= 0:
                self.mode = self._modes.LeavingHouse
                self.target_pos = self.ghost_exit_tile()
            return

        # Assign target based on mode
        if self.mode == self._modes.LeavingHouse:
            if self.get_position() == self.ghost_exit_tile():
                print(f"{self.color.capitalize()} ghost has left the house.")
                self.mode = self._modes.Chase  # Transition to chase once outside
                print(f"{self.color.capitalize()} ghost has enetered chase mode.")
                return
            self.target_pos = self.ghost_exit_tile()

        elif self.mode == self._modes.Chase:
            self.target_pos = self.behavior.get_target_position(pacman_pos, self.last_pacman_dir, self.get_position())
            if self.color == "pink": print(f"pink target {self.target_pos}, at {self.x, self.y}")
        elif self.mode == self._modes.Frightened:
              self.target_pos = self.random_target()
        elif self.mode == self._modes.Eaten:
            # self.speed =  self.speed*2
            self.target_pos = self.home_tile

        # If ghost is centered on a tile, compute new path if needed
        if self._is_centered():
            current_tile = self.get_position()
            if current_tile != self.target_pos:
                self.path = self.pathfinding_algorithm.find_path(self.get_position(), self.target_pos, self.maze)

                if not self.path:
                    print(f"[WARN] {self.color} ghost stuck at {current_tile}, can't reach {self.target_pos}")
                    self.target_pos = self.ghost_exit_tile()

            else:
                self.path = []  # Already at target, clear path

        # Move toward next tile in path
        if self.path:
            # Move toward next tile in path
            next_tile = self.path[0]  # Get the next position from the path
            next_px = next_tile[0] * TILE_LEN + TILE_LEN // 2
            next_py = next_tile[1] * TILE_LEN + TILE_LEN // 2

            dx = dy = 0
            if self.x < next_px:
                dx = self.speed
            elif self.x > next_px:
                dx = -self.speed
            if self.y < next_py:
                dy = self.speed
            elif self.y > next_py:
                dy = -self.speed

            self.x += dx
            self.y += dy
            self.rect.center = (self.x, self.y)

            # If centered and reached tile, remove it from path
            if self._is_centered() and self.get_position() == next_tile:
                self.path.pop(0)  # Move to the next tile in the path
        
        # else:
              
        #     self.path = self.random_pathfinding()
        #     print(f"Path in frightened mode: {self.path}") 
        # Transition to chase mode once outside
        if self.mode == self._modes.LeavingHouse and self.get_position() == self.ghost_exit_tile():
            print(f"{self.color.capitalize()} ghost has left the house.")
            self.mode = self._modes.Chase
            
        if self.mode == self._modes.Eaten and self.get_position() == self.home_tile:
                self.mode = self._modes.Waiting
                # self.speed =  self.speed//2
                self.leave_timer = self.get_leave_time()

    def random_target(self):
        predefined_targets = [(27, 29), (2, 29), (22, 7), (15, 12)]
        return random.choice(predefined_targets)

    def check_collision_with_pacman(
            self,
            pacman: Pacman,
    ):
        pacman_rect = pygame.Rect(pacman.x - 18, pacman.y - 18, 36, 36)

        # prevent "ghost inside wall" collision glitches
        if not self.maze.get_neighbors_for_ghost(self.get_position()):
            return  # ghost is stuck or in wall, don't collide

        if self.rect.colliderect(pacman_rect):
            if self.mode == self._modes.Frightened:
                self.mode = self._modes.Eaten
                ghost_index = self.game.ghosts.index(self)
                self.game.eaten_ghosts[ghost_index] = True
                # self.rect.center = (self.x, self.y)
            elif self.mode in [self._modes.Chase, self._modes.Scatter]:
                pacman.lose_life()
                if pacman.lives > 0:
                    print(f"Pac-Man lost a life! Lives remaining: {pacman.lives}")
                    self.game.reset_ghosts()
                else:
                    print("Game Over!")
                    self.game_over()

    @property
    def home_tile(self) -> Position:
        return self._initial_position
        
    def get_leave_time(self):
        return ghost_leave_times.get(self.color, 0)

    def ghost_exit_tile(self):
        return (14, 13)

    def ghost_home_pixel(self):
        return (14 * TILE_LEN + TILE_LEN // 2, 14 * TILE_LEN + TILE_LEN // 2)

    def random_position(self):
        return (1, 1)

    def game_over(self):
        self.running = False
        print("Game Over!")

    def reset(self):
        initial_position = self._initial_position
        self.set_position(initial_position)
        self.rect.center = (self.x, self.y)

        self.leave_timer = ghost_leave_times.get(self.color, 0)

        self.mode = self._modes.Waiting

    def _load_images(self) -> None:
        image_files = [
            ("blue", './assets/ghost_images/blue.png'),
            ("dead", './assets/ghost_images/dead.png'),
            ("orange", './assets/ghost_images/orange.png'),
            ("pink", './assets/ghost_images/pink.png'),
            ("red", './assets/ghost_images/red.png'),
            ("frightened", './assets/ghost_images/powerup.png')
        ]

        for state, file_path in image_files:
            try:
                image = pygame.image.load(file_path)
                scaled_image = pygame.transform.scale(image, settings.ENTITY_SIZE)
                self.ghost_images[state] = scaled_image
            except pygame.error:
                print(f"Error loading image: {file_path}")
                self.ghost_images[state] = None
