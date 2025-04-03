import pygame
import heapq
from game.structs import Direction
from utils.settings import settings
from typing import List, Dict
import heapq
from collections import deque

TILE_LEN = settings.TILE_LEN


class Ghost:
    def __init__(self, start_pos, color, speed, behavior, maze, game):
        self.x = start_pos.x * TILE_LEN + TILE_LEN // 2
        self.y = start_pos.y * TILE_LEN + TILE_LEN // 2
        self.rect = pygame.Rect(self.x - 18, self.y - 18, 36, 36)
        self.direction = Direction.LEFT
        self.speed = speed
        self.color = color
        self.behavior = behavior
        self.counter = 0
        self.ghost_images: Dict[str, pygame.Surface] = {}
        self.maze = maze
        self.game = game
        self.path = []
        self.last_pacman_dir = None

        ghost_leave_times = {
            "red": 0,
            "pink": 180,
            "blue": 360,
            "orange": 540
        }
        self.leave_timer = ghost_leave_times.get(self.color, 0)
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
                self.target_pos = self.ghost_exit_tile()  # Ensure exit target is set
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
                
#####################################################
                pacman_dir = self.game.pacman.direction
                
                if self.last_pacman_dir != pacman_dir or self.target_pos is None:
                    self.last_pacman_dir = pacman_dir
                    self.target_pos = self.predict_pacman_position(
                        pacman_pos,
                        pacman_dir,
                        self.maze
                    )
                            
     ##################################           
                # self.target_pos = self.predict_pacman_position(pacman_pos)
            # elif self.color == "blue" and blinky_pos:
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

        # If ghost is centered on a tile, compute new path if needed
        if self._is_centered():
            current_tile = self.get_position()
            if current_tile != self.target_pos:
                if self.color == "red":
                    self.path = self.a_star_pathfinding()
                elif self.color == "pink":
                    self.path = self.a_star_pathfinding()
                elif self.color == "blue":
                    self.path = self.a_star_pathfinding()

                if not self.path:
                    print(f"[WARN] {self.color} ghost stuck at {current_tile}, can't reach {self.target_pos}")
                    self.target_pos = self.ghost_exit_tile()

            else:
                self.path = []  # Already at target, clear path

        # Move toward next tile in path
        if self.path:
            next_tile = self.path[0]
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
                self.path.pop(0)

        # Transition to chase mode once outside
        if self.mode == "leaving_house" and self.get_position() == self.ghost_exit_tile():
            print(f"{self.color.capitalize()} ghost has left the house.")
            self.mode = "chase"
       

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

    def reconstruct_path(self, came_from, current):
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def heuristic(self, pos, goal):
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    # def predict_pacman_position(self, pacman_pos):
    #     px, py = pacman_pos.x, pacman_pos.y
    #     if self.direction == Direction.RIGHT:
    #         return (px + 4, py)
    #     elif self.direction == Direction.LEFT:
    #         return (px - 4, py)
    #     elif self.direction == Direction.UP:
    #         return (px, py -4)
    #     elif self.direction == Direction.DOWN:
    #         return (px, py + 4)
    #     return (px, py)
    
#     from game.structs import Position
# from utils.enums import Direction  # Assuming you have a Direction enum

    def predict_pacman_position(self, pacman_pos, pacman_dir, maze, max_steps=4): #-> tuple[int, int]:
        """
        Predicts up to 4 tiles ahead of Pac-Man. Falls back if tiles are invalid (walls or out of bounds).
        Returns a valid tile (x, y).
        """
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
                if maze.grid[ty][tx] != 3:  # Not a wall
                    return (tx, ty)

        # All ahead tiles are walls or out-of-bounds → fallback to Pac-Man’s current tile
        return (px, py)


    # def inky_logic(self, pacman_tile, blinky_tile):
    #     px, py = pacman_tile
    #     bx, by = blinky_tile
    #     target_x = px + (px - bx)
    #     target_y = py + (py - by)
    #     return (target_x, target_y)
    
    
    def inky_logic(self, pacman_pos, pacman_dir, blinky_pos, maze, max_map_size=(30, 31)):

        # Step 1: 2 tiles ahead of Pac-Man
        direction_vectors = {
            Direction.RIGHT: (1, 0),
            Direction.LEFT:  (-1, 0),
            Direction.UP:    (0, -1),
            Direction.DOWN:  (0, 1),
        }

        dx, dy = direction_vectors.get(pacman_dir, (0, 0))
        ahead_x = pacman_pos.x + dx * 2
        ahead_y = pacman_pos.y + dy * 2

        # Step 2: Vector from Blinky to 2-ahead position
        vx = ahead_x - blinky_pos[0]
        vy = ahead_y - blinky_pos[1]

        # Step 3: Double the vector and get final target
        target_x = blinky_pos[0] + 2 * vx
        target_y = blinky_pos[1] + 2 * vy

        # Step 4: Optional – keep within map bounds
        max_x, max_y = max_map_size
        target_x = max(0, min(target_x, max_x - 1))
        target_y = max(0, min(target_y, max_y - 1))

        # Step 5: Optional – make sure it's not a wall
        if maze.grid[target_y][target_x] == 3:
            # fallback to a nearby walkable tile or Pac-Man
            return (pacman_pos.x, pacman_pos.y)

        return (target_x, target_y)


    def clyde_logic(self, pacman_tile):
        px, py = pacman_tile
        cx, cy = self.get_position()
        distance = abs(px - cx) + abs(py - cy)

        if distance < 8:
            return (0, len(self.maze.grid) - 1)
        return pacman_tile


    def check_collision_with_pacman(self, pacman):
        pacman_rect = pygame.Rect(pacman.x - 18, pacman.y - 18, 36, 36)

        # Prevent "ghost inside wall" collision glitches
        if not self.maze.get_neighbors_for_ghost(self.get_position()):
            return  # Ghost is stuck or in wall, don't collide

        if self.rect.colliderect(pacman_rect):
            if self.mode == "frightened":
                self.mode = "eaten"
                self.x, self.y = self.ghost_home_pixel()
                self.rect.center = (self.x, self.y)
            elif self.mode in ["chase", "scatter"]:
                pacman.lose_life()
                if pacman.lives > 0:
                    print(f"Pac-Man lost a life! Lives remaining: {pacman.lives}")
                    self.game.reset_ghosts()
                else:
                    print("Game Over!")
                    self.game_over()

    def ghost_home_tile(self):
        return (14, 14)

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
