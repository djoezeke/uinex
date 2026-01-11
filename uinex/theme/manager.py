import json
import os
import pathlib


class ThemeManager:
    theme: dict = {}  # contains all the theme data
    _built_in_themes: list[str] = ["blue"]
    _currently_loaded_theme: str | None = None

    @classmethod
    def load_theme(cls, theme_name_or_path: str):
        script_directory = os.path.dirname(os.path.abspath(__file__))

        if theme_name_or_path in cls._built_in_themes:
            uinex_path = pathlib.Path(script_directory).parent
            with open(os.path.join(uinex_path, "assets", "themes", f"{theme_name_or_path}.json")) as f:
                cls.theme = json.load(f)
        else:
            with open(theme_name_or_path) as f:
                cls.theme = json.load(f)

        # store theme path for saving
        cls._currently_loaded_theme = theme_name_or_path

    @classmethod
    def save_theme(cls):
        if cls._currently_loaded_theme is not None:
            if cls._currently_loaded_theme not in cls._built_in_themes:
                with open(cls._currently_loaded_theme) as f:
                    json.dump(cls.theme, f)
            else:
                raise ValueError(f"Cannot modify builtin theme '{cls._currently_loaded_theme}'")
        else:
            raise ValueError("Cannot save theme, no theme is loaded")
