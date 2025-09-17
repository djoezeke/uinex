"""PygameUI SpinBox Widget

A SpinBox is a widget that allows the user to select a numeric value by either typing it
or using increment/decrement buttons. It supports value bounds, step size, and callbacks
for value changes.

Features:
    - Integer or float value support
    - Customizable min, max, and step
    - Optional editable text field
    - Increment and decrement buttons
    - Callback for value change
    - Keyboard and mouse interaction

Example:
    sb = SpinBox(master, min_value=0, max_value=10, step=1, value=5)
    sb.on_change = lambda v: print("SpinBox value:", v)

Author: Your Name & PygameUI Contributors
License: MIT
"""

import pygame

from uinex.core.widget import Widget
from uinex.core.themes import ThemeManager

__all__ = ["SpinBox"]


class SpinBox(Widget):
    """
    A numeric input widget with increment and decrement buttons.

    Args:
        master (Widget or pygame.Surface): Parent widget or surface.
        min_value (int or float, optional): Minimum allowed value.
        max_value (int or float, optional): Maximum allowed value.
        step (int or float, optional): Step size for increment/decrement.
        value (int or float, optional): Initial value.
        width (int, optional): Width of the spinbox.
        height (int, optional): Height of the spinbox.
        font (pygame.font.Font, optional): Font for the value display.
        foreground (pygame.Color, optional): Text color.
        background (pygame.Color, optional): Background color.
        button_color (pygame.Color, optional): Color of the buttons.
        editable (bool, optional): Allow direct text editing.
        on_change (callable, optional): Callback when value changes.
        **kwargs: Additional widget options.

    Attributes:
        value (int or float): The current value.
        min_value (int or float): Minimum allowed value.
        max_value (int or float): Maximum allowed value.
        step (int or float): Step size for increment/decrement.
        editable (bool): Whether the value can be edited directly.
        on_change (callable): Callback for value change.
    """

    def __init__(
        self,
        master,
        min_value=0,
        max_value=100,
        step=1,
        value=0,
        width=100,
        height=32,
        font=None,
        foreground=(0, 0, 0),
        background=(255, 255, 255),
        button_color=(200, 200, 200),
        editable=True,
        on_change=None,
        **kwargs,
    ):
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.value = value
        self.editable = editable
        self.on_change = on_change

        self.font = font or pygame.font.SysFont(None, 20)
        self.foreground = foreground
        self.background = background
        self.button_color = button_color

        self._text = str(self.value)
        self._focused = False
        self._cursor_visible = True
        self._cursor_timer = 0
        self._blink_interval = 500  # ms
        self._cursor_pos = len(self._text)
        self._editing = False

        # Button rects
        self._button_width = height
        self._up_rect = pygame.Rect(
            width - self._button_width, 0, self._button_width, height // 2
        )
        self._down_rect = pygame.Rect(
            width - self._button_width, height // 2, self._button_width, height // 2
        )

        super().__init__(
            master,
            width=width,
            height=height,
            foreground=foreground,
            background=background,
            **kwargs,
        )

    def _perform_draw_(self, surface, *args, **kwargs):
        """Draw the spinbox, value, and buttons."""
        # Draw background
        # surface.fill(self.background)

        # Draw value text
        text_surf = self.font.render(self._text, True, self.foreground)
        text_rect = text_surf.get_rect()
        text_rect.centery = self._rect.height // 2
        text_rect.x = 8

        # Draw selection/cursor if focused and editable
        if self.editable and self._focused and self._editing:
            cursor_x = text_rect.x + self.font.size(self._text[: self._cursor_pos])[0]
            cursor_y = text_rect.y
            cursor_h = text_rect.height
            if self._cursor_visible:
                pygame.draw.line(
                    surface,
                    (0, 0, 0),
                    (cursor_x, cursor_y),
                    (cursor_x, cursor_y + cursor_h),
                    1,
                )

        surface.blit(text_surf, text_rect)

        # Draw up/down buttons
        pygame.draw.rect(surface, self.button_color, self._up_rect)
        pygame.draw.rect(surface, self.button_color, self._down_rect)
        # Draw up arrow
        pygame.draw.polygon(
            surface,
            (60, 60, 60),
            [
                (self._up_rect.centerx, self._up_rect.top + 6),
                (self._up_rect.left + 6, self._up_rect.bottom - 6),
                (self._up_rect.right - 6, self._up_rect.bottom - 6),
            ],
        )
        # Draw down arrow
        pygame.draw.polygon(
            surface,
            (60, 60, 60),
            [
                (self._down_rect.centerx, self._down_rect.bottom - 6),
                (self._down_rect.left + 6, self._down_rect.top + 6),
                (self._down_rect.right - 6, self._down_rect.top + 6),
            ],
        )

        # Draw border
        pygame.draw.rect(surface, (120, 120, 120), surface.get_rect(), 1)

    def _handle_event_(self, event, *args, **kwargs):
        """Handle mouse and keyboard events for spinbox."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            rel_pos = (event.pos[0] - self._rect.x, event.pos[1] - self._rect.y)
            if self._up_rect.collidepoint(rel_pos):
                self.increment()
            elif self._down_rect.collidepoint(rel_pos):
                self.decrement()
            elif self.editable and self._rect.collidepoint(event.pos):
                self._focused = True
                self._editing = True
                # Set cursor position based on click
                rel_x = rel_pos[0] - 8
                self._cursor_pos = self._get_cursor_from_x(rel_x)
            else:
                self._focused = False
                self._editing = False

        if not self._focused or not self.editable:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.increment()
            elif event.key == pygame.K_DOWN:
                self.decrement()
            elif event.key == pygame.K_RETURN:
                self._commit_text()
                self._editing = False
            elif event.key == pygame.K_ESCAPE:
                self._text = str(self.value)
                self._editing = False
            elif event.key == pygame.K_BACKSPACE:
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
            elif event.unicode and (
                event.unicode.isdigit()
                or (event.unicode == "." and "." not in self._text)
            ):
                self._text = (
                    self._text[: self._cursor_pos]
                    + event.unicode
                    + self._text[self._cursor_pos :]
                )
                self._cursor_pos += 1
            self._dirty = True

    def _perform_update_(self, delta, *args, **kwargs):
        """Update cursor blink."""
        if self._focused and self.editable and self._editing:
            self._cursor_timer += delta * 1000  # delta in seconds
            if self._cursor_timer >= self._blink_interval:
                self._cursor_visible = not self._cursor_visible
                self._cursor_timer = 0
                self._dirty = True
        else:
            self._cursor_visible = False

    def increment(self):
        """Increase the value by step, up to max_value."""
        new_value = self.value + self.step
        if new_value > self.max_value:
            new_value = self.max_value
        self.set_value(new_value)

    def decrement(self):
        """Decrease the value by step, down to min_value."""
        new_value = self.value - self.step
        if new_value < self.min_value:
            new_value = self.min_value
        self.set_value(new_value)

    def set_value(self, v):
        """Set the value, clamp to min/max, and update text."""
        try:
            v = type(self.value)(v)
        except Exception:
            v = self.min_value
        v = max(self.min_value, min(self.max_value, v))
        if v != self.value:
            self.value = v
            self._text = str(self.value)
            self._cursor_pos = len(self._text)
            if self.on_change:
                self.on_change(self.value)
            self._dirty = True

    def _commit_text(self):
        """Commit the text field to the value."""
        try:
            v = float(self._text) if "." in self._text else int(self._text)
        except Exception:
            v = self.value
        self.set_value(v)
        self._text = str(self.value)
        self._cursor_pos = len(self._text)

    def _get_cursor_from_x(self, x):
        """Get cursor position from x coordinate in the text field."""
        acc = 0
        for i, ch in enumerate(self._text):
            w = self.font.size(ch)[0]
            if acc + w // 2 > x:
                return i
            acc += w
        return len(self._text)

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
            if config == "step":
                return self.step
            return super().configure(config)
        if "value" in kwargs:
            self.set_value(kwargs["value"])
        if "min_value" in kwargs:
            self.min_value = kwargs["min_value"]
            self.set_value(self.value)
        if "max_value" in kwargs:
            self.max_value = kwargs["max_value"]
            self.set_value(self.value)
        if "step" in kwargs:
            self.step
