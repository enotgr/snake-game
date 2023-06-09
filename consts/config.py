GAME_NAME = 'Retro Snake'

SIZE = 600

GAME_SURFACE_HEIGHT = SIZE
GAME_SURFACE_WIDTH = SIZE

SCORE_SURFACE_HEIGHT = 48
SCORE_SURFACE_WIDTH = SIZE

BUTTON_WIDTH = 180
BUTTON_HEIGHT = 50
BUTTON_MARGIN = BUTTON_HEIGHT + 20

WINDOW_WIDTH = SIZE
WINDOW_HEIGHT = GAME_SURFACE_HEIGHT + SCORE_SURFACE_HEIGHT

CELL_SIZE = 20

DIFFICALTIES: dict[str, dict[str, int]] = {
  'easy': {
    'START_SPEED': 5,
    'WALLS_COUNT': 0,
    'REWARD': 1,
  },
  'normal': {
    'START_SPEED': 10,
    'WALLS_COUNT': 5,
    'REWARD': 2,
  },
  'high': {
    'START_SPEED': 15,
    'WALLS_COUNT': 10,
    'REWARD': 4,
  },
  'hard': {
    'START_SPEED': 20,
    'WALLS_COUNT': 15,
    'REWARD': 10,
  }
}
