# import pygame
# import random
# from utils.settings import BLUE

# class Ghost:
#     def __init__(self, x, y, algorithm="BFS"):
#         self.rect = pygame.Rect(x, y, 30, 30)
#         self.color = (255, 0, 0)  # Red ghost
#         self.algorithm = algorithm  # Choose BFS, DFS, or A*
#         self.speed = 2

#     def move(self, pacman):
#         # Placeholder movement: random choice until pathfinding is added
#         direction = random.choice(["left", "right", "up", "down"])
#         if direction == "left":
#             self.rect.x -= self.speed
#         elif direction == "right":
#             self.rect.x += self.speed
#         elif direction == "up":
#             self.rect.y -= self.speed
#         elif direction == "down":
#             self.rect.y += self.speed

#     def draw(self, screen):
#         pygame.draw.circle(screen, self.color, self.rect.center, 15)
# from game import Agent
# from game import Actions
# from game import Directions
# import random
# from util import manhattanDistance
# import util

# class GhostAgent( Agent ):
#     def __init__( self, index ):
#         self.index = index

#     def getAction( self, state ):
#         dist = self.getDistribution(state)
#         if len(dist) == 0:
#             return Directions.STOP
#         else:
#             return util.chooseFromDistribution( dist )

#     def getDistribution(self, state):
#         "Returns a Counter encoding a distribution over actions from the provided state."
#         util.raiseNotDefined()

# class RandomGhost( GhostAgent ):
#     "A ghost that chooses a legal action uniformly at random."
#     def getDistribution( self, state ):
#         dist = util.Counter()
#         for a in state.getLegalActions( self.index ): dist[a] = 1.0
#         dist.normalize()
#         return dist

# class DirectionalGhost( GhostAgent ):
#     "A ghost that prefers to rush Pacman, or flee when scared."
#     def __init__( self, index, prob_attack=0.8, prob_scaredFlee=0.8 ):
#         self.index = index
#         self.prob_attack = prob_attack
#         self.prob_scaredFlee = prob_scaredFlee

#     def getDistribution( self, state ):
#         # Read variables from state
#         ghostState = state.getGhostState( self.index )
#         legalActions = state.getLegalActions( self.index )
#         pos = state.getGhostPosition( self.index )
#         isScared = ghostState.scaredTimer > 0

#         speed = 1
#         if isScared: speed = 0.5

#         actionVectors = [Actions.directionToVector( a, speed ) for a in legalActions]
#         newPositions = [( pos[0]+a[0], pos[1]+a[1] ) for a in actionVectors]
#         pacmanPosition = state.getPacmanPosition()

#         # Select best actions given the state
#         distancesToPacman = [manhattanDistance( pos, pacmanPosition ) for pos in newPositions]
#         if isScared:
#             bestScore = max( distancesToPacman )
#             bestProb = self.prob_scaredFlee
#         else:
#             bestScore = min( distancesToPacman )
#             bestProb = self.prob_attack
#         bestActions = [action for action, distance in zip( legalActions, distancesToPacman ) if distance == bestScore]

#         # Construct distribution
#         dist = util.Counter()
#         for a in bestActions: dist[a] = bestProb / len(bestActions)
#         for a in legalActions: dist[a] += ( 1-bestProb ) / len(legalActions)
#         dist.normalize()
#         return dist

import pygame
import heapq
from game.structs import Direction
from utils.settings import settings
from typing import List, Dict

TILE_LEN = settings.TILE_LEN


class Ghost:
    def __init__(self, start_pos, color, speed, behavior, maze):
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
        self.path = []

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
    # Ghost is still waiting inside
        if self.mode == "waiting":
            self.leave_timer -= 1
            if self.leave_timer <= 0:
                self.mode = "leaving_house"
            return

        # Assign target based on mode
        if self.mode == "leaving_house":
            self.target_pos = self.ghost_exit_tile()
        elif self.mode == "chase":
            pacman_tile = (pacman_pos.x, pacman_pos.y)
            if self.color == "red":
                self.target_pos = pacman_tile
            elif self.color == "pink":
                self.target_pos = self.predict_pacman_position(pacman_pos)
            elif self.color == "blue" and blinky_pos:
                self.target_pos = self.inky_logic(pacman_tile, blinky_pos)
            elif self.color == "orange":
                self.target_pos = self.clyde_logic(pacman_tile)

        # If ghost is centered on a tile, compute new path if needed
        if self._is_centered():
            current_tile = self.get_position()
            if current_tile != self.target_pos:
                self.path = self.a_star_pathfinding()
                if not self.path:
                    print(f"[WARN] {self.color} ghost stuck at {current_tile}, can't reach {self.target_pos}")
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
                print(f"[A*] {self.color} ghost neighbors at {current}: {self.maze.get_neighbors_for_ghost(current)}")
                temp_g_score = g_score[current] + 1
                if neighbor not in g_score or temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

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

    def predict_pacman_position(self, pacman_pos):
        px, py = pacman_pos.x, pacman_pos.y
        if self.direction == Direction.RIGHT:
            return (px + 1, py)
        elif self.direction == Direction.LEFT:
            return (px - 1, py)
        elif self.direction == Direction.UP:
            return (px, py - 1)
        elif self.direction == Direction.DOWN:
            return (px, py + 1)
        return (px, py)

    def inky_logic(self, pacman_tile, blinky_tile):
        px, py = pacman_tile
        bx, by = blinky_tile
        target_x = px + (px - bx)
        target_y = py + (py - by)
        return (target_x, target_y)

    def clyde_logic(self, pacman_tile):
        px, py = pacman_tile
        cx, cy = self.get_position()
        distance = abs(px - cx) + abs(py - cy)
        if distance < 8:
            return (0, settings.SCREEN_HEIGHT // TILE_LEN)
        return pacman_tile

    def check_collision_with_pacman(self, pacman):
        pacman_rect = pygame.Rect(pacman.x - 18, pacman.y - 18, 36, 36)

        # Prevent "ghost inside wall" collision glitches
        if not self.maze.get_neighbors(self.get_position()):
            return  # Ghost is stuck or in wall, don’t collide

        if self.rect.colliderect(pacman_rect):
            if self.mode == "frightened":
                self.mode = "eaten"
                self.x, self.y = self.ghost_home_pixel()
                self.rect.center = (self.x, self.y)
            elif self.mode in ["chase", "scatter"]:
                pacman.lose_life()


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
