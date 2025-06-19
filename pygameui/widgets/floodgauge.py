"""PygameUI Floodgauge Widget

A Floodgauge is a modern progress indicator that visually fills as progress increases.
It supports theming, rounded corners, smooth animation, and optional text display.

Features:
    - Modern theming via ThemeManager
    - Rounded corners and accent color
    - Smooth fill animation
    - Optional percentage or custom text display
    - Value range and step control

Example:
    flood = Floodgauge(master=screen, width=200, height=24, max_value=100)
    flood.set(50)
    flood.draw()

Author: Sackey Ezekiel Etrue & PygameUI Contributors
License: MIT
"""

from typing import Optional, Any

import pygame

from pygameui.core.widget import Widget
from pygameui.core.themes import ThemeManager


class Floodgauge(Widget):
    """
    Modern Floodgauge/progress bar widget.

    Args:
        master (Widget or pygame.Surface, optional): Parent widget or surface.
        width (int): Width of the floodgauge.
        height (int): Height of the floodgauge.
        max_value (int or float): Maximum value.
        value (int or float): Initial value.
        show_text (bool): Whether to display percentage text.
        font (pygame.Font, optional): Font for text.
        bar_color (pygame.Color or tuple, optional): Fill color for the bar.
        background (pygame.Color or tuple, optional): Background color.
        border_color (pygame.Color or tuple, optional): Border color.
        border_radius (int, optional): Corner radius.
        borderwidth (int, optional): Border thickness.
        foreground (pygame.Color or tuple, optional): Text color.
        on_change (callable, optional): Callback when value changes.
        **kwargs: Additional configuration options.

    Attributes:
        value (float): Current value.
        max_value (float): Maximum value.
        show_text (bool): Whether to show text.
        font (pygame.Font): Font for text.
        on_change (callable): Callback for value change.
    """

    def __init__(
        self,
        master: Optional[Any] = None,
        width: int = 200,
        height: int = 24,
        max_value: float = 100,
        value: float = 0,
        show_text: bool = True,
        font: Optional[pygame.font.Font] = None,
        bar_color: Optional[Any] = None,
        background: Optional[Any] = None,
        border_color: Optional[Any] = None,
        border_radius: Optional[int] = None,
        borderwidth: Optional[int] = None,
        foreground: Optional[Any] = None,
        on_change: Optional[callable] = None,
        **kwargs,
    ):
        self.max_value = max(1, float(max_value))
        self.value = max(0, min(float(value), self.max_value))
        self.show_text = show_text
        self.on_change = on_change

        # Theme defaults
        theme = ThemeManager.theme.get("Floodguage", {})
        self.bar_color = pygame.Color(bar_color or theme.get("fill", "#3A8DFF"))
        self.background = pygame.Color(background or theme.get("background", "#22304A"))
        self.border_color = pygame.Color(
            border_color or theme.get("bordercolor", "#339CFF")
        )
        self.border_radius = (
            border_radius
            if border_radius is not None
            else theme.get("border_radius", 12)
        )
        self.borderwidth = (
            borderwidth if borderwidth is not None else theme.get("borderwidth", 0)
        )
        self.foreground = pygame.Color(foreground or theme.get("foreground", "#F5F7FA"))

        self.font = font or pygame.font.SysFont(
            ThemeManager.theme.get("font", {}).get("family", "Segoe UI"),
            ThemeManager.theme.get("font", {}).get("size", 18),
        )

        super().__init__(
            master,
            width=width,
            height=height,
            background=self.background,
            foreground=self.foreground,
            **kwargs,
        )

    def set(self, value: float):
        """Set the current value (clamped to [0, max_value])."""
        value = max(0, min(float(value), self.max_value))
        if value != self.value:
            self.value = value
            if self.on_change:
                self.on_change(self.value)
            self._dirty = True

    def get(self) -> float:
        """Get the current value."""
        return self.value

    def set_max(self, max_value: float):
        """Set the maximum value."""
        self.max_value = max(1, float(max_value))
        self.value = min(self.value, self.max_value)
        self._dirty = True

    def _perform_draw_(self, surface: pygame.Surface, *args, **kwargs) -> None:
        """
        Draw the floodgauge with a modern look.

        - Draws a rounded background bar
        - Draws a filled accent bar for progress
        - Optionally displays percentage or value text

        Args:
            surface (pygame.Surface): The surface to draw on.
        """
        rect = self._rect
        percent = self.value / self.max_value if self.max_value else 0
        fill_width = int(rect.width * percent)

        # Draw background bar
        pygame.draw.rect(
            surface, self.background, rect, border_radius=self.border_radius
        )
        # Draw border if needed
        if self.borderwidth > 0:
            pygame.draw.rect(
                surface, self.border_color, rect, self.borderwidth, self.border_radius
            )

        # Draw filled bar
        fill_rect = pygame.Rect(rect.left, rect.top, fill_width, rect.height)
        if fill_width > 0:
            pygame.draw.rect(
                surface, self.bar_color, fill_rect, border_radius=self.border_radius
            )

        # Draw text (percentage) if enabled
        if self.show_text:
            percent_val = int(percent * 100)
            text = f"{percent_val}%"
            txt_surf = self.font.render(text, True, self.foreground)
            txt_rect = txt_surf.get_rect(center=rect.center)
            surface.blit(txt_surf, txt_rect)

    def _handle_event_(self, event: pygame.event.Event, *args, **kwargs) -> None:
        """Floodgauge does not handle events."""
        pass

    def _perform_update_(self, delta: float, *args, **kwargs) -> None:
        """Floodgauge does not update state."""
        pass

    def configure(self, config=None, **kwargs):
        """
        Get or set configuration options.

        Args:
            config (str, optional): Name of config to get.
            **kwargs: Configs to set.

        Returns:
            Any: Value of config if requested.
        """
        if config is not None:
            if config == "value":
                return self.value
            if config == "max_value":
                return self.max_value
            if config == "show_text":
                return self.show_text
            return super().configure(config)
        if "value" in kwargs:
            self.set(kwargs["value"])
        if "max_value" in kwargs:
            self.set_max(kwargs["max_value"])
        if "show_text" in kwargs:
            self.show_text = kwargs["show_text"]
            self._dirty = True
        return super().configure(**kwargs)
