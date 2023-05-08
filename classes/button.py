import pygame

from consts import SNAKE_COLOR, FOOD_COLOR, TEXT_COLOR, RETRO_FONT_PATH

class Button():
  def __init__(self, text: str, x: int, y: int, width: int, height: int, active: bool = False, action = None):
    self.text: str = text
    self.x: int = x
    self.y: int = y
    self.width: int = width
    self.height: int = height
    self.active: bool = active
    self.action = action

  def draw(self, surface: pygame.Surface):
    button_surface = pygame.Surface((self.width, self.height))

    if self.active:
      button_surface.fill(SNAKE_COLOR)
    else:
      button_surface.fill(FOOD_COLOR)

    small_text = pygame.font.Font(RETRO_FONT_PATH, 12)
    text_surface = small_text.render(self.text, True, TEXT_COLOR)
    text_rect = text_surface.get_rect()
    text_rect.center = (self.width / 2, self.height / 2)
    button_surface.blit(text_surface, text_rect)
    surface.blit(button_surface, (self.x, self.y))

  def select(self):
    self.active = True

  def deselect(self):
    self.active = False

  def set_text(self, text: str):
    self.text = text

  def set_action(self, action):
    self.action = action
