"""PygameUI SizeGrip Widget

A SizeGrip is a small draggable handle, usually placed at the bottom-right corner of a window or frame,
allowing the user to resize the parent widget by dragging. It provides visual feedback and integrates
with mouse events for resizing.

Features:
    - Draggable resize handle for parent widget
    - Customizable size and color
    - Visual feedback on hover/drag
    - Integrates with layout managers

Example:
    grip = SizeGrip(master, size=16, color=(160, 160, 160))

Author: Your Name & PygameUI Contributors
License: MIT
"""

import pygame

from uinex.core.widget import Widget
from uinex.core.themes import ThemeManager

__all__ = ["SizeGrip"]


class SizeGrip(Widget):
    """
    A draggable size grip for resizing the parent widget.

    Args:
        master (Widget or pygame.Surface): Parent widget or surface.
        size (int, optional): Size (width and height) of the grip square. Default is 16.
        color (pygame.Color or tuple, optional): Grip color. Default is (160, 160, 160).
        hover_color (pygame.Color or tuple, optional): Color when hovered. Default is (120, 120, 120).
        **kwargs: Additional widget options.

    Attributes:
        dragging (bool): Whether the grip is being dragged.
        color (pygame.Color): Grip color.
        hover_color (pygame.Color): Color when hovered.
    """

    def __init__(
        self,
        master,
        size=16,
        color=(160, 160, 160),
        hover_color=(120, 120, 120),
        **kwargs,
    ):
        self.size = size
        self.color = color
        self.hover_color = hover_color
        self.dragging = False
        self._hovered = False
        self._drag_offset = (0, 0)
        super().__init__(
            master,
            width=size,
            height=size,
            background=(0, 0, 0, 0),  # Transparent background
            **kwargs,
        )

    def _perform_draw_(self, surface, *args, **kwargs):
        """Draw the size grip handle."""
        grip_color = self.hover_color if self._hovered or self.dragging else self.color
        rect = surface.get_rect()
        # Draw diagonal grip lines (classic style)
        for i in range(3, self.size, 4):
            pygame.draw.line(
                surface,
                grip_color,
                (rect.right - i, rect.bottom),
                (rect.right, rect.bottom - i),
                2,
            )
        # Optionally, draw a border for visibility
        pygame.draw.rect(surface, (100, 100, 100), rect, 1)

    def _handle_event_(self, event, *args, **kwargs):
        """Handle mouse events for resizing."""
        if event.type == pygame.MOUSEMOTION:
            mouse_pos = (event.pos[0] - self._rect.x, event.pos[1] - self._rect.y)
            self._hovered = self._rect.collidepoint(event.pos)
            if self.dragging:
                dx = event.rel[0]
                dy = event.rel[1]
                # Resize parent widget if possible
                if hasattr(self._master, "width") and hasattr(self._master, "height"):
                    new_width = max(self._master.width + dx, self.size)
                    new_height = max(self._master.height + dy, self.size)
                    self._master.width = new_width
                    self._master.height = new_height
                    # Optionally, update surface/rect if needed
                    if hasattr(self._master, "surface"):
                        self._master.surface = pygame.Surface(
                            (new_width, new_height), pygame.SRCALPHA
                        )
                        self._master.rect.size = (new_width, new_height)
                self._dirty = True
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._rect.collidepoint(event.pos):
                self.dragging = True
                pygame.mouse.get_rel()  # Reset relative mouse movement
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

    def _perform_update_(self, delta, *args, **kwargs):
        """Update logic for SizeGrip."""
