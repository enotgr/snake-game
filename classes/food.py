import random
import pygame

from consts import GAME_SURFACE_HEIGHT, GAME_SURFACE_WIDTH, CELL_SIZE, FOOD_COLOR

class Food:
  def __init__(self, points: int = 1, color: tuple[int, int, int] = FOOD_COLOR):
    self.position: tuple[int, int] = (random.randrange(0, GAME_SURFACE_WIDTH, CELL_SIZE), random.randrange(0, GAME_SURFACE_HEIGHT, CELL_SIZE))
    self.points: int = points

    self._color: tuple[int, int, int] = color

  def new_position(self):
    self.position = (random.randrange(0, GAME_SURFACE_WIDTH, CELL_SIZE), random.randrange(0, GAME_SURFACE_HEIGHT, CELL_SIZE))

  def draw(self, surface):
    pygame.draw.rect(surface, self._color, (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))
