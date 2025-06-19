"""PygameUI Frame Widget

This module defines the Frame widget for PygameUI, which acts as a container for grouping
other widgets. The Frame supports modern theming, rounded corners, borders, and background color.

Features:
    - Acts as a container for child widgets
    - Modern theming via ThemeManager
    - Rounded corners and border styling
    - Optional background and border color
    - Geometry management (pack, place, grid)

Usage Example:
    frame = Frame(master=screen, width=300, height=200)
    frame.place(x=50, y=50)
    ...
    frame.draw()
    ...

Author: Sackey Ezekiel Etrue & PygameUI Contributors
License: MIT
"""

from typing import Optional, Any

import pygame

from pygameui.core.widget import Widget
from pygameui.core.themes import ThemeManager


class Frame(Widget):
    """
    Frame widget for grouping other widgets.

    Args:
        master (Widget or pygame.Surface, optional): Parent widget or surface.
        width (int): Width of the frame.
        height (int): Height of the frame.
        background (pygame.Color, optional): Background color.
        bordercolor (pygame.Color, optional): Border color.
        borderwidth (int, optional): Border width.
        border_radius (int, optional): Border radius for rounded corners.
        **kwargs: Additional configuration options.

    Attributes:
        _background (pygame.Color): Frame background color.
        _bordercolor (pygame.Color): Frame border color.
        _borderwidth (int): Frame border width.
        _border_radius (int): Frame border radius.
    """

    def __init__(
        self,
        master: Optional[Any] = None,
        width: int = 200,
        height: int = 120,
        background: Optional[pygame.Color] = None,
        bordercolor: Optional[pygame.Color] = None,
        borderwidth: Optional[int] = None,
        border_radius: Optional[int] = None,
        **kwargs
    ):
        theme = ThemeManager.theme.get("Frame", {})
        self._background = pygame.Color(
            background if background is not None else theme.get("background", "#22304A")
        )
        self._bordercolor = pygame.Color(
            bordercolor
            if bordercolor is not None
            else theme.get("bordercolor", "#3A8DFF")
        )
        self._borderwidth = (
            borderwidth if borderwidth is not None else theme.get("borderwidth", 2)
        )
        self._border_radius = (
            border_radius
            if border_radius is not None
            else theme.get("border_radius", 10)
        )

        Widget.__init__(self, master, width, height, self._background, **kwargs)

    def _perform_draw_(self, surface: pygame.Surface, *args, **kwargs) -> None:
        """
        Draw the frame with a modern look.

        - Draws a rounded rectangle background
        - Draws a border if borderwidth > 0

        Args:
            surface (pygame.Surface): The surface to draw on.
        """
        rect = self._rect
        # Draw background
        # pygame.draw.rect(
        #     surface, self._background, rect, border_radius=self._border_radius
        # )
        # Draw border
        if self._borderwidth > 0:
            pygame.draw.rect(
                surface, self._bordercolor, rect, self._borderwidth, self._border_radius
            )

    def _handle_event_(self, event: pygame.event.Event, *args, **kwargs) -> None:
        """Frame does not handle events by default."""

    def _perform_update_(self, delta: float, *args, **kwargs) -> None:
        """Frame does not require updates by default."""
