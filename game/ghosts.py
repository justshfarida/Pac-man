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
from game.maze import Maze
from typing import List, TYPE_CHECKING, Dict


TILE_LEN = settings.TILE_LEN


class Ghost:
    def __init__(self, start_pos, color, speed, behavior, maze):
       
        self.x = start_pos.x * settings.TILE_LEN  # Convert start position to pixel coordinates
        self.y = start_pos.y * settings.TILE_LEN
        self.direction = Direction.LEFT  # Assuming Direction is an Enum or Class for movement
        self.speed = speed
        self.color = color
        self.behavior = behavior  # Movement strategy, e.g., Blinky, Pinky
        self.mode = "scatter"  # Modes: chase, scatter, frightened, eaten
        self.counter = 0
        self.ghost_images: Dict[str, pygame.Surface] = {}  # Initializing the dictionary
        self.maze = maze
        
        self.load_images()  # Load all ghost images

    def load_images(self) -> None:
        """Loads and scales all ghost images."""
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
                scaled_image = pygame.transform.scale(image, (36, 36))  # Adjust size as needed
                self.ghost_images[state] = scaled_image
            except pygame.error:
                print(f"Error loading image: {file_path}")
                self.ghost_images[state] = None  # If image fails to load, set to None

    def get_image(self, state: str) -> pygame.Surface:
        """Returns the image for a given ghost state."""
        return self.ghost_images.get(state)

        
    def _is_centered(self) -> bool:
        return self.x % TILE_LEN == self.y % TILE_LEN == TILE_LEN//2
    
    def draw(self, screen: pygame.Surface) -> None:
        """Draws the animated Ghost with direction adjustments."""
        self.counter = (self.counter + 1) % 20  
        frame_index = (self.counter // 5) % 4

        dest = (self.x - TILE_LEN // 2, self.y - TILE_LEN // 2)
        # Replace the player_images with ghost_images as you've loaded them
        image = self.ghost_images[self.color]  # Use the color of the ghost
        screen.blit(image, dest)




    def move(self, pacman_pos, blinky_pos=None):
        """Decide movement based on ghost behavior."""
        # Get the ghost's current position in grid coordinates
        grid_pos = self.get_position()

        # Get the valid neighboring tiles
        neighbors = self.maze.get_neighbors(grid_pos)

        # Now decide movement based on behavior
        if self.mode == "frightened":
            self.target_pos = self.random_position()  # Move randomly
        elif self.mode == "dead":
            self.target_pos = self.ghost_home()  # Return to ghost house
        else:
            if self.behavior == "blinky":
                self.target_pos = pacman_pos  # Chase Pac-Man directly
            elif self.behavior == "pinky":
                self.target_pos = self.predict_pacman_position(pacman_pos)  # Predict Pac-Man's next move
            elif self.behavior == "inky" and blinky_pos:
                self.target_pos = self.inky_logic(pacman_pos, blinky_pos)  # Complex logic
            elif self.behavior == "clyde":
                self.target_pos = self.clyde_logic(pacman_pos)  # Run away from Pac-Man

        # Find the next position using A* or another pathfinding method
        next_position = self.a_star_pathfinding()
        if next_position:
            self.x, self.y = next_position  # Move to the next tile

#     def load_images(self):
#         """Load ghost images and resize them correctly."""
#         ghost_size = (36, 36)  # Make sure the ghost size matches Pac-Man

#         try:
#             images = {
#                 "normal": pygame.transform.scale(
#                     pygame.image.load(f'./assets/ghost_images/{self.color}.png'), ghost_size
#                 ),
#                 "frightened": pygame.transform.scale(
#                     pygame.image.load('./assets/ghost_images/powerup.png'), ghost_size
#                 ),
#                 "dead": pygame.transform.scale(
#                     pygame.image.load('./assets/ghost_images/dead.png'), ghost_size
#                 )
#             }
#             return images
#         except pygame.error:
#             print(f"ERROR: Missing ghost image for {self.color}.png")
#             return None


    def a_star_pathfinding(self):
        """Uses A* to find the shortest path to the target."""
        start = (self.x // settings.TILE_LEN, self.y // settings.TILE_LEN)
        goal = self.target_pos  # self.target_pos is already a tuple (x, y)

        open_set = []
        heapq.heappush(open_set, (0, start))  # Push the starting position with a priority of 0
        came_from = {}  # To reconstruct the path later
        g_score = {start: 0}  # The cost from the start to the current node
        f_score = {start: self.heuristic(start, goal)}  # f = g + heuristic

        while open_set:
            _, current = heapq.heappop(open_set)  # Get the node with the lowest f_score

            if current == goal:
                return self.reconstruct_path(came_from, current)  # Reconstruct the path

            # Check all neighbors (up, down, left, right)
            for neighbor in self.maze.get_neighbors(current):
                temp_g_score = g_score[current] + 1  # Moving to the neighbor increases g by 1
                if neighbor not in g_score or temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None  # If no path is found

    def blinky_logic(self, pacman_pos):
        """Blinky (Red Ghost) always moves directly toward Pac-Man."""
        return pacman_pos

    def check_collision_with_pacman(self, pacman):
        """Handle collision with Pac-Man."""
        # Assume Pac-Man has the same size as the ghost
        if self.rect.colliderect(pacman.rect):  # Using Rect for collision detection
            if self.mode == "frightened":
                self.mode = "eaten"  # Ghost is eaten by Pac-Man
                self.reset_position()  # Reset ghost to the home
            elif self.mode in ["chase", "scatter"]:
                pacman.lose_life()  # Pac-Man dies on collision

    def inky_logic(self, pacman_pos, blinky_pos):
        """Inky moves using a tricky logic combining Pac-Man and Blinky's positions."""
        px, py = pacman_pos
        bx, by = blinky_pos
        target_x = px + (px - bx)
        target_y = py + (py - by)
        return (target_x, target_y)

    def clyde_logic(self, pacman_pos):
        """Clyde moves toward Pac-Man but runs away when too close."""
        px, py = pacman_pos
        cx, cy = self.x // settings.TILE_LEN, self.y // settings.TILE_LEN
        distance = abs(px - cx) + abs(py - cy)

        if distance < 8:  # If too close, run away to the corner
            return (0, settings.SCREEN_HEIGHT)  # Bottom-left corner
        return pacman_pos  # Otherwise, chase Pac-Man


    def heuristic(self, pos, goal):
        """Manhattan distance heuristic for A*."""
        return abs(pos[0] - goal[0]) + abs(pos[1] - goal[1])

    def reconstruct_path(self, came_from, current):
        """Reconstructs the path from A* and returns the next move."""
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path[1] if len(path) > 1 else None  # Return next step

    def check_collision_with_pacman(self, pacman):
        """Handle collision with Pac-Man."""
        if self.x == pacman.x and self.y == pacman.y:
            if self.mode == "frightened":
                self.mode = "eaten"  # Return to ghost house
            elif self.mode in ["chase", "scatter"]:
                pacman.lose_life()  # Pac-Man dies

    def draw(self, screen):
        """Draw the ghost with the correct sprite."""
        if self.mode == "eaten":
            image = self.ghost_images["eaten"]
        elif self.mode == "frightened":
            image = self.ghost_images["frightened"]
        else:
            image = self.ghost_images[self.color]

        screen.blit(image, (self.x, self.y))
        
    def get_position(self) -> tuple:
        """Returns the ghost's position as a (x, y) tile coordinate."""
        return (self.x // TILE_LEN, self.y // TILE_LEN)


    def predict_pacman_position(self, pacman_pos):
        """Predict Pac-Man's next position based on its current position and direction."""
        px, py = pacman_pos.x, pacman_pos.y

        # Predict Pac-Man's next position based on its current direction
        if self.direction == Direction.RIGHT:
            return (px + 1, py)  # Move one tile to the right
        elif self.direction == Direction.LEFT:
            return (px - 1, py)  # Move one tile to the left
        elif self.direction == Direction.UP:
            return (px, py - 1)  # Move one tile up
        elif self.direction == Direction.DOWN:
            return (px, py + 1)  # Move one tile down
        return pacman_pos  # Default case, if no direction
