"""PygameUI Entry Widget

This module defines the Entry widget for PygameUI, providing a modern single-line
text input box with theming, cursor, focus, and keyboard input support.

Features:
    - Modern theming via ThemeManager
    - Rounded corners and border styling
    - Focus and hover effects
    - Text selection and cursor support
    - Optional placeholder text
    - Callback for text change

Usage Example:
    entry = Entry(master=screen, width=200, placeholder="Type here...")
    entry.place(x=100, y=200)
    ...
    entry.handel(event)
    entry.update()
    entry.draw()
    text = entry.get()
    ...

Author: Sackey Ezekiel Etrue & PygameUI Contributors
License: MIT
"""

from typing import Optional, Callable, Any

import pygame

from uinex.core.widget import Widget
from uinex.core.themes import ThemeManager
from uinex.core.mixins import HoverableMixin, ClickableMixin


class Entry(Widget, HoverableMixin, ClickableMixin):
    """
    Modern single-line text input widget.

    Args:
        master (Widget or pygame.Surface, optional): Parent widget or surface.
        width (int): Width of the entry box.
        height (int): Height of the entry box.
        font (pygame.Font, optional): Font for text.
        text (str): Initial text.
        placeholder (str): Placeholder text when empty.
        on_change (callable, optional): Callback for text change.
        disabled (bool): If True, disables input.
        **kwargs: Additional configuration options.

    Attributes:
        _text (str): Current text.
        _placeholder (str): Placeholder text.
        _font (pygame.Font): Font for rendering.
        _focused (bool): Whether the entry is focused.
        _disabled (bool): Whether the entry is disabled.
        _cursor_pos (int): Cursor position in text.
        _on_change (callable): Callback for text change.
        _blink (bool): Cursor blink state.
        _blink_timer (float): Timer for cursor blinking.
    """

    def __init__(
        self,
        master: Optional[Any] = None,
        width: int = 200,
        height: int = 36,
        font: Optional[pygame.font.Font] = None,
        text: str = "",
        placeholder: str = "",
        on_change: Optional[Callable[[str], None]] = None,
        disabled: bool = False,
        **kwargs
    ):
        self._text = text
        self._placeholder = placeholder
        self._on_change = on_change
        self._disabled = disabled
        self._focused = False
        self._cursor_pos = len(text)
        self._blink = True
        self._blink_timer = 0

        font_ = pygame.font.SysFont(
            ThemeManager.theme["font"]["family"], ThemeManager.theme["font"]["size"]
        )
        self._font = font or font_

        Widget.__init__(self, master, width, height, **kwargs)
        HoverableMixin.__init__(self)
        ClickableMixin.__init__(self)

    def get(self) -> str:
        """Return the current text."""
        return self._text

    def set(self, value: str):
        """Set the text value."""
        self._text = value
        self._cursor_pos = len(value)
        if self._on_change:
            self._on_change(self._text)

    def focus(self):
        """Set focus to this entry."""
        if not self._disabled:
            self._focused = True

    def blur(self):
        """Remove focus from this entry."""
        self._focused = False

    def is_focused(self) -> bool:
        """Return True if entry is focused."""
        return self._focused

    def disable(self):
        """Disable the entry (no input)."""
        self._disabled = True
        self.blur()

    def enable(self):
        """Enable the entry."""
        self._disabled = False

    def _perform_draw_(self, surface: pygame.Surface, *args, **kwargs) -> None:
        """
        Draw the entry widget with a modern look.

        - Draws a rounded rectangle background and border
        - Shows placeholder if empty and not focused
        - Draws text and blinking cursor if focused

        Args:
            surface (pygame.Surface): The surface to draw on.
        """
        theme = ThemeManager.theme.get("Entry", {})
        state = (
            "disabled"
            if self._disabled
            else "focused" if self._focused else "hovered" if self.hovered else "normal"
        )
        entry_theme = theme.get(state, theme.get("normal", {}))

        rect = self._rect
        border_radius = entry_theme.get("border_radius", 8)
        borderwidth = entry_theme.get("borderwidth", 2)
        bordercolor = pygame.Color(entry_theme.get("bordercolor", "#339CFF"))
        background = pygame.Color(entry_theme.get("background", "#F7FAFC"))
        text_color = pygame.Color(entry_theme.get("foreground", "#1A2332"))
        placeholder_color = pygame.Color(entry_theme.get("placeholder", "#A0AEC0"))

        # Draw background
        pygame.draw.rect(surface, background, rect, border_radius=border_radius)
        # Draw border
        pygame.draw.rect(surface, bordercolor, rect, borderwidth, border_radius)

        # Render text or placeholder
        if self._text or self._focused:
            txt = self._font.render(self._text, True, text_color)
        else:
            txt = self._font.render(self._placeholder, True, placeholder_color)
        txt_rect = txt.get_rect()
        txt_rect.midleft = (rect.left + 12, rect.centery)
        surface.blit(txt, txt_rect)

        # Draw blinking cursor if focused and not disabled
        if self._focused and not self._disabled:
            cursor_x = (
                txt_rect.left + self._font.size(self._text[: self._cursor_pos])[0]
            )
            cursor_y1 = rect.top + 8
            cursor_y2 = rect.bottom - 8
            if self._blink:
                pygame.draw.line(
                    surface, text_color, (cursor_x, cursor_y1), (cursor_x, cursor_y2), 2
                )

    def _handle_event_(self, event: pygame.event.Event, *args, **kwargs) -> None:
        """
        Handle events for the entry widget.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        self._check_hover(event)
        self._check_click(event)

        if self._disabled:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            self.focus()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.blur()

        if self._focused and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if self._cursor_pos > 0:
                    self._text = (
                        self._text[: self._cursor_pos - 1]
                        + self._text[self._cursor_pos :]
                    )
                    self._cursor_pos -= 1
            elif event.key == pygame.K_DELETE:
                if self._cursor_pos < len(self._text):
                    self._text = (
                        self._text[: self._cursor_pos]
                        + self._text[self._cursor_pos + 1 :]
                    )
            elif event.key == pygame.K_LEFT:
                if self._cursor_pos > 0:
                    self._cursor_pos -= 1
            elif event.key == pygame.K_RIGHT:
                if self._cursor_pos < len(self._text):
                    self._cursor_pos += 1
            elif event.key == pygame.K_HOME:
                self._cursor_pos = 0
            elif event.key == pygame.K_END:
                self._cursor_pos = len(self._text)
            elif event.unicode and event.key != pygame.K_RETURN:
                self._text = (
                    self._text[: self._cursor_pos]
                    + event.unicode
                    + self._text[self._cursor_pos :]
                )
                self._cursor_pos += 1
            if self._on_change:
                self._on_change(self._text)

    def _perform_update_(self, delta: float, *args, **kwargs) -> None:
        """
        Update the widget's logic (cursor blinking).

        Args:
            delta (float): Time since last update.
        """
        if self._focused:
            self._blink_timer += delta
            if self._blink_timer > 0.5:
                self._blink = not self._blink
                self._blink_timer = 0
        else:
            self._blink = False
            self._blink_timer = 0
