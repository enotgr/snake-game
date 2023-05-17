from consts import SIZE, SWITCH_BUTTON
from .food import Food
from .sound import Sound

class Melon(Food):
  def __init__(self, points: int = 1, color: tuple[int, int, int] = None, sound: Sound = None):
    super().__init__(points, color)
    self._draw_counter: int = 0
    self._sound: Sound = sound

  def draw(self, surface):
    if self.position:
      super().draw(surface)
      self._draw_counter += 1

      if self._draw_counter >= SIZE // 10:
        self.remove()

  def remove(self):
    self.position = None
    self._draw_counter = 0

  def play_sound(self):
    self._sound.play_sound(SWITCH_BUTTON)
