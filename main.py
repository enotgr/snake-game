import pygame

from services import file_service
from classes import Snake, Apple, Menu, Button, Sound, Melon
from consts import WINDOW_WIDTH, WINDOW_HEIGHT, GAME_SURFACE_WIDTH, GAME_SURFACE_HEIGHT, SCORE_SURFACE_WIDTH, SCORE_SURFACE_HEIGHT, RETRO_FONT_PATH, LAST_SAVE_PATH, BORDER_WIDTH, BUTTON_MARGIN, BUTTON_HEIGHT, BUTTON_WIDTH, GAME_NAME, MENU_BG_TRACK, SOUNDS_PATH, FAIL_SOUND, THEMES, SAVED_THEME_PATH, CELL_SIZE, WALLS_COUNT, MAIN_ICON_PATH
from utils import get_heart, generate_walls

is_running: bool = True

def quit():
  global is_running

  is_running = False
  pygame.mixer.music.stop()

def get_record():
  record = file_service.getTextFileByPath(LAST_SAVE_PATH)
  if record:
    return int(record)
  return 0

# TODO: create util
def load_theme_name() -> str:
  theme_name: str = file_service.getTextFileByPath(SAVED_THEME_PATH)
  if theme_name:
    return theme_name
  return list(THEMES.keys())[0]

def save_record(score: int):
  file_service.saveTextFile(str(score), LAST_SAVE_PATH)

def save_theme(theme_name: str):
  file_service.saveTextFile(theme_name, SAVED_THEME_PATH)

def switch_theme(buttons: list[Button], update_menu_theme):
  theme_name: str = load_theme_name()
  theme_keys_list: list[str] = list(THEMES.keys())
  theme_index: int = theme_keys_list.index(theme_name)
  next_theme_index = theme_index + 1

  if next_theme_index >= len(theme_keys_list):
    next_theme_index = 0

  next_theme_name = theme_keys_list[next_theme_index]
  save_theme(next_theme_name)
  update_menu_theme(next_theme_name)
  for button in buttons:
    button.update_theme()

def draw_score(surface: pygame.Surface, theme_name: str, score: int, record: int, snake_lives: int):
  font = pygame.font.Font(RETRO_FONT_PATH, 16)
  text: pygame.Surface = font.render(f'Score: {score} / Record: {record}', True, THEMES[theme_name]['TEXT_COLOR'])
  surface.fill(THEMES[theme_name]['SCORE_BG_COLOR'])
  surface.blit(text, (16, 16))

  heart: pygame.Surface = get_heart(theme_name)
  for i in range(snake_lives):
    surface.blit(heart, (SCORE_SURFACE_WIDTH - (3 - i)*(40), 11))

def draw_game_over(surface: pygame.Surface, theme_name: str):
  font = pygame.font.Font(RETRO_FONT_PATH, 36)
  text_surf = font.render('Game Over', True, THEMES[theme_name]['TEXT_COLOR'])
  text_rect = text_surf.get_rect()
  text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4)
  surface.blit(text_surf, text_rect)
  pygame.display.flip()

def switch_sound(sound: Sound, sound_btn: Button):
  if sound.is_sound:
    sound_btn.set_text('Sound: On')
  else:
    sound_btn.set_text('Sound: Off')
  sound.switch_sound()

def game_event_handler(snake: Snake):
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      quit()
    elif event.type == pygame.KEYDOWN:
      snake.set_direction(event.key)

def draw_game(screen: pygame.Surface, game_surface: pygame.Surface, score_surface: pygame.Surface, theme_name: str, snake: Snake, apple: Apple, melon: Melon, score: int, record: int, walls: list[tuple[int, int]]):
  game_surface.fill(THEMES[theme_name]['BG_COLOR'])
  snake.draw(game_surface)
  apple.draw(game_surface)
  melon.draw(game_surface)

  for wall in walls:
    pygame.draw.rect(game_surface, THEMES[theme_name]['BORDER_COLOR'], (wall[0], wall[1], CELL_SIZE, CELL_SIZE))

  draw_score(score_surface, theme_name, score, record, snake.lives)
  screen.blit(game_surface, (0, 0))
  screen.blit(score_surface, (0, WINDOW_HEIGHT - SCORE_SURFACE_HEIGHT))
  border_rect = pygame.Rect(0, GAME_SURFACE_HEIGHT, WINDOW_WIDTH, BORDER_WIDTH)
  pygame.draw.rect(screen, THEMES[theme_name]['BORDER_COLOR'], border_rect)
  pygame.display.flip()

