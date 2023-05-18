import random
import pygame

from consts import GAME_SURFACE_HEIGHT, GAME_SURFACE_WIDTH, CELL_SIZE, THEMES
from utils import load_theme_name

class Food:
  def __init__(self, points: int = 1, color: tuple[int, int, int] = None):
    self.position: tuple[int, int] = None
    self.points: int = points

    self._theme_name: str = load_theme_name()
    self._color: tuple[int, int, int] = THEMES[self._theme_name]['APPLE_COLOR']

    if color:
      self._color = color

  def new_position(self, inaccessible_positions: list[tuple[int, int]] = []):
    new_position: tuple[int, int] = (random.randrange(0, GAME_SURFACE_WIDTH, CELL_SIZE), random.randrange(0, GAME_SURFACE_HEIGHT, CELL_SIZE))

    while new_position in inaccessible_positions:
      new_position = (random.randrange(0, GAME_SURFACE_WIDTH, CELL_SIZE), random.randrange(0, GAME_SURFACE_HEIGHT, CELL_SIZE))

    self.position = new_position

  def draw(self, surface):
    pygame.draw.rect(surface, self._color, (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))
