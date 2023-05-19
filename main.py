import pygame

from services import file_service
from classes import Snake, Apple, Menu, Button, Sound, Melon
from consts import WINDOW_WIDTH, WINDOW_HEIGHT, GAME_SURFACE_WIDTH, GAME_SURFACE_HEIGHT, SCORE_SURFACE_WIDTH, SCORE_SURFACE_HEIGHT, RETRO_FONT_PATH, LAST_SAVE_PATH, BUTTON_MARGIN, BUTTON_HEIGHT, BUTTON_WIDTH, GAME_NAME, MENU_BG_TRACK, SOUNDS_PATH, FAIL_SOUND, THEMES, SAVED_THEME_PATH, CELL_SIZE, MAIN_ICON_PATH, DIFFICALTIES
from utils import get_heart, generate_walls, load_theme_name

is_running: bool = True
difficalty: str = 'easy'

def quit():
  global is_running

  is_running = False
  pygame.mixer.music.stop()

def get_record():
  record = file_service.getTextFileByPath(LAST_SAVE_PATH)
  if record:
    return int(record)
  return 0

def save_record(score: int):
  file_service.saveTextFile(str(score), LAST_SAVE_PATH)

def save_theme(theme_name: str):
  file_service.saveTextFile(theme_name, SAVED_THEME_PATH)

def switch_theme(buttons: list[Button], update_menu_theme):
  theme_name: str = load_theme_name()
  theme_keys: list[str] = list(THEMES.keys())
  theme_index: int = theme_keys.index(theme_name)
  next_theme_index: int = theme_index + 1

  if next_theme_index >= len(theme_keys):
    next_theme_index = 0

  next_theme_name = theme_keys[next_theme_index]
  save_theme(next_theme_name)
  update_menu_theme(next_theme_name)
  for button in buttons:
    button.update_theme()

def draw_score(surface: pygame.Surface, theme_name: str, score: int, record: int, snake_lives: int):
  font = pygame.font.Font(RETRO_FONT_PATH, 16)
  text: pygame.Surface = font.render(f'SCORE: {score} / HI-SCORE: {record}', True, THEMES[theme_name]['MAIN_TEXT_COLOR'])
  surface.fill(THEMES[theme_name]['SCORE_BG_COLOR'])
  surface.blit(text, (16, 16))

  heart: pygame.Surface = get_heart(theme_name)
  for i in range(snake_lives):
    surface.blit(heart, (SCORE_SURFACE_WIDTH - (3 - i)*(40), 11))

def draw_game_over(surface: pygame.Surface, theme_name: str, score: int):
  font = pygame.font.Font(RETRO_FONT_PATH, 36)
  text_surf: pygame.Surface = font.render('GAME OVER', True, THEMES[theme_name]['MAIN_TEXT_COLOR'])
  text_rect: pygame.Rect = text_surf.get_rect()
  text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 4)
  surface.blit(text_surf, text_rect)

  score_font = pygame.font.Font(RETRO_FONT_PATH, 24)
  score_text_surf: pygame.Surface = score_font.render(f'SCORE: {score}', True, THEMES[theme_name]['APPLE_COLOR'])
  score_text_rect: pygame.Rect = score_text_surf.get_rect()
  score_text_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 3)
  surface.blit(score_text_surf, score_text_rect)

  pygame.display.flip()

def switch_sound(sound: Sound, sound_btn: Button):
  if sound.is_sound:
    sound_btn.set_text('Sound: On')
  else:
    sound_btn.set_text('Sound: Off')
  sound.switch_sound()

def change_difficulty(update_difficalty_btn_text):
  global difficalty

  difficalty_keys: list[str] = list(DIFFICALTIES.keys())
  difficalty_index: int = difficalty_keys.index(difficalty)
  next_difficalty_index: int = difficalty_index + 1

  if next_difficalty_index >= len(difficalty_keys):
    next_difficalty_index = 0

  difficalty = difficalty_keys[next_difficalty_index]
  update_difficalty_btn_text(f'Level: {difficalty.title()}')

def game_event_handler(snake: Snake):
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      quit()
    elif event.type == pygame.KEYDOWN:
      snake.set_direction(event.key)

def draw_game(screen: pygame.Surface, game_surface: pygame.Surface, score_surface: pygame.Surface, theme_name: str, snake: Snake, apple: Apple, melon: Melon, score: int, record: int, walls: list[tuple[int, int]]):
  game_surface.fill(THEMES[theme_name]['MAIN_BG_COLOR'])
  snake.draw(game_surface)
  apple.draw(game_surface)
  melon.draw(game_surface)

  for wall in walls:
    pygame.draw.rect(game_surface, THEMES[theme_name]['WALL_COLOR'], (wall[0], wall[1], CELL_SIZE, CELL_SIZE))

  draw_score(score_surface, theme_name, score, record, snake.lives)
  screen.blit(game_surface, (0, 0))
  screen.blit(score_surface, (0, WINDOW_HEIGHT - SCORE_SURFACE_HEIGHT))
  pygame.display.flip()

