import pygame

from consts import SNAKE_COLOR, FOOD_COLOR, TEXT_COLOR, RETRO_FONT_PATH

class Button():
  def __init__(self, text: str, x: int, y: int, width: int, height: int, active: bool = False, action = None):
    self.active: bool = active
    self.action = action

    self._text: str = text
    self._x: int = x
    self._y: int = y
    self._width: int = width
    self._height: int = height

  def draw(self, surface: pygame.Surface):
    button_surface = pygame.Surface((self._width, self._height))

    if self.active:
      button_surface.fill(SNAKE_COLOR)
    else:
      button_surface.fill(FOOD_COLOR)

    small_text = pygame.font.Font(RETRO_FONT_PATH, 12)
    text_surface = small_text.render(self._text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect()
    text_rect.center = (self._width / 2, self._height / 2)
    button_surface.blit(text_surface, text_rect)
    surface.blit(button_surface, (self._x, self._y))

  def select(self):
    self.active = True

  def deselect(self):
    self.active = False

  def set_text(self, text: str):
    self._text = text

  def set_action(self, action):
    self.action = action
