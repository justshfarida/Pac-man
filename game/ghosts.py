import pygame
import heapq
from game.structs import Direction, Position
from utils.settings import settings
from typing import List, Dict
import heapq
import random
from collections import deque

TILE_LEN = settings.TILE_LEN


class Ghost:
    def __init__(self, start_pos, color, pathfinding_algorithm, speed, behavior, maze, game):
        self.x = start_pos.x * TILE_LEN + TILE_LEN // 2
        self.y = start_pos.y * TILE_LEN + TILE_LEN // 2
        self.rect = pygame.Rect(self.x - 18, self.y - 18, 36, 36)
        self.direction = Direction.LEFT
        self.speed = speed
        self.color = color
        self.behavior = behavior
        self.pathfinding_algorithm = pathfinding_algorithm
        self.counter = 0
        self.ghost_images: Dict[str, pygame.Surface] = {}
        self.maze = maze
        self.game = game
        self.path = []
        self.last_pacman_dir = None

        
        self.leave_timer = self.set_ghost_leave_times()
        self.mode = "waiting"
        self.target_pos = None

        self.load_images()

    def load_images(self) -> None:
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
                scaled_image = pygame.transform.scale(image, (36, 36))
                self.ghost_images[state] = scaled_image
            except pygame.error:
                print(f"Error loading image: {file_path}")
                self.ghost_images[state] = None

    def draw(self, screen):
        if self.mode == "eaten":
            image = self.ghost_images["dead"]
        elif self.mode == "frightened":
            image = self.ghost_images["frightened"]
        else:
            image = self.ghost_images[self.color]

        screen.blit(image, (self.x - TILE_LEN // 2, self.y - TILE_LEN // 2))

    def get_position(self) -> tuple:
        return (self.x // TILE_LEN, self.y // TILE_LEN)
    

    def move(self, pacman_pos, blinky_pos=None):
        if self.mode == "waiting":
            self.leave_timer -= 1
            if self.leave_timer <= 0:
                self.mode = "leaving_house"
                self.target_pos = self.ghost_exit_tile()  
            return

        # Assign target based on mode
        if self.mode == "leaving_house":
            if self.get_position() == self.ghost_exit_tile():
                print(f"{self.color.capitalize()} ghost has left the house.")
                self.mode = "chase"  # Transition to chase once outside
                print(f"{self.color.capitalize()} ghost has enetered chase mode.")
                return
            self.target_pos = self.ghost_exit_tile()

        elif self.mode == "chase":
            pacman_tile = (pacman_pos.x, pacman_pos.y)

            if self.color == "red":
                self.target_pos = pacman_tile
            elif self.color == "pink":
                
                pacman_dir = self.game.pacman.direction
                
                if self.last_pacman_dir != pacman_dir or self.target_pos is None:
                    self.last_pacman_dir = pacman_dir
                    self.target_pos = self.predict_pacman_position(
                        pacman_pos,
                        pacman_dir,
                        self.maze
                    )
                            

            elif self.color == "blue":
                print(blinky_pos)
                self.target_pos = self.inky_logic(
                                                        pacman_pos=self.game.pacman.get_position() ,
                                                        pacman_dir=self.game.pacman.direction,
                                                        blinky_pos=blinky_pos,
                                                        maze=self.maze
                                                    )
            elif self.color == "orange":
                self.target_pos = self.clyde_logic(pacman_tile)
                
        elif self.mode == "frightened":
              self.target_pos = self.random_target()
              
        elif self.mode == "eaten":
            # self.speed =  self.speed*2

        
            self.target_pos = self.ghost_home_tile() 
        # If ghost is centered on a tile, compute new path if needed
        if self._is_centered():
            current_tile = self.get_position()
            if current_tile != self.target_pos:
                # if self.mode != "frightened":
                if self.pathfinding_algorithm == 'astar':
                    self.path = self.a_star_pathfinding()
                elif self.pathfinding_algorithm == 'dfs':
                    self.path = self.dfs_pathfinding()
                elif self.pathfinding_algorithm == 'bfs':
                    self.path = self.bfs_pathfinding()
                # else:  
                #     self.path = self.random_pathfinding()



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
        if self.mode == "leaving_house" and self.get_position() == self.ghost_exit_tile():
            print(f"{self.color.capitalize()} ghost has left the house.")
            self.mode = "chase"
            
        if self.mode == "eaten" and self.get_position() == self.ghost_home_tile():
                self.mode = "waiting"
                # self.speed =  self.speed//2
                self.leave_timer = self.set_ghost_leave_times()          

    def move_to_tile(self, tile):
        self.x = tile[0] * TILE_LEN + TILE_LEN // 2
        self.y = tile[1] * TILE_LEN + TILE_LEN // 2
        self.rect.center = (self.x, self.y)


  
    def a_star_pathfinding(self):
        start = self.get_position()
        goal = self.target_pos
        print(f"[A*] Target: {goal}")

        open_set = []
        heapq.heappush(open_set, (0, start))    
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            _, current = heapq.heappop(open_set)
            if current == goal:
                return self.reconstruct_path(came_from, current)

            for neighbor in self.maze.get_neighbors_for_ghost(current):
                # print(f"[A*] {self.color} ghost neighbors at {current}: {self.maze.get_neighbors_for_ghost(current)}")
                temp_g_score = g_score[current] + 1
                if neighbor not in g_score or temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return []

    def bfs_pathfinding(self, start, goal):
        visited = set()
        queue = deque([(start, [])])

        while queue:
            current, path = queue.popleft()
            if current == goal:
                return path

            for neighbor in self.maze.get_neighbors_for_ghost(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return []

    def dfs_pathfinding(self, start, goal):
        visited = set()
        stack = [(start, [])]

        while stack:
            current, path = stack.pop()

            if current == goal:
                return path

            for neighbor in self.maze.get_neighbors_for_ghost(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor]))

        return []


    def random_target(self):
        predefined_targets = [(27, 29), (2, 29), (22, 7), (15, 12)]
        return random.choice(predefined_targets)
    

    def reconstruct_path(self, came_from, current):
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def heuristic(self, pos, goal):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    

    def predict_pacman_position(self, pacman_pos, pacman_dir, maze, max_steps=4): #-> tuple[int, int]:
   
        direction_vectors = {
            Direction.RIGHT: (1, 0),
            Direction.LEFT:  (-1, 0),
            Direction.UP:    (0, -1),
            Direction.DOWN:  (0, 1),
        }

        dx, dy = direction_vectors.get(pacman_dir, (0, 0))
        px, py = pacman_pos.x, pacman_pos.y

        for steps in range(max_steps, 0, -1):
            tx = px + dx * steps
            ty = py + dy * steps

            # Bounds check
            if 0 <= ty < len(maze.grid) and 0 <= tx < len(maze.grid[0]):
                if maze.grid[ty][tx] != 3:  
                    return (tx, ty)

        # If all ahead tiles are walls or out-of-bounds, fallback to Pac-Man’s current tile
        return (px, py)


    
    def inky_logic(self, pacman_pos, pacman_dir, blinky_pos, maze, max_map_size=(30, 31)):

        # 2 tiles ahead of Pac-Man
        direction_vectors = {
            Direction.RIGHT: (1, 0),
            Direction.LEFT:  (-1, 0),
            Direction.UP:    (0, -1),
            Direction.DOWN:  (0, 1),
        }

        dx, dy = direction_vectors.get(pacman_dir, (0, 0))
        ahead_x = pacman_pos.x + dx * 2
        ahead_y = pacman_pos.y + dy * 2

        # Vector from Blinky to 2-ahead position
        vx = ahead_x - blinky_pos[0]
        vy = ahead_y - blinky_pos[1]

        # Double the vector and get final target
        target_x = blinky_pos[0] + 2 * vx
        target_y = blinky_pos[1] + 2 * vy

        #Keep target within map bounds
        max_x, max_y = max_map_size
        target_x = max(0, min(target_x, max_x - 1))
        target_y = max(0, min(target_y, max_y - 1))

        #Make sure target is not a wall
        if maze.grid[target_y][target_x] == 3:
            # fallback to a nearby walkable tile or Pac-Man
            return (pacman_pos.x, pacman_pos.y)

        return (target_x, target_y)


    def clyde_logic(self, pacman_tile):
        px, py = pacman_tile
        cx, cy = self.get_position()
        distance = abs(px - cx) + abs(py - cy)

        if distance < 8:
            return (2,30)
        return pacman_tile


    def check_collision_with_pacman(self, pacman):
        pacman_rect = pygame.Rect(pacman.x - 18, pacman.y - 18, 36, 36)

        # prevent "ghost inside wall" collision glitches
        if not self.maze.get_neighbors_for_ghost(self.get_position()):
            return  # ghost is stuck or in wall, don't collide

        if self.rect.colliderect(pacman_rect):
            if self.mode == "frightened":
                self.mode = "eaten"
                ghost_index = self.game.ghosts.index(self)
                self.game.eaten_ghosts[ghost_index] = True
                # self.rect.center = (self.x, self.y)
            elif self.mode in ["chase", "scatter"]:
                pacman.lose_life()
                if pacman.lives > 0:
                    print(f"Pac-Man lost a life! Lives remaining: {pacman.lives}")
                    self.game.reset_ghosts()
                else:
                    print("Game Over!")
                    self.game_over()

    def ghost_home_tile(self):
        initial_positions = {
            "red": (14, 15),  # Blinky's initial position
            "pink": (14, 16),  # Pinky's initial position
            "blue": (12, 14),  # Inky's initial position
            "orange":(16, 14) # Clyde's initial position
        }
        
        
        return initial_positions.get(self.color, (14, 15))
        
    def set_ghost_leave_times(self):
        
        ghost_leave_times = {
            "red": 0,      # Blinky leaves immediately
            "pink": 180,   # Pinky leaves after 180 units of time
            "blue": 360,   # Inky leaves after 360 units of time
            "orange": 540  # Clyde leaves after 540 units of time
        }

        return ghost_leave_times.get(self.color, 0) 
        


    def ghost_exit_tile(self):
        return (14, 13)

    def ghost_home_pixel(self):
        return (14 * TILE_LEN + TILE_LEN // 2, 14 * TILE_LEN + TILE_LEN // 2)

    def random_position(self):
        return (1, 1)

    def _is_centered(self):
        return self.x % TILE_LEN == self.y % TILE_LEN == TILE_LEN // 2

    def game_over(self):
        self.running = False
        print("Game Over!")
