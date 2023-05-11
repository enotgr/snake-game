import pygame

from consts import THEMES

def get_heart(theme_name: str) -> pygame.Surface:
  heart_surface = pygame.Surface((28, 26), pygame.SRCALPHA)

  heart_pixels = [
      "    ######        ######    ",
      "    ######        ######    ",
      "  ##******##    ##******##  ",
      "  ##******##    ##******##  ",
      "##**********####****  ****##",
      "##**********####****  ****##",
      "##********************  **##",
      "##********************  **##",
      "##************************##",
      "##************************##",
      "##************************##",
      "##************************##",
      "  ##********************##  ",
      "  ##********************##  ",
      "    ##****************##    ",
      "    ##****************##    ",
      "      ##************##      ",
      "      ##************##      ",
      "        ##********##        ",
      "        ##********##        ",
      "          ##****##          ",
      "          ##****##          ",
      "            ####            ",
      "            ####            "
  ]

  for y, row in enumerate(heart_pixels):
      for x, char in enumerate(row):
          if char == "*":
              heart_surface.set_at((x, y), THEMES[theme_name]['APPLE_COLOR'])
          if char == "#":
            heart_surface.set_at((x, y), THEMES[theme_name]['TEXT_COLOR'])
  return heart_surface
