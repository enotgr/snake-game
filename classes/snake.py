import pygame

from services import file_service
from consts import GAME_SURFACE_HEIGHT, GAME_SURFACE_WIDTH, CELL_SIZE, COMPLEXITY, EAT_SOUND, THEMES, SAVED_THEME_PATH

class Snake:
  def __init__(self, is_sound: bool, start_speed: int = COMPLEXITY):
    self.speed: int = start_speed
    self.is_alive: bool = True
    self.is_sound: bool = is_sound

    head: tuple[int, int] = (GAME_SURFACE_WIDTH // 2, GAME_SURFACE_HEIGHT // 2)
    self._body: list[tuple[int, int]] = [head, head]
    self._direction = (0, -CELL_SIZE)

    self._eat_sound: pygame.mixer.Sound = pygame.mixer.Sound(EAT_SOUND)
    self._eat_sound.set_volume(0.4)
    self._theme_name = self._load_theme_name()

  def set_direction(self, key: int):
    if (key == pygame.K_UP or key == pygame.K_w) and self._direction != (0, CELL_SIZE):
      self._direction = (0, -CELL_SIZE)
    elif (key == pygame.K_DOWN or key == pygame.K_s) and self._direction != (0, -CELL_SIZE):
      self._direction = (0, CELL_SIZE)
    elif (key == pygame.K_LEFT or key == pygame.K_a) and self._direction != (CELL_SIZE, 0):
      self._direction = (-CELL_SIZE, 0)
    elif (key == pygame.K_RIGHT or key == pygame.K_d) and self._direction != (-CELL_SIZE, 0):
      self._direction = (CELL_SIZE, 0)

  def move(self):
    new_head_pos: tuple[int, int] = (self._body[0][0] + self._direction[0], self._body[0][1] + self._direction[1])
    self._body.insert(0, new_head_pos)
    self._body.pop()
    self._check_collision()

  def grow(self):
    if self.is_sound:
      self._eat_sound.play()
    self._body.append(self._body[-1])
    self._change_speed()

  def draw(self, surface):
    for pos in self._body:
      pygame.draw.rect(surface, THEMES[self._theme_name]['SNAKE_COLOR'], (pos[0], pos[1], CELL_SIZE, CELL_SIZE))

  def check_food(self, food_position: tuple[int, int]) -> bool:
    if self._body[0] == food_position:
      return True
    return False

  def _change_speed(self):
    self.speed = COMPLEXITY + len(self._body) // 5

  def _check_collision(self):
    if (
      self._body[0][0] < 0
      or self._body[0][0] >= GAME_SURFACE_WIDTH
      or self._body[0][1] < 0
      or self._body[0][1] >= GAME_SURFACE_HEIGHT
      or self._body[0] in self._body[1:]):
      self.is_alive = False

  def _load_theme_name(self) -> str:
    theme_name: str = file_service.getTextFileByPath(SAVED_THEME_PATH)
    if theme_name:
      return theme_name
    return list(THEMES.keys())[0]
