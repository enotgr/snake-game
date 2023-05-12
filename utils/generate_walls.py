import random

from consts import GAME_SURFACE_HEIGHT, GAME_SURFACE_WIDTH, CELL_SIZE

CELLS_VERTICAL = GAME_SURFACE_HEIGHT // CELL_SIZE
CELLS_HORIZONTAL = GAME_SURFACE_WIDTH // CELL_SIZE

def generate_walls(wall_count: int = 10) -> list[tuple[int, int]]:
  walls = []
  for _ in range(wall_count):
    wall_x = random.randint(1, CELLS_HORIZONTAL - 2)
    wall_y = random.randint(1, CELLS_VERTICAL - 2)
    while (wall_x, wall_y) in walls:
      wall_x = random.randint(1, CELLS_HORIZONTAL - 2)
      wall_y = random.randint(1, CELLS_VERTICAL - 2)
    walls.append((wall_x*CELL_SIZE, wall_y*CELL_SIZE))
  return walls
