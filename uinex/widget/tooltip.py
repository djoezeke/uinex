"""Uinex Tooltip Widget

A Tooltip is a small informational popup that appears near the cursor (or a
target widget) after a short hover delay.

Features:
    - Appears after a configurable hover delay
    - Auto-positioned to stay within the display surface
    - Customisable background, text colour, border, and padding
    - Follows a target widget or a fixed position

Usage example::

    tooltip = Tooltip(master=screen, text="This is a button", target=button)
    # Register tooltip with the WidgetManager on OVERLAY_LAYER so it draws
    # on top of everything.
    manager.register(tooltip, layer=WidgetManager.OVERLAY_LAYER)

Author: Sackey Ezekiel Etrue (https://github.com/djoezeke) & Uinex Contributors
License: MIT
"""

from typing import Any

import pygame

from uinex.theme.manager import ThemeManager
from uinex.widget.base import Widget

__all__ = ["Tooltip"]


class Tooltip(Widget):
    """A small floating label shown on hover over a target widget.

    Args:
        master (pygame.Surface): The master surface to render on.
        text (str): Tooltip text.
        target (Widget, optional): Widget that triggers the tooltip.
        delay (float): Hover delay in seconds before showing. Default 0.5.
        padding (int): Inner padding in pixels. Default 6.
        font (pygame.font.Font, optional): Font for tooltip text.
        background (tuple, optional): Background colour.
        text_color (tuple, optional): Text colour.
        border_color (tuple, optional): Border colour.
        border_radius (int): Corner radius. Default 4.
        **kwargs: Additional Widget options.

    Attributes:
        _text (str): The tooltip text.
        _target (Widget): The trigger widget.
        _delay (float): Hover delay in seconds.
        _hover_timer (float): Accumulated hover time.
        _visible (bool): Whether the tooltip is currently shown.
    """

    def __init__(
        self,
        master: Any | None = None,
        text: str = "",
        target: Widget | None = None,
        delay: float = 0.5,
        padding: int = 6,
        font: pygame.font.Font | None = None,
        background: tuple | None = None,
        text_color: tuple | None = None,
        border_color: tuple | None = None,
        border_radius: int = 4,
        **kwargs,
    ):
        # Determine size from text before calling super().__init__
        _font_cfg = ThemeManager.theme.get("font", ThemeManager.theme.get("Font", {}))
        self._font: pygame.font.Font = font or pygame.font.SysFont(
            _font_cfg.get("family", "Arial"), _font_cfg.get("size", 13)
        )
        text_surface = self._font.render(text or " ", True, (255, 255, 255))
        w = text_surface.get_width() + padding * 2
        h = text_surface.get_height() + padding * 2

        super().__init__(master, width=w, height=h, border_radius=border_radius, **kwargs)

        _theme = ThemeManager.theme.get("Tooltip", {})
        self._theme.setdefault("background", _theme.get("background", (50, 50, 70)))
        self._theme.setdefault("text_color", _theme.get("text_color", (220, 220, 220)))
        self._theme.setdefault("border_color", _theme.get("border_color", (100, 100, 120)))

        if background is not None:
            self._theme["background"] = background
        if text_color is not None:
            self._theme["text_color"] = text_color
        if border_color is not None:
            self._theme["border_color"] = border_color

        self._text: str = text
        self._target: Widget | None = target
        self._delay: float = delay
        self._padding: int = padding
        self._hover_timer: float = 0.0
        self._visible: bool = False

    # ─────────────────────────────────────────────────
    # Public API
    # ─────────────────────────────────────────────────

    def set_text(self, text: str) -> None:
        """Update the tooltip text.

        Args:
            text: New tooltip text.
        """
        self._text = text
        # Recalculate size
        text_surface = self._font.render(text or " ", True, (255, 255, 255))
        self._width = text_surface.get_width() + self._padding * 2
        self._height = text_surface.get_height() + self._padding * 2
        self._surface = pygame.Surface((self._width, self._height), pygame.SRCALPHA, 32)
        self._rect = self._surface.get_rect(topleft=self._rect.topleft)

    def attach(self, target: Widget) -> None:
        """Attach the tooltip to a new target widget.

        Args:
            target: The widget that triggers this tooltip.
        """
        self._target = target
        self._hover_timer = 0.0
        self._visible = False

    # ─────────────────────────────────────────────────
    # Widget internals
    # ─────────────────────────────────────────────────

    def _perform_draw_(self, surface: pygame.Surface, *args, **kwargs) -> None:
        bg = self._theme["background"]
        tc = self._theme["text_color"]
        bc = self._theme["border_color"]
        r = self._border_radius

        pygame.draw.rect(surface, bg, self._rect, border_radius=r)
        pygame.draw.rect(surface, bc, self._rect, 1, border_radius=r)

        text_surf = self._font.render(self._text, True, tc)
        text_rect = text_surf.get_rect()
        text_rect.topleft = (self._rect.left + self._padding, self._rect.top + self._padding)
        surface.blit(text_surf, text_rect)

    def _handle_event_(self, event: pygame.event.Event, *args, **kwargs) -> None:
        """Tooltip is passive – it does not consume events."""

    def _perform_update_(self, delta: float, *args, **kwargs) -> None:
        """Track hover over the target widget and toggle visibility."""
        if self._target is None:
            return

        mouse_pos = pygame.mouse.get_pos()
        if self._target._rect.collidepoint(mouse_pos):
            self._hover_timer += delta
            if self._hover_timer >= self._delay:
                self._visible = True
                # Position tooltip near cursor, clamped within master surface
                mx, my = mouse_pos
                self._rect.topleft = (mx + 14, my + 10)
                if self._master is not None:
                    mw = self._master.get_width()
                    mh = self._master.get_height()
                    if self._rect.right > mw:
                        self._rect.right = mw - 2
                    if self._rect.bottom > mh:
                        self._rect.bottom = my - 2
        else:
            self._hover_timer = 0.0
            self._visible = False
