"""PygameUI Meter Widget

A Meter is a visual widget that displays a value as a filled bar or arc, commonly used for progress,
capacity, or gauge indicators. It supports horizontal, vertical, and circular styles, value bounds,
custom colors, and value display.

Features:
    - Horizontal, vertical, or circular meter styles
    - Customizable min, max, and current value
    - Customizable colors and thickness
    - Optional value display (numeric or percent)
    - Callback for value change
    - Mouse interaction (optional, for setting value)

Example:
    meter = Meter(master, min_value=0, max_value=100, value=50, style="horizontal")
    meter.set_value(75)

Author: Your Name & PygameUI Contributors
License: MIT
"""
import math
import pygame

from pygameui.core.widget import Widget
from pygameui.core.themes import ThemeManager

__all__ = ["Meter"]


class Meter(Widget):
    """
    A visual meter/progress/gauge widget.

    Args:
        master (Widget or pygame.Surface): Parent widget or surface.
        min_value (int or float, optional): Minimum value. Default is 0.
        max_value (int or float, optional): Maximum value. Default is 100.
        value (int or float, optional): Initial value. Default is 0.
        style (str, optional): "horizontal", "vertical", or "circular". Default is "horizontal".
        width (int, optional): Width of the meter. Default is 200.
        height (int, optional): Height of the meter. Default is 24.
        bar_color (pygame.Color or tuple, optional): Color of the filled bar. Default is (30, 144, 255).
        background (pygame.Color or tuple, optional): Background color. Default is (220, 220, 220).
        border_color (pygame.Color or tuple, optional): Border color. Default is (120, 120, 120).
        border_width (int, optional): Border thickness. Default is 2.
        show_value (bool, optional): Show value as text. Default is True.
        font (pygame.font.Font, optional): Font for value display.
        on_change (callable, optional): Callback when value changes.
        **kwargs: Additional widget options.

    Attributes:
        value (int or float): Current value.
        min_value (int or float): Minimum value.
        max_value (int or float): Maximum value.
        style (str): Meter style ("horizontal", "vertical", "circular").
        on_change (callable): Callback for value change.
    """

    def __init__(
        self,
        master,
        min_value=0,
        max_value=100,
        value=0,
        style="horizontal",
        width=200,
        height=24,
        bar_color=(30, 144, 255),
        background=(220, 220, 220),
        border_color=(120, 120, 120),
        border_width=2,
        show_value=True,
        font=None,
        on_change=None,
        **kwargs,
    ):
        self.min_value = min_value
        self.max_value = max_value
        self.value = value
        self.style = style
        self.bar_color = bar_color
        self.background = background
        self.border_color = border_color
        self.border_width = border_width
        self.show_value = show_value
        self.font = font or pygame.font.SysFont(None, 18)
        self.on_change = on_change

        if style == "circular":
            w = h = max(width, height)
        else:
            w, h = width, height

        super().__init__(
            master,
            width=w,
            height=h,
            background=background,
            **kwargs,
        )

    def _perform_draw_(self, surface, *args, **kwargs):
        """Draw the meter bar, border, and value text."""
        rect = surface.get_rect()
        # Draw background
        surface.fill(self.background)
        # Draw border
        if self.border_width > 0:
            pygame.draw.rect(surface, self.border_color, rect, self.border_width)

        percent = (self.value - self.min_value) / (self.max_value - self.min_value)
        percent = max(0.0, min(1.0, percent))

        if self.style == "horizontal":
            fill_rect = pygame.Rect(
                rect.left + self.border_width,
                rect.top + self.border_width,
                int((rect.width - 2 * self.border_width) * percent),
                rect.height - 2 * self.border_width,
            )
            pygame.draw.rect(surface, self.bar_color, fill_rect)
        elif self.style == "vertical":
            fill_height = int((rect.height - 2 * self.border_width) * percent)
            fill_rect = pygame.Rect(
                rect.left + self.border_width,
                rect.bottom - self.border_width - fill_height,
                rect.width - 2 * self.border_width,
                fill_height,
            )
            pygame.draw.rect(surface, self.bar_color, fill_rect)
        elif self.style == "circular":
            center = rect.center
            radius = min(rect.width, rect.height) // 2 - self.border_width
            start_angle = -90
            end_angle = start_angle + int(360 * percent)
            pygame.draw.circle(surface, self.background, center, radius)
            if percent > 0:
                # Draw arc as filled pie
                points = [center]
                for angle in range(start_angle, end_angle + 1, 2):
                    rad = angle * 3.14159 / 180
                    x = center[0] + int(radius * math.cos(rad))
                    y = center[1] + int(radius * math.sin(rad))
                    points.append((x, y))
                if len(points) > 2:
                    pygame.draw.polygon(surface, self.bar_color, points)
            pygame.draw.circle(
                surface, self.border_color, center, radius, self.border_width
            )

        # Draw value text
        if self.show_value:
            value_str = (
                f"{self.value}"
                if self.max_value - self.min_value > 1
                else f"{int(percent * 100)}%"
            )
            value_surf = self.font.render(value_str, True, (0, 0, 0))
            value_rect = value_surf.get_rect(center=rect.center)
            surface.blit(value_surf, value_rect)

    def _handle_event_(self, event, *args, **kwargs):
        """Handle mouse events for interactive value setting (optional)."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = (event.pos[0] - self._rect.x, event.pos[1] - self._rect.y)
            if self.style == "horizontal":
                percent = (mouse[0] - self.border_width) / (
                    self._rect.width - 2 * self.border_width
                )
            elif self.style == "vertical":
                percent = 1.0 - (mouse[1] - self.border_width) / (
                    self._rect.height - 2 * self.border_width
                )
            elif self.style == "circular":
                # Optional: implement circular click-to-set
                return
            else:
                return
            value = self.min_value + percent * (self.max_value - self.min_value)
            self.set_value(value)

    def _perform_update_(self, delta, *args, **kwargs):
        """Update logic for Meter (not used)."""
        pass

    def set_value(self, value):
        """Set the meter's value and trigger callback if changed."""
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
            if config == "style":
                return self.style
            return super().configure(config)
        if "value" in kwargs:
            self.set_value(kwargs["value"])
        if "min_value" in kwargs:
            self.min_value = kwargs["min_value"]
            self.set_value(self.value)
        if "max_value" in kwargs:
            self.max_value = kwargs["max_value"]
            self.set_value(self.value)
        if "style" in kwargs:
            self.style = kwargs["style"]
        return super().configure(**kwargs)
