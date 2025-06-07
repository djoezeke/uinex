"""PygameUI ThemeManager

Defines a modern, consistent theme for all widgets in PygameUI.
You can customize colors, fonts, and widget-specific styles here.
"""

import os
import pathlib
import json
from typing import List, Union


class ThemeManager:
    """
    Central theme manager for PygameUI widgets.
    Provides default colors, fonts, and per-widget style dictionaries.
    """

    theme = {
        "font": {
            "family": "Segoe UI",
            "size": 18,
            "bold": False,
        },
        "colors": {
            "background": "#22304A",
            "foreground": "#F5F7FA",
            "accent": "#3A8DFF",
            "accent2": "#339CFF",
            "border": "#2C3E50",
            "select": "#2C82C9",
            "frame_bg": "#28365A",
            "disabled": "#787878",
            "error": "#FF4D4F",
        },
        "Label": {
            "foreground": "#F5F7FA",
            "background": "#22304A",
        },
        "Button": {
            "foreground": "#F5F7FA",
            "background": "#3A8DFF",
            "hover": "#339CFF",
            "active": "#2C82C9",
            "border_radius": 8,
            "bordercolor": "#339CFF",
            "borderwidth": 0,
        },
        "Entry": {
            "foreground": "#F5F7FA",
            "background": "#28365A",
            "bordercolor": "#339CFF",
            "border_radius": 8,
            "borderwidth": 2,
        },
        "CheckButton": {
            "foreground": "#F5F7FA",
            "background": "#22304A",
            "check_color": "#3A8DFF",
            "bordercolor": "#339CFF",
        },
        "RadioButton": {
            "foreground": "#F5F7FA",
            "background": "#22304A",
            "circle_color": "#339CFF",
            "check_color": "#3A8DFF",
        },
        "MenuButton": {
            "foreground": "#F5F7FA",
            "background": "#28365A",
            "menu_background": "#22304A",
            "menu_foreground": "#F5F7FA",
            "hover": "#2C82C9",
        },
        "ComboBox": {
            "foreground": "#F5F7FA",
            "background": "#28365A",
            "select_color": "#2C82C9",
            "bordercolor": "#339CFF",
        },
        "TextBox": {
            "foreground": "#F5F7FA",
            "background": "#28365A",
            "bordercolor": "#339CFF",
            "border_radius": 8,
            "borderwidth": 2,
        },
        "SpinBox": {
            "foreground": "#F5F7FA",
            "background": "#28365A",
            "button_color": "#339CFF",
            "bordercolor": "#339CFF",
        },
        "ListBox": {
            "foreground": "#F5F7FA",
            "background": "#28365A",
            "select_color": "#2C82C9",
            "bordercolor": "#339CFF",
        },
        "Progressbar": {
            "bar_color": "#3A8DFF",
            "background": "#22304A",
            "border_color": "#339CFF",
            "border_width": 2,
            "show_value": True,
        },
        "Floodguage": {
            "fill": "#3A8DFF",
            "background": "#28365A",
            "bordercolor": "#339CFF",
            "border_radius": 14,
            "borderwidth": 0,
            "foreground": "#F5F7FA",
        },
        "Separator": {
            "color": "#339CFF",
            "thickness": 3,
            "padding": 4,
        },
        "Meter": {
            "bar_color": "#3A8DFF",
            "background": "#28365A",
            "border_color": "#339CFF",
            "border_width": 2,
            "show_value": True,
        },
        "Scale": {
            "track_color": "#339CFF",
            "handle_color": "#3A8DFF",
            "handle_radius": 12,
            "show_value": True,
        },
        "SizeGrip": {
            "color": "#339CFF",
            "hover_color": "#3A8DFF",
        },
        "TreeView": {
            "foreground": "#F5F7FA",
            "background": "#28365A",
            "select_color": "#2C82C9",
            "bordercolor": "#339CFF",
        },
        "Frame": {
            "background": "#28365A",
            "bordercolor": "#339CFF",
        },
    }

    _built_in_themes: List[str] = ["light-blue", "dark-blue"]
    _currently_loaded_theme: Union[str, None] = None

    @property
    def button(self) -> dict:
        """Get the button theme."""
        return ThemeManager.theme["button"]

    @property
    def themename(self) -> dict:
        """Get the Name of Current theme."""
        return ThemeManager._currently_loaded_theme

    @classmethod
    def load_theme(cls, theme_name_or_path: str):
        """Load a theme by name or path."""
        script_directory = os.path.dirname(os.path.abspath(__file__))

        if theme_name_or_path in cls._built_in_themes:
            pygameui_path = pathlib.Path(script_directory).parent
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
        """Save the currently loaded theme."""
        if cls._currently_loaded_theme is not None:
            if cls._currently_loaded_theme not in cls._built_in_themes:
                with open(cls._currently_loaded_theme, "w", encoding="utf-8") as f:
                    json.dump(cls.theme, f, indent=2)
            else:
                raise ValueError(
                    f"cannot modify builtin theme '{cls._currently_loaded_theme}'"
                )
        else:
            raise ValueError("cannot save theme, no theme is loaded")
