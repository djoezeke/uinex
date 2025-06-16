"""PygameUI Widgets Themes & Manager."""

from .theme import ThemeManager

# from .style import Style

# load default light blue theme
try:
    ThemeManager.load_theme("dark-blue")
except FileNotFoundError as err:
    raise FileNotFoundError(
        f"{err}\nThe theme file for PygameUI could not be found.\n"
    ) from err
