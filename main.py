import pygame

from services import file_service
from classes import Snake, Food, Menu, Button, Sound
from consts import WINDOW_WIDTH, WINDOW_HEIGHT, GAME_SURFACE_WIDTH, GAME_SURFACE_HEIGHT, SCORE_SURFACE_WIDTH, SCORE_SURFACE_HEIGHT, BG_COLOR, TEXT_COLOR, SCORE_BG_COLOR, RETRO_FONT_PATH, LAST_SAVE_PATH, BORDER_WIDTH, BORDER_COLOR, BUTTON_MARGIN, BUTTON_HEIGHT, BUTTON_WIDTH, GAME_NAME, MENU_BG_TRACK, BACKGROUND_TRACK, FAIL_SOUND

def quit():
  pygame.mixer.music.stop()
  pygame.quit()

def get_record():
  record = file_service.getTextFileByPath(LAST_SAVE_PATH)
  if record:
    return int(record)
  return 0

def save_record(score: int):
  file_service.saveTextFile(str(score), LAST_SAVE_PATH)

def draw_score(surface: pygame.Surface, score: int, record: int):
  font = pygame.font.Font(RETRO_FONT_PATH, 16)
  text = font.render(f'Score: {score} / Record: {record}', True, TEXT_COLOR)
  surface.fill(SCORE_BG_COLOR)
  surface.blit(text, (16, 16))

def draw_game_over(surface: pygame.Surface):
  font = pygame.font.Font(RETRO_FONT_PATH, 36)
  text_surf = font.render('Game Over', True, TEXT_COLOR)
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

def draw_game(screen: pygame.Surface, game_surface: pygame.Surface, score_surface: pygame.Surface, snake: Snake, food: Food, score: int, record: int):
  game_surface.fill(BG_COLOR)
  snake.draw(game_surface)
  food.draw(game_surface)
  draw_score(score_surface, score, record)
  screen.blit(game_surface, (0, 0))
  screen.blit(score_surface, (0, WINDOW_HEIGHT - SCORE_SURFACE_HEIGHT))
  border_rect = pygame.Rect(0, GAME_SURFACE_HEIGHT, WINDOW_WIDTH, BORDER_WIDTH)
  pygame.draw.rect(screen, BORDER_COLOR, border_rect)
  pygame.display.flip()
  
def on_game_over(screen: pygame.Surface, clock: pygame.time.Clock, sound: Sound):
  draw_game_over(screen)

  sound.play_sound(FAIL_SOUND)
  is_sound = sound.is_sound

  if is_sound:
    sound.sound_off()
  clock.tick(0.4)
  if is_sound:
    sound.sound_on()
  sound.change_music(MENU_BG_TRACK)

def start_game(screen: pygame.Surface, clock: pygame.time.Clock, sound: Sound, update_menu_record):
  sound.change_music(BACKGROUND_TRACK)
  game_surface = pygame.Surface((GAME_SURFACE_WIDTH, GAME_SURFACE_HEIGHT))
  score_surface = pygame.Surface((SCORE_SURFACE_WIDTH, SCORE_SURFACE_HEIGHT))

  snake = Snake(sound.is_sound)
  food = Food()
  score: int = 0
  record: int = get_record()

  while snake.is_alive:
    game_event_handler(snake)
    snake.move()

    if snake.check_food(food.position):
      snake.grow()
      score += food.points
      food.new_position()

    draw_game(screen, game_surface, score_surface, snake, food, score, record)
    clock.tick(snake.speed)

  if score > record:
    save_record(score)
    update_menu_record(score)

  on_game_over(screen, clock, sound)

def create_buttons() -> list[Button]:
  x = WINDOW_WIDTH // 2 - BUTTON_WIDTH // 2
  y = WINDOW_HEIGHT // 2

  new_game_btn = Button('New Game', x, y, BUTTON_WIDTH, BUTTON_HEIGHT, True)
  sound_btn = Button('Sound: Off', x, y + BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT, False)
  exit_btn = Button('Exit', x, y + 2*BUTTON_MARGIN, BUTTON_WIDTH, BUTTON_HEIGHT, False, quit)

  return [new_game_btn, sound_btn, exit_btn]

def start_menu(clock: pygame.time.Clock, menu: Menu):
  while True:
    menu.draw(quit)
    pygame.display.flip()
    clock.tick(15)

def main():
  pygame.init()
  screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
  pygame.display.set_caption(GAME_NAME)
  clock = pygame.time.Clock()

  new_game_btn, sound_btn, exit_btn = create_buttons()
  sound = Sound(MENU_BG_TRACK)

  sound_btn.set_action(lambda: switch_sound(sound, sound_btn))

  menu = Menu(screen, clock, sound, GAME_NAME, [new_game_btn, sound_btn, exit_btn], get_record())
  new_game_btn.set_action(lambda: start_game(screen, clock, sound, menu.update_record))

  start_menu(clock, menu)

if __name__ == '__main__':
  main()
