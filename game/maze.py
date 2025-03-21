from __future__ import annotations

from typing import List

import pygame

from game.structs import Position
from utils.settings import settings, Color

TILE_LEN = settings.TILE_LEN
PI = settings.PI


class Maze:
    def __init__(self) -> None:
        self.flicker_counter: int   = 0  #Tracks flickering effect

        self.grid = [
[6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5],
[3, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 1, 6, 4, 4, 5, 1, 6, 4, 4, 4, 5, 1, 3, 3, 1, 6, 4, 4, 4, 5, 1, 6, 4, 4, 5, 1, 3, 3],
[3, 3, 2, 3, 0, 0, 3, 1, 3, 0, 0, 0, 3, 1, 3, 3, 1, 3, 0, 0, 0, 3, 1, 3, 0, 0, 3, 2, 3, 3],
[3, 3, 1, 7, 4, 4, 8, 1, 7, 4, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 4, 8, 1, 7, 4, 4, 8, 1, 3, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 1, 6, 4, 4, 5, 1, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 1, 6, 4, 4, 5, 1, 3, 3],
[3, 3, 1, 7, 4, 4, 8, 1, 3, 3, 1, 7, 4, 4, 5, 6, 4, 4, 8, 1, 3, 3, 1, 7, 4, 4, 8, 1, 3, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 7, 4, 4, 4, 4, 5, 1, 3, 7, 4, 4, 5, 0, 3, 3, 0, 6, 4, 4, 8, 3, 1, 6, 4, 4, 4, 4, 8, 3],
[3, 0, 0, 0, 0, 0, 3, 1, 3, 6, 4, 4, 8, 0, 7, 8, 0, 7, 4, 4, 5, 3, 1, 3, 0, 0, 0, 0, 0, 3],
[3, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 3],
[8, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 6, 4, 4, 9, 9, 4, 4, 5, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 7],
[4, 4, 4, 4, 4, 4, 8, 1, 7, 8, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 7, 8, 1, 7, 4, 4, 4, 4, 4, 4],
[0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
[4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4],
[5, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 7, 4, 4, 4, 4, 4, 4, 8, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 6],
[3, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 3],
[3, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 6, 4, 4, 4, 4, 4, 4, 5, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 3],
[3, 6, 4, 4, 4, 4, 8, 1, 7, 8, 0, 7, 4, 4, 5, 6, 4, 4, 8, 0, 7, 8, 1, 7, 4, 4, 4, 4, 5, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 1, 6, 4, 4, 5, 1, 6, 4, 4, 4, 5, 1, 3, 3, 1, 6, 4, 4, 4, 5, 1, 6, 4, 4, 5, 1, 3, 3],
[3, 3, 1, 7, 4, 5, 3, 1, 7, 4, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 4, 8, 1, 3, 6, 4, 8, 1, 3, 3],
[3, 3, 2, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 2, 3, 3],
[3, 7, 4, 5, 1, 3, 3, 1, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 1, 3, 3, 1, 6, 4, 8, 3],
[3, 6, 4, 8, 1, 7, 8, 1, 3, 3, 1, 7, 4, 4, 5, 6, 4, 4, 8, 1, 3, 3, 1, 7, 8, 1, 7, 4, 5, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 3, 1, 6, 4, 4, 4, 4, 8, 7, 4, 4, 5, 1, 3, 3, 1, 6, 4, 4, 8, 7, 4, 4, 4, 4, 5, 1, 3, 3],
[3, 3, 1, 7, 4, 4, 4, 4, 4, 4, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 4, 4, 4, 4, 4, 4, 8, 1, 3, 3],
[3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
[3, 7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8, 3],
[7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8]
         ]
              
    def draw(
            self,
            screen: pygame.Surface
    ) -> None:
        """Draws the maze elements on the screen, including flickering pellets."""
        self.flicker_counter = (self.flicker_counter + 1) % 60  # Resets every 6 frames

        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                center_x = col * TILE_LEN + TILE_LEN // 2
                center_y = row * TILE_LEN + TILE_LEN // 2

                match self.grid[row][col]:
                    case 1: # dot
                        pygame.draw.circle(
                            surface=screen,
                            color=Color.WHITE,
                            center=(center_x, center_y), #centering dot
                            radius=4,
                        )
                    case 2: # big dot
                        if self.flicker_counter > 30:
                            pygame.draw.circle(
                                surface=screen,
                                color=Color.WHITE,
                                center=(center_x, center_y),
                                radius=10,
                            )
                    case 3: #straight vertical line
                        pygame.draw.line(
                            surface=screen,
                            color=Color.LINE_COLOR,
                            start_pos=(center_x, row*TILE_LEN),
                            end_pos=(center_x, (row+1)*TILE_LEN),
                            width=3,
                        )
                    case 4: #straight horizontal line
                        pygame.draw.line(
                            surface=screen,
                            color=Color.LINE_COLOR,
                            start_pos=(col*TILE_LEN, center_y),
                            end_pos=((col+1)*TILE_LEN, center_y),
                            width=3,
                        )
                    case 5: #arc
                        pygame.draw.arc(
                            surface=screen,
                            color=Color.LINE_COLOR,
                            rect=[
                                (col*TILE_LEN-(TILE_LEN*0.4))-2,
                                (row*TILE_LEN+(TILE_LEN//2)),
                                TILE_LEN,
                                TILE_LEN,
                            ],
                            start_angle=0,
                            stop_angle=PI/2,
                            width=3,
                        )
                    case 6:
                        pygame.draw.arc(
                            surface=screen,
                            color=Color.LINE_COLOR,
                            rect=[
                                (col*TILE_LEN+(TILE_LEN//2)),
                                (row*TILE_LEN+(TILE_LEN//2)),
                                TILE_LEN,
                                TILE_LEN,
                            ],
                            start_angle=PI/2,
                            stop_angle=PI,
                            width=3,
                        )
                    case 7:
                        pygame.draw.arc(
                            surface=screen,
                            color=Color.LINE_COLOR,
                            rect=[
                                (col*TILE_LEN+(TILE_LEN//2)),
                                (row*TILE_LEN-(TILE_LEN*0.4)),
                                TILE_LEN,
                                TILE_LEN,
                            ],
                            start_angle=PI,
                            stop_angle=3*PI/2,
                            width=3,
                        )
                    case 8:
                        pygame.draw.arc(
                            surface=screen,
                            color=Color.LINE_COLOR,
                            rect=[
                                (col*TILE_LEN-(TILE_LEN*0.4))-2,
                                (row*TILE_LEN-(TILE_LEN*0.4)),
                                TILE_LEN,
                                TILE_LEN,
                            ],
                            start_angle=3*PI/2,
                            stop_angle=2*PI,
                            width=3,
                        )
                    case 9: #door for ghosts
                        pygame.draw.line(
                            surface=screen,
                            color=Color.WHITE,
                            start_pos=(col*TILE_LEN, center_y),
                            end_pos=((col+1)*TILE_LEN, center_y),
                            width=3,
                        )

    def check_position(
            self,
            grid_pos: Position,
    ) -> List[bool]:
        turns = [False, False, False, False]  # Default: No movement allowed
        x, y = grid_pos.x, grid_pos.y

        if x < 28:
            if self.grid[y+1][x] < 3:
                turns[3] = True  # Down
            if self.grid[y-1][x] < 3:
                turns[2] = True  # Up
            if self.grid[y][x-1] < 3:
                turns[1] = True  # Left
            if self.grid[y][x+1] < 3:
                turns[0] = True  # Right
        else:
            turns[0] = True  
            turns[1] = True

        return turns  # Return allowed movements

    
    def get_neighbors(self, position: tuple) -> List[tuple]:
        """Returns a list of valid neighboring positions (up, down, left, right) in grid coordinates."""
        neighbors = []
        x, y = position  # Unpack the tuple into x and y for grid coordinates

        # Check for the neighbor to the left (if within bounds)
        if x > 0 and self.grid[y][x - 1] != 3:  # Ensure it's not a wall (3 represents a wall)
            neighbors.append((x - 1, y))  # Append as a tuple (x-1, y)

        # Check for the neighbor to the right (if within bounds)
        if x < len(self.grid[0]) - 1 and self.grid[y][x + 1] != 3:  # Ensure it's not a wall
            neighbors.append((x + 1, y))

        # Check for the neighbor above (if within bounds)
        if y > 0 and self.grid[y - 1][x] != 3:  # Ensure it's not a wall
            neighbors.append((x, y - 1))

        # Check for the neighbor below (if within bounds)
        if y < len(self.grid) - 1 and self.grid[y + 1][x] != 3:  # Ensure it's not a wall
            neighbors.append((x, y + 1))

        return neighbors
