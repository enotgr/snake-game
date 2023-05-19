import random

from consts import GAME_SURFACE_HEIGHT, GAME_SURFACE_WIDTH, CELL_SIZE

HORIZONTAL_CELLS_COUNT = GAME_SURFACE_WIDTH // CELL_SIZE
VERTICAL_CELLS_COUNT = GAME_SURFACE_HEIGHT // CELL_SIZE

def generate_random_walls(wall_count: int = 10) -> list[tuple[int, int]]:
  walls = []
  for _ in range(wall_count):
    wall_x = random.randint(1, HORIZONTAL_CELLS_COUNT - 2)
    wall_y = random.randint(1, VERTICAL_CELLS_COUNT - 2)
    while (wall_x, wall_y) in walls:
      wall_x = random.randint(1, HORIZONTAL_CELLS_COUNT - 2)
      wall_y = random.randint(1, VERTICAL_CELLS_COUNT - 2)
    walls.append((wall_x*CELL_SIZE, wall_y*CELL_SIZE))
  return walls

def generate_walls(level: str) -> list[tuple[int, int]]:
  walls: list[tuple[int, int]] = []

  center_x = HORIZONTAL_CELLS_COUNT // 2
  center_y = VERTICAL_CELLS_COUNT // 2

  if level == 'normal':
    for i in range(15):
      walls.append(((center_x - i + 7)*CELL_SIZE, center_y*CELL_SIZE))
  elif level == 'high':
    for i in range(15):
      walls.append(((center_x - i + 7)*CELL_SIZE, center_y*CELL_SIZE))
    for i in range(7):
      walls.append(((center_x - 7)*CELL_SIZE, (center_y - i + 3)*CELL_SIZE))
      walls.append(((center_x + 7)*CELL_SIZE, (center_y - i + 3)*CELL_SIZE))
    for i in range(2):
      walls.append(((2 + i)*CELL_SIZE, 2*CELL_SIZE))
      walls.append(((2 + i)*CELL_SIZE, 3*CELL_SIZE))

      walls.append(((HORIZONTAL_CELLS_COUNT - 4 + i)*CELL_SIZE, (VERTICAL_CELLS_COUNT - 3)*CELL_SIZE))
      walls.append(((HORIZONTAL_CELLS_COUNT - 4 + i)*CELL_SIZE, (VERTICAL_CELLS_COUNT - 4)*CELL_SIZE))
  elif level == 'hard':
    for i in range(9):
      walls.append(((center_x - i + 4)*CELL_SIZE, center_y*CELL_SIZE))
    for i in range(9):
      walls.append(((center_x - 9)*CELL_SIZE, (center_y - i + 4)*CELL_SIZE))
      walls.append(((center_x - 4)*CELL_SIZE, (center_y - i + 4)*CELL_SIZE))
      walls.append(((center_x + 9)*CELL_SIZE, (center_y - i + 4)*CELL_SIZE))
      walls.append(((center_x + 4)*CELL_SIZE, (center_y - i + 4)*CELL_SIZE))
    for i in range(2):
      walls.append(((2 + i)*CELL_SIZE, 2*CELL_SIZE))
      walls.append(((2 + i)*CELL_SIZE, 3*CELL_SIZE))

      walls.append(((HORIZONTAL_CELLS_COUNT - 4 + i)*CELL_SIZE, 2*CELL_SIZE))
      walls.append(((HORIZONTAL_CELLS_COUNT - 4 + i)*CELL_SIZE, 3*CELL_SIZE))

      walls.append(((2 + i)*CELL_SIZE, (VERTICAL_CELLS_COUNT - 3)*CELL_SIZE))
      walls.append(((2 + i)*CELL_SIZE, (VERTICAL_CELLS_COUNT - 4)*CELL_SIZE))

      walls.append(((HORIZONTAL_CELLS_COUNT - 4 + i)*CELL_SIZE, (VERTICAL_CELLS_COUNT - 3)*CELL_SIZE))
      walls.append(((HORIZONTAL_CELLS_COUNT - 4 + i)*CELL_SIZE, (VERTICAL_CELLS_COUNT - 4)*CELL_SIZE))

  return walls
