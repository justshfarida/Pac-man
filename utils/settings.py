import math
from dataclasses import dataclass
from typing import Tuple


@dataclass
class Settings:
    PI: float = math.pi

    #  Screen dimensions
    TILE_LEN: int = 24
    SCREEN_WIDTH: int = 30 * TILE_LEN
    SCREEN_HEIGHT: int = 32 * TILE_LEN + 60

    PACMAN_SPEED: int = 4
    GHOST_SPEED: int = 3
    ENTITY_SIZE: Tuple[int, int] = (pixels:=TILE_LEN*4//3, pixels)


class Color:
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)
    LINE_COLOR = (0, 0, 255)
    BLUE = (0, 0, 255)
    WHITE=(255, 255, 255)


settings = Settings()

def get_settings() -> Settings:
    return settings
