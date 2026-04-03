"""Uinex Dialog Widget

A modal dialog box that overlays the screen and displays a title, message, and
configurable action buttons.

Features:
    - Semi-transparent overlay behind the dialog
    - Title and body text rendering
    - Configurable action buttons (OK, Cancel, Yes/No, etc.)
    - Blocks event propagation to widgets beneath while open
    - Callback for each button press

Usage example::

    def on_confirm(result):
        if result == "yes":
            print("User confirmed!")
        else:
            print("User cancelled.")

    dialog = Dialog(
        master=screen,
        title="Confirm",
        message="Are you sure you want to quit?",
        buttons=["Yes", "No"],
        on_close=on_confirm,
    )
    manager.register(dialog, layer=WidgetManager.OVERLAY_LAYER)
    dialog.show()

Author: Sackey Ezekiel Etrue (https://github.com/djoezeke) & Uinex Contributors
License: MIT
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import pygame

from uinex.theme.manager import ThemeManager
from uinex.widget.base import Widget

__all__ = ["Dialog"]

_DEFAULT_BUTTON_WIDTH = 90
_DEFAULT_BUTTON_HEIGHT = 34
_BUTTON_SPACING = 12


class Dialog(Widget):
    """A modal dialog widget.

    When visible, the dialog renders a translucent overlay over the entire
    master surface and a centred dialog box with a title, message, and action
    buttons.  All events that land *inside* the dialog box are consumed; events
    outside are also consumed while the dialog is open (modal behaviour).

    Args:
        master (pygame.Surface): The master surface (typically the display).
        title (str): Dialog title text.
        message (str): Body / message text.
        buttons (list[str]): Button labels (e.g. ``["OK"]``, ``["Yes", "No"]``).
            Defaults to ``["OK"]``.
        on_close (callable, optional): Called with the label of the pressed
            button (or ``None`` if closed otherwise).
        width (int): Dialog box width.  Defaults to 380.
        height (int): Dialog box height.  Defaults to 180.
        title_font (pygame.font.Font, optional): Font for the title.
        body_font (pygame.font.Font, optional): Font for the body text.
        **kwargs: Additional Widget options.

    Attributes:
        _title (str): Title text.
        _message (str): Body message text.
        _buttons (list[str]): Button labels.
        _on_close (callable): Close callback.
        _button_rects (list[pygame.Rect]): Hit areas for each button.
        _hovered_btn (int or None): Index of hovered button.
        _pressed_btn (int or None): Index of pressed button.
    """

    def __init__(
        self,
        master: Any | None = None,
        title: str = "Dialog",
        message: str = "",
        buttons: list[str] | None = None,
        on_close: Callable[[str | None], None] | None = None,
        width: int = 380,
        height: int = 180,
        title_font: pygame.font.Font | None = None,
        body_font: pygame.font.Font | None = None,
        **kwargs,
    ):
        super().__init__(master, width, height, **kwargs)

        _theme = ThemeManager.theme.get("Dialog", {})
        self._theme.setdefault("background", _theme.get("background", (40, 40, 56)))
        self._theme.setdefault("title_color", _theme.get("title_color", (220, 220, 220)))
        self._theme.setdefault("text_color", _theme.get("text_color", (180, 180, 200)))
        self._theme.setdefault("border_color", _theme.get("border_color", (100, 100, 120)))
        self._theme.setdefault("border_radius", _theme.get("border_radius", 10))
        self._theme.setdefault("borderwidth", _theme.get("borderwidth", 1))
        self._theme.setdefault("button_bg", (0, 120, 215))
        self._theme.setdefault("button_hover", (0, 90, 180))
        self._theme.setdefault("button_text", (255, 255, 255))

        _font_cfg = ThemeManager.theme.get("font", ThemeManager.theme.get("Font", {}))
        _family = _font_cfg.get("family", "Arial")
        _size = _font_cfg.get("size", 14)

        self._title: str = title
        self._message: str = message
        self._buttons: list[str] = buttons if buttons is not None else ["OK"]
        self._on_close: Callable[[str | None], None] | None = on_close

        self._title_font: pygame.font.Font = title_font or pygame.font.SysFont(_family, _size + 2, bold=True)
        self._body_font: pygame.font.Font = body_font or pygame.font.SysFont(_family, _size)

        self._button_rects: list[pygame.Rect] = []
        self._hovered_btn: int | None = None
        self._pressed_btn: int | None = None

        # Start hidden
        self._visible = False

    # ─────────────────────────────────────────────────
    # Public API
    # ─────────────────────────────────────────────────

    def show(self) -> None:
        """Show the dialog and centre it on the master surface."""
        self._visible = True
        if self._master is not None:
            mw = self._master.get_width()
            mh = self._master.get_height()
            self._rect.center = (mw // 2, mh // 2)
        self._rebuild_button_rects()

    def close(self, result: str | None = None) -> None:
        """Close the dialog and invoke the on_close callback.

        Args:
            result: The value to pass to the on_close callback.
        """
        self._visible = False
        if self._on_close is not None:
            self._on_close(result)

    # ─────────────────────────────────────────────────
    # Widget internals
    # ─────────────────────────────────────────────────

    def _rebuild_button_rects(self) -> None:
        """Recalculate button hit rects based on current dialog position."""
        n = len(self._buttons)
        total_w = n * _DEFAULT_BUTTON_WIDTH + (n - 1) * _BUTTON_SPACING
        start_x = self._rect.centerx - total_w // 2
        btn_y = self._rect.bottom - _DEFAULT_BUTTON_HEIGHT - 16

        self._button_rects = [
            pygame.Rect(
                start_x + i * (_DEFAULT_BUTTON_WIDTH + _BUTTON_SPACING),
                btn_y,
                _DEFAULT_BUTTON_WIDTH,
                _DEFAULT_BUTTON_HEIGHT,
            )
            for i in range(n)
        ]

    def _perform_draw_(self, surface: pygame.Surface, *args, **kwargs) -> None:
        # Semi-transparent overlay over the whole surface
        if self._master is not None:
            overlay = pygame.Surface(self._master.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            surface.blit(overlay, (0, 0))

        bg = self._theme["background"]
        border_col = self._theme["border_color"]
        r = self._theme["border_radius"]
        bw = self._theme["borderwidth"]
        title_col = self._theme["title_color"]
        text_col = self._theme["text_color"]

        # Draw dialog box
        pygame.draw.rect(surface, bg, self._rect, border_radius=r)
        if bw > 0:
            pygame.draw.rect(surface, border_col, self._rect, bw, border_radius=r)

        # Title
        title_surf = self._title_font.render(self._title, True, title_col)
        title_rect = title_surf.get_rect(centerx=self._rect.centerx, top=self._rect.top + 16)
        surface.blit(title_surf, title_rect)

        # Divider line under title
        dy = title_rect.bottom + 8
        pygame.draw.line(surface, border_col, (self._rect.left + 16, dy), (self._rect.right - 16, dy), 1)

        # Body message
        msg_surf = self._body_font.render(self._message, True, text_col)
        msg_rect = msg_surf.get_rect(centerx=self._rect.centerx, top=dy + 12)
        surface.blit(msg_surf, msg_rect)

        # Buttons
        for i, (label, btn_rect) in enumerate(zip(self._buttons, self._button_rects)):
            if i == self._hovered_btn:
                btn_bg = self._theme["button_hover"]
            else:
                btn_bg = self._theme["button_bg"]
            pygame.draw.rect(surface, btn_bg, btn_rect, border_radius=6)
            btn_text = self._body_font.render(label, True, self._theme["button_text"])
            btn_text_rect = btn_text.get_rect(center=btn_rect.center)
            surface.blit(btn_text, btn_text_rect)

    def _handle_event_(self, event: pygame.event.Event, *args, **kwargs) -> None:
        if event.type == pygame.MOUSEMOTION:
            self._hovered_btn = None
            for i, btn_rect in enumerate(self._button_rects):
                if btn_rect.collidepoint(event.pos):
                    self._hovered_btn = i
                    break

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, btn_rect in enumerate(self._button_rects):
                if btn_rect.collidepoint(event.pos):
                    self._pressed_btn = i
                    break

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self._pressed_btn is not None:
                btn_rect = self._button_rects[self._pressed_btn]
                if btn_rect.collidepoint(event.pos):
                    label = self._buttons[self._pressed_btn]
                    self._pressed_btn = None
                    self.close(label)
                    return
            self._pressed_btn = None

    def handle(self, event: pygame.event.Event, *args, **kwargs) -> bool:
        """Handle events. While visible, the dialog consumes ALL events (modal)."""
        if not self._visible:
            return False
        self._handle_event_(event, *args, **kwargs)
        # Modal: consume every event while open
        return True

    def _perform_update_(self, delta: float, *args, **kwargs) -> None:
        """Ensure button rects are updated if the dialog rect has moved."""
        if self._visible:
            self._rebuild_button_rects()
