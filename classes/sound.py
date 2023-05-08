import pygame

from consts import BACKGROUND_TRACK

class Sound():
  def __init__(self, track_path: str = BACKGROUND_TRACK):
    self.is_sound: bool = True

    self._load_track(track_path)
    pygame.mixer.music.play(-1)

  def switch_sound(self):
    if self.is_sound:
      self.sound_off()
    else:
      self.sound_on()

  def change_music(self, track_path: str):
    self._load_track(track_path)
    if self.is_sound:
      self.sound_on()

  def play_sound(self, sound_path: str):
    if self.is_sound:
      sound: pygame.mixer.Sound = pygame.mixer.Sound(sound_path)
      sound.set_volume(0.2)
      sound.play()

  def sound_off(self):
    pygame.mixer.music.stop()
    self.is_sound = False

  def sound_on(self):
    pygame.mixer.music.play(-1)
    self.is_sound = True

  def _load_track(self, track_path: str):
    pygame.mixer.music.load(track_path)
    pygame.mixer.music.set_volume(0.3)