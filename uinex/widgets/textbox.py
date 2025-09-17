"""PygameUI TextBox Widget

A TextBox is a single-line or multi-line text input field for user text entry.
This widget supports keyboard input, cursor movement, selection, and basic editing.

Features:
    - Single-line or multi-line text input
    - Customizable font, colors, and padding
    - Cursor and selection support
    - Focus and blur handling
    - Optional input validation and max length
    - Callback for text change

Example:
    tb = TextBox(master, width=200, text="Hello", multiline=False)
    tb.on_change = lambda text: print("Text changed:", text)

Author: Your Name & PygameUI Contributors
License: MIT
"""

import pygame

from uinex.core.widget import Widget
from uinex.core.themes import ThemeManager

__all__ = ["TextBox"]


class TextBox(Widget):
    """
    A text input widget for single-line or multi-line text entry.

    Args:
        master (Widget or pygame.Surface): Parent widget or surface.
        width (int): Width of the textbox.
        height (int): Height of the textbox.
        text (str, optional): Initial text.
        font (pygame.font.Font, optional): Font for the text.
        foreground (pygame.Color, optional): Text color.
        background (pygame.Color, optional): Background color.
        border_color (pygame.Color, optional): Border color.
        border_width (int, optional): Border width.
        padding (int, optional): Padding inside the textbox.
        multiline (bool, optional): Enable multi-line input.
        max_length (int, optional): Maximum allowed text length.
        on_change (callable, optional): Callback when text changes.
        **kwargs: Additional widget options.

    Attributes:
        text (str): The current text.
        focused (bool): Whether the textbox is focused.
        cursor_pos (int): Cursor position in the text.
        selection (tuple): Selection start and end positions.
        on_change (callable): Callback for text change.
    """

    def __init__(
        self,
        master,
        width=150,
        height=28,
        text="",
        font=None,
        foreground=(0, 0, 0),
        background=(255, 255, 255),
        border_color=(120, 120, 120),
        border_width=1,
        padding=6,
        multiline=False,
        max_length=None,
        on_change=None,
        **kwargs,
    ):
        self.text = text
        self.font = font or pygame.font.SysFont(None, 20)
        self.foreground = foreground
        self.background = background
        self.border_color = border_color
        self.border_width = border_width
        self.padding = padding
        self.multiline = multiline
        self.max_length = max_length
        self.on_change = on_change

        self.focused = False
        self.cursor_pos = len(text)
        self.selection = None  # (start, end) or None
        self._cursor_visible = True
        self._cursor_timer = 0
        self._blink_interval = 500  # ms

        super().__init__(
            master,
            width=width,
            height=height,
            foreground=foreground,
            background=background,
            **kwargs,
        )

    def _perform_draw_(self, surface, *args, **kwargs):
        """Draw the textbox, border, text, and cursor."""
        # Draw background
        surface.fill(self.background)

        # Draw border
        if self.border_width > 0:
            pygame.draw.rect(
                surface,
                self.border_color,
                surface.get_rect(),
                self.border_width,
            )

        # Render text
        text_surf = self.font.render(self.text, True, self.foreground)
        text_rect = text_surf.get_rect()
        text_rect.topleft = (self.padding, (self._rect.height - text_rect.height) // 2)

        # Draw selection highlight if any
        if self.focused and self.selection and self.selection[0] != self.selection[1]:
            sel_start = min(self.selection)
            sel_end = max(self.selection)
            pre_text = self.text[:sel_start]
            sel_text = self.text[sel_start:sel_end]
            pre_width = self.font.size(pre_text)[0]
            sel_width = self.font.size(sel_text)[0]
            sel_rect = pygame.Rect(
                self.padding + pre_width,
                text_rect.top,
                sel_width,
                text_rect.height,
            )
            pygame.draw.rect(surface, (180, 210, 255), sel_rect)

        # Draw text
        surface.blit(text_surf, text_rect)

        # Draw cursor if focused
        if self.focused and self._cursor_visible:
            cursor_x = self.padding + self.font.size(self.text[: self.cursor_pos])[0]
            cursor_y = text_rect.top
            cursor_h = text_rect.height
            pygame.draw.line(
                surface,
                (0, 0, 0),
                (cursor_x, cursor_y),
                (cursor_x, cursor_y + cursor_h),
                1,
            )

    def _handle_event_(self, event, *args, **kwargs):
        """Handle keyboard and mouse events for text editing."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._rect.collidepoint(event.pos):
                self.focused = True
                # Set cursor position based on click
                rel_x = event.pos[0] - self._rect.x - self.padding
                self.cursor_pos = self._get_cursor_from_x(rel_x)
                self.selection = None
            else:
                self.focused = False
                self.selection = None

        if not self.focused:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if self.selection and self.selection[0] != self.selection[1]:
                    self._delete_selection()
                elif self.cursor_pos > 0:
                    self.text = (
                        self.text[: self.cursor_pos - 1] + self.text[self.cursor_pos :]
                    )
                    self.cursor_pos -= 1
                    self._trigger_on_change()
            elif event.key == pygame.K_DELETE:
                if self.selection and self.selection[0] != self.selection[1]:
                    self._delete_selection()
                elif self.cursor_pos < len(self.text):
                    self.text = (
                        self.text[: self.cursor_pos] + self.text[self.cursor_pos + 1 :]
                    )
                    self._trigger_on_change()
            elif event.key == pygame.K_LEFT:
                if self.cursor_pos > 0:
                    self.cursor_pos -= 1
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    if not self.selection:
                        self.selection = (self.cursor_pos + 1, self.cursor_pos)
                    else:
                        self.selection = (self.selection[0], self.cursor_pos)
                else:
                    self.selection = None
            elif event.key == pygame.K_RIGHT:
                if self.cursor_pos < len(self.text):
                    self.cursor_pos += 1
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    if not self.selection:
                        self.selection = (self.cursor_pos - 1, self.cursor_pos)
                    else:
                        self.selection = (self.selection[0], self.cursor_pos)
                else:
                    self.selection = None
            elif event.key == pygame.K_HOME:
                self.cursor_pos = 0
                self.selection = None
            elif event.key == pygame.K_END:
                self.cursor_pos = len(self.text)
                self.selection = None
            elif event.key == pygame.K_RETURN:
                if self.multiline:
                    self._insert_text("\n")
                # else: ignore in single-line
            elif event.unicode and (
                self.max_length is None or len(self.text) < self.max_length
            ):
                self._insert_text(event.unicode)
            self._dirty = True

    def _perform_update_(self, delta, *args, **kwargs):
        """Update cursor blink."""
        if self.focused:
            self._cursor_timer += delta * 1000  # delta in seconds
            if self._cursor_timer >= self._blink_interval:
                self._cursor_visible = not self._cursor_visible
                self._cursor_timer = 0
                self._dirty = True
        else:
            self._cursor_visible = False

    def _insert_text(self, s):
        """Insert text at cursor, replacing selection if any."""
        if self.selection and self.selection[0] != self.selection[1]:
            self._delete_selection()
        self.text = self.text[: self.cursor_pos] + s + self.text[self.cursor_pos :]
        self.cursor_pos += len(s)
        self.selection = None
        self._trigger_on_change()

    def _delete_selection(self):
        """Delete selected text."""
        start, end = sorted(self.selection)
        self.text = self.text[:start] + self.text[end:]
        self.cursor_pos = start
        self.selection = None
        self._trigger_on_change()

    def _get_cursor_from_x(self, x):
        """Get cursor position from x coordinate."""
        acc = 0
        for i, ch in enumerate(self.text):
            w = self.font.size(ch)[0]
            if acc + w // 2 > x:
                return i
            acc += w
        return len(self.text)

    def _trigger_on_change(self):
        """Call on_change callback if set."""
        if self.on_change:
            self.on_change(self.text)

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
            if config == "text":
                return self.text
            if config == "focused":
                return self.focused
            if config == "max_length":
                return self.max_length
            return super().configure(config)
        if "text" in kwargs:
            self.text = kwargs["text"]
            self.cursor_pos = min(self.cursor_pos, len(self.text))
            self._trigger_on_change()
        if "focused" in kwargs:
            self.focused = kwargs["focused"]
        if "max_length" in kwargs:
            self.max_length = kwargs["max_length"]
