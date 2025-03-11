from __future__ import annotations

from typing import List

import pygame

from game.structs.direction import Direction
from utils.settings import settings, Color

TILE_LEN = settings.TILE_LEN
PI = settings.PI

class Maze:
    def __init__(self) -> None:
        self.tile_height: int       = TILE_LEN
        self.tile_width: int        = TILE_LEN
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
              
    def draw(self, screen):
        """Draws the maze elements on the screen, including flickering pellets."""
        self.flicker_counter = (self.flicker_counter + 1) % 6  # Resets every 6 frames

        for row in range(len(self.grid)):
            for col in range(len(self.grid[row])):
                center_x = col * self.tile_width + self.tile_width // 2
                center_y = row * self.tile_height + self.tile_height // 2

                if self.grid[row][col] == 1: #for dot
                    pygame.draw.circle(screen, Color.WHITE, (center_x, center_y),  4 ) #centering dot
                elif self.grid[row][col] == 2: #for big dot
                         if self.flicker_counter < 3:
                            pygame.draw.circle(screen, Color.WHITE, (center_x, center_y), 10)

                elif self.grid[row][col] == 3: #straight vertical line
                    pygame.draw.line(screen, Color.LINE_COLOR, (center_x,row*self.tile_height), (center_x, row*self.tile_height+self.tile_height) ,3)
                elif self.grid[row][col] == 4: #straight horizontal line
                    pygame.draw.line(screen, Color.LINE_COLOR, (col*self.tile_width,center_y), (col*self.tile_width+self.tile_width, center_y) ,3)

                elif self.grid[row][col] == 5: #arc
                    pygame.draw.arc(screen, Color.LINE_COLOR, [(col*self.tile_width-(self.tile_width*0.4))-2, (row*self.tile_height+(self.tile_height//2)), self.tile_width, self.tile_height] ,0, PI/2, 3)

                elif self.grid[row][col] == 6:
                    pygame.draw.arc(screen, Color.LINE_COLOR, [(col*self.tile_width+(self.tile_width//2)), (row*self.tile_height+(self.tile_height//2)), self.tile_width, self.tile_height] ,PI/2,PI, 3)

                elif self.grid[row][col] == 7:
                    pygame.draw.arc(screen, Color.LINE_COLOR, [(col*self.tile_width+(self.tile_width//2)), (row*self.tile_height-(self.tile_height*0.4)), self.tile_width, self.tile_height] ,PI, 3*PI/2, 3)

                elif self.grid[row][col] == 8:
                    pygame.draw.arc(screen, Color.LINE_COLOR, [(col*self.tile_width-(self.tile_width*0.4))-2, (row*self.tile_height-(self.tile_height*0.4)), self.tile_width, self.tile_height] ,3*PI/2,2*PI, 3)

                elif self.grid[row][col] == 9: #door for ghosts
                     pygame.draw.line(screen, Color.WHITE, (col*self.tile_width,center_y), (col*self.tile_width+self.tile_width, center_y) ,3)

    def check_position(
            self,
            centerx,
            centery,
            direction: Direction
    ) -> List[bool]:
        turns = [False, False, False, False]  # Default: No movement allowed
        fudge_factor = 15  # Small adjustment for smooth movement

        x = centerx // TILE_LEN
        y = centery // TILE_LEN

        print(x)

        if x < 28:
            # if direction == Direction.RIGHT and self.grid[y][x+1] < 3:  # Moving right
            #     turns[0] = True  # Left allowed
            # if direction == Direction.LEFT and self.grid[y][x-1] < 3:  # Moving left
            #     turns[1] = True  # Right allowed
            # if direction == Direction.UP and self.grid[y-1][x] < 3:  # Moving up
            #     turns[2] = True  # Down allowed
            # if direction == Direction.DOWN and self.grid[y+1][x] < 3:  # Moving down
            #     turns[3] = True  # Up allowed

            if direction in [Direction.UP, Direction.DOWN]:  # Vertical movement
                if self.grid[(centery + fudge_factor) // TILE_LEN][x] < 3:
                    turns[3] = True  # Down
                if self.grid[(centery - fudge_factor) // TILE_LEN][x] < 3:
                    turns[2] = True  # Up
                if self.grid[y][x-1] < 3:
                    turns[1] = True  # Left
                if self.grid[y][x+1] < 3:
                    turns[0] = True  # Right

            if direction in [Direction.RIGHT, Direction.LEFT]:  # Horizontal movement
                if self.grid[(centery + TILE_LEN) // TILE_LEN][x] < 3:
                    turns[3] = True  # Down
                if self.grid[(centery - TILE_LEN) // TILE_LEN][x] < 3:
                    turns[2] = True  # Up
                if self.grid[y][(centerx - fudge_factor) // TILE_LEN] < 3:
                    turns[1] = True  # Left
                if self.grid[y][(centerx + fudge_factor) // TILE_LEN] < 3:
                    turns[0] = True  # Right
        else:
            turns[0] = True  
            turns[1] = True

        return turns  # Return allowed movements