def on_game_over(screen: pygame.Surface, theme_name: str, clock: pygame.time.Clock, sound: Sound):
  draw_game_over(screen, theme_name)

  sound.play_sound(FAIL_SOUND)
  is_sound = sound.is_sound

  if is_sound:
    sound.sound_off()
  clock.tick(0.5)
  if is_sound:
    sound.sound_on()
  sound.change_music(MENU_BG_TRACK)

def start_game(screen: pygame.Surface, clock: pygame.time.Clock, sound: Sound, update_menu_record):
  global is_running

  theme_name: str = load_theme_name()
  sound.change_music(f'{SOUNDS_PATH}/{theme_name}.mp3')
  game_surface = pygame.Surface((GAME_SURFACE_WIDTH, GAME_SURFACE_HEIGHT))
  score_surface = pygame.Surface((SCORE_SURFACE_WIDTH, SCORE_SURFACE_HEIGHT))

  walls: list[tuple[int, int]] = generate_walls(WALLS_COUNT)

  snake = Snake(sound.is_sound, walls)
  apple = Apple()
  melon = Melon(3, THEMES[theme_name]['MELON_COLOR'], sound)
  score: int = 0
  record: int = get_record()
  game_loop: int = 0

  while snake.is_alive:
    if not is_running:
      return
    game_event_handler(snake)
    snake.move()

    if snake.check_food(apple.position):
      snake.grow()
      score += apple.points
      apple.new_position(walls)

    if melon.position:
      if snake.check_food(melon.position):
        snake.grow()
        score += melon.points
        melon.remove()
    elif game_loop == 300:
      melon.new_position(walls)
      melon.play_sound()
      game_loop = 0

    draw_game(screen, game_surface, score_surface, theme_name, snake, apple, melon, score, record, walls)
    clock.tick(snake.speed)
    game_loop += 1

  if score > record:
    save_record(score)
    update_menu_record(score)

  on_game_over(screen, theme_name, clock, sound)

def create_buttons() -> list[Button]:
  x = WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2
  y = WINDOW_HEIGHT // 2

  new_game_btn = Button('New Game', x, y - BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT, True)
  switch_theme_btn = Button('Switch Theme', x, y, BUTTON_WIDTH, BUTTON_HEIGHT, False)
  sound_btn = Button('Sound: Off', x, y + BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT, False)
  exit_btn = Button('Exit', x, y + 2*BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT, False, quit)

  return [new_game_btn, switch_theme_btn, sound_btn, exit_btn]

def start_menu(clock: pygame.time.Clock, menu: Menu):
  global is_running

  while is_running:
    menu.draw(quit)
    pygame.display.flip()

    if not is_running:
      pygame.quit()
      return

    clock.tick(15)

def main():
  pygame.init()
  screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
  # Здесь необходимо второй раз вызвать set_mode,
  # чтобы окно не было свернутым при запуске скомпилированного приложения в MacOS на arm64
  pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
  pygame.display.set_caption(GAME_NAME)
  icon: pygame.Surface = pygame.image.load(MAIN_ICON_PATH)
  pygame.display.set_icon(icon)
  clock = pygame.time.Clock()

  new_game_btn, switch_theme_btn, sound_btn, exit_btn = create_buttons()
  sound = Sound(MENU_BG_TRACK)
  buttons = [new_game_btn, switch_theme_btn, sound_btn, exit_btn]

  menu = Menu(screen, clock, sound, GAME_NAME, buttons, get_record())

  sound_btn.set_action(lambda: switch_sound(sound, sound_btn))
  new_game_btn.set_action(lambda: start_game(screen, clock, sound, menu.update_record))
  switch_theme_btn.set_action(lambda: switch_theme(buttons, menu.set_theme))

  start_menu(clock, menu)

if __name__ == '__main__':
  main()
