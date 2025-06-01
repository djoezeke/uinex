"""PygameUI Widgets Themes Manager"""

import os
import pathlib
import json
from typing import List, Union


class ThemeManager:
    """ThemeManager"""

    theme: dict = {}  # contains all the theme data
    _built_in_themes: List[str] = ["light-blue", "dark-blue"]
    _currently_loaded_theme: Union[str, None] = None

    @property
    def button(self) -> dict:
        """font"""
        return ThemeManager.theme["button"]

    @classmethod
    def load_theme(cls, theme_name_or_path: str):
        """load_theme"""
        script_directory = os.path.dirname(os.path.abspath(__file__))

        if theme_name_or_path in cls._built_in_themes:
            pygameui_path = pathlib.Path(script_directory).parent.parent
            theme_path = os.path.join(
                pygameui_path, "assets", "themes", f"{theme_name_or_path}.json"
            )
            with open(theme_path, "r", encoding="utf-8") as f:
                cls.theme = json.load(f)
        else:
            with open(theme_name_or_path, "r", encoding="utf-8") as f:
                cls.theme = json.load(f)

        # store theme path for saving
        cls._currently_loaded_theme = theme_name_or_path

    @classmethod
    def save_theme(cls):
        """save_theme"""
        if cls._currently_loaded_theme is not None:
            if cls._currently_loaded_theme not in cls._built_in_themes:
                with open(cls._currently_loaded_theme, "r", encoding="utf-8") as f:
                    json.dump(cls.theme, f, indent=2)
            else:
                raise ValueError(
                    f"cannot modify builtin theme '{cls._currently_loaded_theme}'"
                )
        else:
            raise ValueError("cannot save theme, no theme is loaded")
