import json
import os
import pathlib

from uinex.core.exceptions import ThemeError

# Sensible defaults used when no theme file has been loaded explicitly.
# Widget-specific overrides are layered on top of these in each widget's __init__.
_DEFAULT_THEME: dict = {
    "font": {
        "family": "Arial",
        "size": 14,
        "weight": "normal",
    },
    "Font": {
        "family": "Arial",
        "size": 14,
        "weight": "normal",
    },
    "Widget": {
        "background": (30, 30, 46),
        "border_color": (100, 100, 120),
    },
    "Button": {
        "background": (0, 120, 215),
        "text_color": (255, 255, 255),
        "hover_color": (0, 90, 180),
        "select_color": (0, 70, 140),
        "disable_color": (90, 90, 100),
        "border_color": (0, 90, 180),
        "border_radius": 6,
        "borderwidth": 0,
    },
    "Label": {
        "background": (30, 30, 46),
        "text_color": (220, 220, 220),
        "hover_text_color": (255, 255, 255),
        "disable_text_color": (140, 140, 150),
        "hover_color": (50, 50, 70),
        "border_color": (100, 100, 120),
        "border_radius": 4,
        "borderwidth": 0,
    },
    "Entry": {
        "normal": {
            "background": "#F7FAFC",
            "foreground": "#1A2332",
            "bordercolor": "#CBD5E0",
            "placeholder": "#A0AEC0",
            "border_radius": 6,
            "borderwidth": 2,
        },
        "focused": {
            "background": "#FFFFFF",
            "foreground": "#1A2332",
            "bordercolor": "#339CFF",
            "placeholder": "#A0AEC0",
            "border_radius": 6,
            "borderwidth": 2,
        },
        "hovered": {
            "background": "#EDF2F7",
            "foreground": "#1A2332",
            "bordercolor": "#90CDF4",
            "placeholder": "#A0AEC0",
            "border_radius": 6,
            "borderwidth": 2,
        },
        "disabled": {
            "background": "#E2E8F0",
            "foreground": "#A0AEC0",
            "bordercolor": "#CBD5E0",
            "placeholder": "#CBD5E0",
            "border_radius": 6,
            "borderwidth": 2,
        },
    },
    "Frame": {
        "background": (40, 40, 56),
        "border_color": (100, 100, 120),
        "border_radius": 8,
        "borderwidth": 0,
    },
    "Separator": {
        "color": (100, 100, 120),
        "thickness": 2,
    },
    "Scale": {
        "track_color": (80, 80, 100),
        "handle_color": (0, 120, 215),
        "handle_radius": 10,
        "fill_color": (0, 120, 215),
    },
    "Progressbar": {
        "background": (60, 60, 80),
        "fill_color": (0, 120, 215),
        "border_color": (100, 100, 120),
        "border_radius": 4,
        "borderwidth": 0,
    },
    "CheckButton": {
        "background": (30, 30, 46),
        "text_color": (220, 220, 220),
        "check_color": (0, 120, 215),
        "border_color": (100, 100, 120),
        "border_radius": 3,
    },
    "RadioButton": {
        "background": (30, 30, 46),
        "text_color": (220, 220, 220),
        "select_color": (0, 120, 215),
        "border_color": (100, 100, 120),
    },
    "Tooltip": {
        "background": (50, 50, 70),
        "text_color": (220, 220, 220),
        "border_color": (100, 100, 120),
        "border_radius": 4,
        "padding": 6,
    },
    "Dialog": {
        "background": (40, 40, 56),
        "title_color": (220, 220, 220),
        "text_color": (180, 180, 200),
        "border_color": (100, 100, 120),
        "border_radius": 10,
        "borderwidth": 1,
        "overlay_color": (0, 0, 0, 160),
    },
}


class ThemeManager:
    theme: dict = dict(_DEFAULT_THEME)  # pre-populated with defaults
    _built_in_themes: list[str] = ["blue"]
    _currently_loaded_theme: str | None = None

    @classmethod
    def load_theme(cls, theme_name_or_path: str):
        """Load a built-in or custom theme from a JSON file.

        The loaded values are merged *on top of* the defaults so that widgets
        always have sensible fallback values even for keys not present in the
        file.

        Args:
            theme_name_or_path: Name of a built-in theme (e.g. ``"blue"``) or
                an absolute/relative path to a JSON theme file.

        Raises:
            ThemeError: If the theme file cannot be found or parsed.
        """
        script_directory = os.path.dirname(os.path.abspath(__file__))

        try:
            if theme_name_or_path in cls._built_in_themes:
                uinex_path = pathlib.Path(script_directory).parent
                theme_path = os.path.join(uinex_path, "assets", "themes", f"{theme_name_or_path}.json")
                with open(theme_path) as f:
                    loaded = json.load(f)
            else:
                with open(theme_name_or_path) as f:
                    loaded = json.load(f)
        except FileNotFoundError as exc:
            raise ThemeError(f"Theme file not found: {theme_name_or_path!r}") from exc
        except json.JSONDecodeError as exc:
            raise ThemeError(f"Invalid JSON in theme file: {theme_name_or_path!r}") from exc

        # Deep merge: start fresh from defaults then apply file values
        merged = dict(_DEFAULT_THEME)
        for key, value in loaded.items():
            if isinstance(value, dict) and isinstance(merged.get(key), dict):
                merged[key] = {**merged[key], **value}
            else:
                merged[key] = value
        cls.theme = merged

        # store theme path for saving
        cls._currently_loaded_theme = theme_name_or_path

    @classmethod
    def save_theme(cls, path: str | None = None):
        """Save the current theme to a JSON file.

        Args:
            path: Destination file path.  If *None*, the originally loaded path
                is used.  Built-in themes cannot be overwritten.

        Raises:
            ThemeError: If no theme is loaded or the target is a built-in theme.
        """
        target = path or cls._currently_loaded_theme
        if target is None:
            raise ThemeError("Cannot save theme: no theme is loaded and no path provided.")
        if target in cls._built_in_themes:
            raise ThemeError(f"Cannot modify built-in theme '{target}'.")
        try:
            with open(target, "w") as f:
                json.dump(cls.theme, f, indent=4)
        except OSError as exc:
            raise ThemeError(f"Failed to write theme to '{target}': {exc}") from exc
