import pygame

from consts import WINDOW_WIDTH, WINDOW_HEIGHT, RETRO_FONT_PATH, SWITCH_BUTTON, ENTER_BUTTON, THEMES
from utils import load_theme_name
from .button import Button
from .sound import Sound

class Menu:
  def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, sound: Sound, title: str, buttons: list[Button] = [], record: int = 0):
    self._screen: pygame.Surface = screen
    self._clock: pygame.time.Clock = clock
    self._sound: Sound = sound
    self._title: str = title
    self._buttons: list[Button] = buttons
    self._record: int = record
    self._theme_name: str = load_theme_name()
    self._theme: dict[str, tuple[int, int, int]] = THEMES[self._theme_name]

  def draw(self, quit):
    self._event_handler(quit)

    self._screen.fill(self._theme['MAIN_BG_COLOR'])
    self._draw_title()
    self._draw_record()
    self._draw_theme_name()
    self._draw_author()

    for button in self._buttons:
      button.draw(self._screen)

    pygame.display.flip()
    self._clock.tick(15)

  def add_button(self, button: Button):
    self._buttons.append(button)

  def set_buttons(self, buttons: list[Button]):
    self._buttons = buttons
    for button in self._buttons:
      button.update_theme(self._theme_name)

    self._switch_active_button(0)

  def update_record(self, record: int):
    self._record = record

  def set_theme(self, theme_name: str):
    self._theme_name = theme_name
    self._theme = THEMES[self._theme_name]

  def _event_handler(self, quit):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        quit()
      elif event.type == pygame.KEYDOWN:
        active_index: int = self._find_active_button_index()

        if (event.key == pygame.K_UP or event.key == pygame.K_w):
          self._sound.play_sound(SWITCH_BUTTON)
          new_index: int = active_index - 1

          if new_index == -1:
            new_index = len(self._buttons) - 1
          self._switch_active_button(new_index)
        elif (event.key == pygame.K_DOWN or event.key == pygame.K_s):
          self._sound.play_sound(SWITCH_BUTTON)
          new_index: int = active_index + 1

          if new_index == len(self._buttons):
            new_index = 0
          self._switch_active_button(new_index)
        elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
          active_button = self._buttons[active_index]
          self._sound.play_sound(ENTER_BUTTON)
          if active_button.action != None:
            active_button.action()
        elif event.key == pygame.K_ESCAPE:
          quit()

  def _switch_active_button(self, active_index: int = 0):
    for i in range(len(self._buttons)):
      if i == active_index:
        self._buttons[i].select()
      else:
        self._buttons[i].deselect()

  def _find_active_button_index(self) -> int:
    for i in range(len(self._buttons)):
      if self._buttons[i].active:
        return i
    return -1

  def _draw_title(self):
    large_text = pygame.font.Font(RETRO_FONT_PATH, 30)
    text_surf: pygame.Surface = large_text.render(self._title, True, self._theme['APPLE_COLOR'])
    text_rect: pygame.Rect = text_surf.get_rect()
    text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4)
    self._screen.blit(text_surf, text_rect)

  def _draw_record(self):
    font = pygame.font.Font(RETRO_FONT_PATH, 20)
    text_surf: pygame.Surface = font.render(f'HI-SCORE: {self._record}', True, self._theme['MAIN_TEXT_COLOR'])
    text_rect: pygame.Rect = text_surf.get_rect()
    text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4 + 50)
    self._screen.blit(text_surf, text_rect)

  def _draw_theme_name(self):
    font = pygame.font.Font(RETRO_FONT_PATH, 14)
    theme_title_name: str = ' '.join(self._theme_name.split('_')).title()
    text_surf: pygame.Surface = font.render(f'Theme: {theme_title_name}', True, self._theme['WALL_COLOR'])
    text_rect: pygame.Rect = text_surf.get_rect()
    self._screen.blit(text_surf, (20, WINDOW_HEIGHT - text_rect.height - 20))

  def _draw_author(self):
    font = pygame.font.Font(RETRO_FONT_PATH, 10)
    text_surf: pygame.Surface = font.render('by Mikhail Krotov', True, self._theme['WALL_COLOR'])
    text_rect: pygame.Rect = text_surf.get_rect()
    self._screen.blit(text_surf, (WINDOW_WIDTH - text_rect.width - 20, WINDOW_HEIGHT - text_rect.height - 20))