def on_game_over(screen: pygame.Surface, theme_name: str, clock: pygame.time.Clock, sound: Sound, score: int):
  draw_game_over(screen, theme_name, score)

  sound.play_sound(FAIL_SOUND)
  is_sound = sound.is_sound

  if is_sound:
    sound.sound_off()
  clock.tick(0.5)
  if is_sound:
    sound.sound_on()
  sound.change_music(MENU_BG_TRACK)

def start_game(screen: pygame.Surface, clock: pygame.time.Clock, sound: Sound, update_menu_record):
  global is_running, difficalty

  theme_name: str = load_theme_name()
  sound.change_music(f'{SOUNDS_PATH}/{theme_name}.mp3')
  game_surface = pygame.Surface((GAME_SURFACE_WIDTH, GAME_SURFACE_HEIGHT))
  score_surface = pygame.Surface((SCORE_SURFACE_WIDTH, SCORE_SURFACE_HEIGHT))

  walls: list[tuple[int, int]] = generate_walls(difficalty)

  snake = Snake(sound.is_sound, walls, DIFFICALTIES[difficalty]['START_SPEED'])
  apple = Apple(DIFFICALTIES[difficalty]['REWARD'])
  melon = Melon(3*DIFFICALTIES[difficalty]['REWARD'], THEMES[theme_name]['MELON_COLOR'], sound)
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
      apple.new_position(walls + snake.get_body())

    if melon.position:
      if snake.check_food(melon.position):
        snake.grow()
        score += melon.points
        melon.remove()
    elif game_loop == 300:
      melon.new_position(walls + snake.get_body())
      melon.play_sound()
      game_loop = 0

    draw_game(screen, game_surface, score_surface, theme_name, snake, apple, melon, score, record, walls)
    clock.tick(snake.speed)
    game_loop += 1

  if score > record:
    save_record(score)
    update_menu_record(score)

  on_game_over(screen, theme_name, clock, sound, score)

def create_main_buttons() -> list[Button]:
  x = WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2
  y = WINDOW_HEIGHT // 2

  new_game_btn = Button('New Game', x, y - BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT, True)
  switch_theme_btn = Button('Switch Theme', x, y, BUTTON_WIDTH, BUTTON_HEIGHT, False)
  options_btn = Button('Options', x, y + BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT, False)
  quit_btn = Button('Quit', x, y + 2*BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT, False, quit)

  return [new_game_btn, switch_theme_btn, options_btn, quit_btn]

def create_options_buttons() -> list[Button]:
  global difficalty

  x = WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2
  y = WINDOW_HEIGHT // 2

  difficulty_btn = Button(f'Level: {difficalty.title()}', x, y - BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT, True)
  sound_btn = Button('Sound: Off', x, y, BUTTON_WIDTH, BUTTON_HEIGHT, False)
  back_btn = Button('Back', x, y + BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT, False)

  return [difficulty_btn, sound_btn, back_btn]

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
  global difficalty

  pygame.init()
  screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
  # Здесь необходимо второй раз вызвать set_mode,
  # чтобы окно не было свернутым при запуске скомпилированного приложения в MacOS на arm64
  pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
  pygame.display.set_caption(GAME_NAME)
  icon: pygame.Surface = pygame.image.load(MAIN_ICON_PATH)
  pygame.display.set_icon(icon)
  clock = pygame.time.Clock()
  sound = Sound(MENU_BG_TRACK)

  new_game_btn, switch_theme_btn, options_btn, quit_btn = create_main_buttons()
  difficulty_btn, sound_btn, back_btn = create_options_buttons()
  main_buttons = [new_game_btn, switch_theme_btn, options_btn, quit_btn]
  options_buttons = [difficulty_btn, sound_btn, back_btn]

  menu = Menu(screen, clock, sound, GAME_NAME, main_buttons, get_record())

  new_game_btn.set_action(lambda: start_game(screen, clock, sound, menu.update_record))
  switch_theme_btn.set_action(lambda: switch_theme(main_buttons, menu.set_theme))
  options_btn.set_action(lambda: menu.set_buttons(options_buttons))
  difficulty_btn.set_action(lambda: change_difficulty(difficulty_btn.set_text))
  sound_btn.set_action(lambda: switch_sound(sound, sound_btn))
  back_btn.set_action(lambda: menu.set_buttons(main_buttons))

  start_menu(clock, menu)

if __name__ == '__main__':
  main()
