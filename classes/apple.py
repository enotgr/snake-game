import random

from consts import GAME_SURFACE_HEIGHT, GAME_SURFACE_WIDTH, CELL_SIZE
from .food import Food

class Apple(Food):
  def __init__(self, points: int = 1, color: tuple[int, int, int] = None):
    super().__init__(points, color)
    self.position: tuple[int, int] = (random.randrange(0, GAME_SURFACE_WIDTH, CELL_SIZE), random.randrange(0, GAME_SURFACE_HEIGHT, CELL_SIZE))
