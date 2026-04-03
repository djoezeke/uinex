"""Uinex Widget Mixins

Reusable mixin classes that provide common interaction behaviours for widgets.

Available Mixins:
    - HoverableMixin  – tracks mouse-hover state
    - ClickableMixin  – tracks single-click state and calls a bound command
    - DoubleClickMixin – tracks double-click state

Author: Sackey Ezekiel Etrue (https://github.com/djoezeke) & Uinex Contributors
License: MIT
"""

import time

import pygame

__all__ = ["HoverableMixin", "ClickableMixin", "DoubleClickMixin"]

# ──────────────────────────────────────────────────────────────────────────────
# HoverableMixin
# ──────────────────────────────────────────────────────────────────────────────


class HoverableMixin:
    """Mixin that adds mouse-hover detection to a widget.

    Requires the widget to have a ``_rect`` attribute (``pygame.Rect``).

    Attributes:
        _hover (bool): True while the mouse cursor is over the widget.
    """

    def __init__(self):
        self._hover: bool = False

    # region Properties

    @property
    def hovered(self) -> bool:
        """Return ``True`` if the mouse cursor is currently over the widget."""
        return self._hover

    # endregion

    # region Helpers

    def _check_hover(self, event: pygame.event.Event) -> bool:
        """Update hover state from a MOUSEMOTION or MOUSEBUTTONDOWN event.

        Args:
            event: A pygame event.

        Returns:
            ``True`` if the widget is currently hovered.
        """
        mouse_pos = pygame.mouse.get_pos()
        self._hover = self._rect.collidepoint(mouse_pos)
        return self._hover

    # endregion


# ──────────────────────────────────────────────────────────────────────────────
# ClickableMixin
# ──────────────────────────────────────────────────────────────────────────────


class ClickableMixin:
    """Mixin that adds left-click detection to a widget.

    Requires the widget to have a ``_rect`` attribute (``pygame.Rect``).

    Attributes:
        _clicked (bool): True on the frame the widget is clicked.
    """

    def __init__(self):
        self._clicked: bool = False

    # region Properties

    @property
    def clicked(self) -> bool:
        """Return ``True`` if the widget was clicked this frame."""
        return self._clicked

    # endregion

    # region Helpers

    def _check_click(self, event: pygame.event.Event) -> bool:
        """Update clicked state from MOUSEBUTTONDOWN / MOUSEBUTTONUP events.

        Args:
            event: A pygame event.

        Returns:
            ``True`` if the widget was clicked (MOUSEBUTTONDOWN inside rect).
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self._clicked = self._rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            self._clicked = False
        return self._clicked

    # endregion


# ──────────────────────────────────────────────────────────────────────────────
# DoubleClickMixin
# ──────────────────────────────────────────────────────────────────────────────


class DoubleClickMixin:
    """Mixin that adds double-click detection to a widget.

    Requires the widget to have a ``_rect`` attribute (``pygame.Rect``).

    Attributes:
        _double_clicked (bool): True on the frame a double-click is detected.
        _double_click_threshold (float): Maximum time (seconds) between clicks.
    """

    _DOUBLE_CLICK_THRESHOLD: float = 0.35

    def __init__(self):
        self._double_clicked: bool = False
        self._last_click_time: float = 0.0
        self._double_click_threshold: float = self._DOUBLE_CLICK_THRESHOLD

    # region Properties

    @property
    def doubleclicked(self) -> bool:
        """Return ``True`` if the widget was double-clicked this frame."""
        return self._double_clicked

    # endregion

    # region Helpers

    def _check_double(self, event: pygame.event.Event) -> bool:
        """Update double-click state from MOUSEBUTTONDOWN events.

        Args:
            event: A pygame event.

        Returns:
            ``True`` if a double-click was detected.
        """
        self._double_clicked = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._rect.collidepoint(event.pos):
                now = time.time()
                if now - self._last_click_time <= self._double_click_threshold:
                    self._double_clicked = True
                self._last_click_time = now
        return self._double_clicked

    # endregion
