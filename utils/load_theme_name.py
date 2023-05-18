from services import file_service
from consts import THEMES, SAVED_THEME_PATH

def load_theme_name() -> str:
  theme_name: str = file_service.getTextFileByPath(SAVED_THEME_PATH)
  if theme_name:
    return theme_name
  return list(THEMES.keys())[0]