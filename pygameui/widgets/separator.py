"""PygameUI Separator Widget

A Separator is a simple visual divider used to separate groups of widgets in a UI layout.
It can be horizontal or vertical, with customizable thickness, color, and padding.

Features:
    - Horizontal or vertical orientation
    - Customizable color, thickness, and padding
    - Integrates with layout managers

Example:
    sep = Separator(master, orientation="horizontal", color=(180,180,180), thickness=2)

Author: Your Name & PygameUI Contributors
License: MIT
"""

import pygame
from pygameui.core.widget import Widget

__all__ = ["Separator"]


class Separator(Widget):
    """
    A visual separator (horizontal or vertical line) for grouping widgets.

    Args:
        master (Widget or pygame.Surface): Parent widget or surface.
        orientation (str, optional): "horizontal" or "vertical". Default is "horizontal".
        color (pygame.Color or tuple, optional): Line color. Default is (180, 180, 180).
        thickness (int, optional): Line thickness in pixels. Default is 2.
        padding (int, optional): Space around the separator. Default is 4.
        length (int, optional): Length of the separator. If None, fills parent.
        **kwargs: Additional widget options.

    Attributes:
        orientation (str): "horizontal" or "vertical".
        color (pygame.Color): Line color.
        thickness (int): Line thickness.
        padding (int): Padding around the separator.
        length (int): Length of the separator.
    """

    def __init__(
        self,
        master,
        orientation="horizontal",
        color=(10, 10, 10),
        thickness=2,
        padding=40,
        length=None,
        **kwargs,
    ):
        self._orientation = orientation
        self._thickness = thickness
        self._padding = padding
        self._length = length

        if orientation == "horizontal":
            width = length if length is not None else 100
            height = thickness  # + 2 * padding
        else:
            width = thickness  # + 2 * padding
            height = length if length is not None else 100

        Widget.__init__(self, master, width, height, color, **kwargs)

    def _perform_draw_(self, surface, *args, **kwargs):
        """Draw the separator line."""
        if self._orientation == "horizontal":
            self._surface.fill(self._background)
            surface.blit(self._surface, self._rect)
        else:
            x = self._rect.centerx
            pygame.draw.line(
                surface,
                self._background,
                (x, self._padding),
                (x, self._rect.height - self._padding),
                self._thickness,
            )

    def _handle_event_(self, event, *args, **kwargs):
        """Separator does not handle events."""

    def _perform_update_(self, delta, *args, **kwargs):
        """Separator does not"""
