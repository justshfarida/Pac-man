import pygame
from utils.settings import LINE_COLOR, TILE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE, PI

class Maze:
    def __init__(self):
        self.tile_height=(SCREEN_HEIGHT-50)//32
        self.tile_width=SCREEN_WIDTH//30  
        self.flicker_counter = 0  # Tracks flickering effect

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
                            pygame.draw.circle(screen, WHITE, (center_x, center_y),  4 ) #centering dot
                        elif self.grid[row][col] == 2: #for big dot
                                 if self.flicker_counter < 3:  # Show for 3 frames, hide for 3 frames
                                    pygame.draw.circle(screen, WHITE, (center_x, center_y), 10)

                        elif self.grid[row][col] == 3: #straight vertical line
                            pygame.draw.line(screen, LINE_COLOR, (center_x,row*self.tile_height), (center_x, row*self.tile_height+self.tile_height) ,3)
                        elif self.grid[row][col] == 4: #straight horizontal line
                            pygame.draw.line(screen, LINE_COLOR, (col*self.tile_width,center_y), (col*self.tile_width+self.tile_width, center_y) ,3)

                        elif self.grid[row][col] == 5: #arc
                            pygame.draw.arc(screen, LINE_COLOR, [(col*self.tile_width-(self.tile_width*0.4))-2, (row*self.tile_height+(self.tile_height//2)), self.tile_width, self.tile_height] ,0, PI/2, 3)

                        elif self.grid[row][col] == 6:
                            pygame.draw.arc(screen, LINE_COLOR, [(col*self.tile_width+(self.tile_width//2)), (row*self.tile_height+(self.tile_height//2)), self.tile_width, self.tile_height] ,PI/2,PI, 3)

                        elif self.grid[row][col] == 7:
                            pygame.draw.arc(screen, LINE_COLOR, [(col*self.tile_width+(self.tile_width//2)), (row*self.tile_height-(self.tile_height*0.4)), self.tile_width, self.tile_height] ,PI, 3*PI/2, 3)
   
                        elif self.grid[row][col] == 8:
                            pygame.draw.arc(screen, LINE_COLOR, [(col*self.tile_width-(self.tile_width*0.4))-2, (row*self.tile_height-(self.tile_height*0.4)), self.tile_width, self.tile_height] ,3*PI/2,2*PI, 3)

                        elif self.grid[row][col] == 9: #door for ghosts
                             pygame.draw.line(screen, WHITE, (col*self.tile_width,center_y), (col*self.tile_width+self.tile_width, center_y) ,3)

    def check_position(self, x, y, direction):
        """Checks if Pac-Man can move in a given direction (0: Right, 1: Left, 2: Up, 3: Down)."""
        turns = [False, False, False, False]  # Default: All directions blocked
        fudge_factor = 15  # Small adjustment for smooth movement

        grid_x = x // self.tile_width
        grid_y = y // self.tile_height

        # Ensure we do not go out of grid bounds
        max_x = len(self.grid[0]) - 1
        max_y = len(self.grid) - 1

        if 0 <= grid_x <= max_x and 0 <= grid_y <= max_y:
            # Right movement (0)
            if direction == 0 and grid_x + 1 <= max_x:
                if self.grid[grid_y][grid_x + 1] < 3:
                    turns[0] = True

            # Left movement (1)
            if direction == 1 and grid_x - 1 >= 0:
                if self.grid[grid_y][grid_x - 1] < 3:
                    turns[1] = True

            # Up movement (2)
            if direction == 2 and grid_y - 1 >= 0:
                if self.grid[grid_y - 1][grid_x] < 3:
                    turns[2] = True

            # Down movement (3)
            if direction == 3 and grid_y + 1 <= max_y:
                if self.grid[grid_y + 1][grid_x] < 3:
                    turns[3] = True

        return turns  # Return valid movement directions
