"""PygameUI Progressbar Widget

A Progressbar is a visual indicator of progress for a task, typically displayed as a horizontal or vertical bar
that fills as progress increases. It supports value bounds, orientation, colors, and optional value display.

Features:
    - Horizontal or vertical orientation
    - Customizable min, max, and current value
    - Customizable colors and border
    - Optional value display (numeric or percent)
    - Callback for value change

Example:
    pb = Progressbar(master, width=200, height=24, value=50, max_value=100)
    pb.set_value(75)

Author: Your Name & PygameUI Contributors
License: MIT
"""

import pygame

from pygameui.core.widget import Widget
from pygameui.core.themes import ThemeManager

__all__ = ["Progressbar"]


class Progressbar(Widget):
    """
    A visual progress bar widget.

    Args:
        master (Widget or pygame.Surface): Parent widget or surface.
        width (int, optional): Width of the progressbar. Default is 200.
        height (int, optional): Height of the progressbar. Default is 24.
        value (int or float, optional): Initial value. Default is 0.
        min_value (int or float, optional): Minimum value. Default is 0.
        max_value (int or float, optional): Maximum value. Default is 100.
        orientation (str, optional): "horizontal" or "vertical". Default is "horizontal".
        bar_color (pygame.Color or tuple, optional): Color of the filled bar. Default is (30, 144, 255).
        background (pygame.Color or tuple, optional): Background color. Default is (220, 220, 220).
        border_color (pygame.Color or tuple, optional): Border color. Default is (120, 120, 120).
        border_width (int, optional): Border thickness. Default is 2.
        show_value (bool, optional): Show value as text. Default is False.
        font (pygame.font.Font, optional): Font for value display.
        on_change (callable, optional): Callback when value changes.
        **kwargs: Additional widget options.

    Attributes:
        value (int or float): Current value.
        min_value (int or float): Minimum value.
        max_value (int or float): Maximum value.
        orientation (str): "horizontal" or "vertical".
        on_change (callable): Callback for value change.
    """

    def __init__(
        self,
        master,
        width=200,
        height=24,
        value=0,
        min_value=0,
        max_value=100,
        orientation="horizontal",
        bar_color=(30, 144, 255),
        background=(220, 220, 220),
        border_color=(120, 120, 120),
        border_width=2,
        show_value=False,
        font=None,
        on_change=None,
        **kwargs,
    ):
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.orientation = orientation
        self.bar_color = bar_color
        self.background = background
        self.border_color = border_color
        self.border_width = border_width
        self.show_value = show_value
        self.font = font or pygame.font.SysFont(None, 18)
        self.on_change = on_change

        super().__init__(
            master,
            width=width,
            height=height,
            background=background,
            **kwargs,
        )

    def _perform_draw_(self, surface, *args, **kwargs):
        """Draw the progress bar, border, and value text."""
        rect = surface.get_rect()
        # Draw background
        surface.fill(self.background)
        # Draw border
        if self.border_width > 0:
            pygame.draw.rect(surface, self.border_color, rect, self.border_width)

        percent = (self.value - self.min_value) / (self.max_value - self.min_value)
        percent = max(0.0, min(1.0, percent))

        if self.orientation == "horizontal":
            fill_rect = pygame.Rect(
                rect.left + self.border_width,
                rect.top + self.border_width,
                int((rect.width - 2 * self.border_width) * percent),
                rect.height - 2 * self.border_width,
            )
            pygame.draw.rect(surface, self.bar_color, fill_rect)
        else:
            fill_height = int((rect.height - 2 * self.border_width) * percent)
            fill_rect = pygame.Rect(
                rect.left + self.border_width,
                rect.bottom - self.border_width - fill_height,
                rect.width - 2 * self.border_width,
                fill_height,
            )
            pygame.draw.rect(surface, self.bar_color, fill_rect)

        # Draw value text
        if self.show_value:
            value_str = f"{int(percent * 100)}%"
            value_surf = self.font.render(value_str, True, (0, 0, 0))
            value_rect = value_surf.get_rect(center=rect.center)
            surface.blit(value_surf, value_rect)

    def _handle_event_(self, event, *args, **kwargs):
        """Progressbar does not handle events by default."""
        pass

    def _perform_update_(self, delta, *args, **kwargs):
        """Update logic for Progressbar (not used)."""
        pass

    def set_value(self, value):
        """Set the progressbar's value and trigger callback if changed."""
        value = min(max(value, self.min_value), self.max_value)
        if value != self.value:
            self.value = value
            if self.on_change:
                self.on_change(self.value)
            self._dirty = True

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
            if config == "min_value":
                return self.min_value
            if config == "max_value":
                return self.max_value
            if config == "orientation":
                return self.orientation
            return super().configure(config)
        if "value" in kwargs:
            self.set_value(kwargs["value"])
        if "min_value" in kwargs:
            self.min_value = kwargs["min_value"]
            self.set_value(self.value)
        if "max_value" in kwargs:
            self.max_value = kwargs["max_value"]
            self.set_value(self.value)
        if "orientation" in kwargs:
            self.orientation = kwargs["orientation"]
