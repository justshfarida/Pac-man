import math
from dataclasses import dataclass


@dataclass
class Settings:
    PI: float = math.pi

    #  Screen dimensions
    TILE_LEN: int = 32
    SCREEN_WIDTH: int = 30 * TILE_LEN
    SCREEN_HEIGHT: int = 32 * TILE_LEN + 50

    PACMAN_SPEED: int = 4


class Color:
    BLACK = (0, 0, 0)
    YELLOW = (255, 255, 0)
    LINE_COLOR = (0, 0, 255)
    BLUE = (0, 0, 255)
    WHITE=(255, 255, 255)


settings = Settings()

def get_settings() -> Settings:
    return settings
