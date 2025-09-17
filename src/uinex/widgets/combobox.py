"""PygameUI ComboBox Widget

A ComboBox is a widget that combines a text field with a dropdown list of options.
It allows the user to select one item from a list or type a custom value (optional).
ComboBoxes are commonly used for forms, settings, and anywhere a compact selection
widget is needed.

Features:
    - Dropdown list of selectable items
    - Optional editable text field
    - Customizable font, colors, and size
    - Mouse and keyboard interaction
    - Callback for selection change

Example:
    cb = ComboBox(master, items=["One", "Two", "Three"], width=120)
    cb.on_select = lambda idx, value: print("Selected:", idx, value)

Author: Your Name & PygameUI Contributors
License: MIT
"""

import pygame

from uinex.core.widget import Widget
from uinex.core.themes import ThemeManager

__all__ = ["ComboBox"]


class ComboBox(Widget):
    """
    A dropdown selection widget with optional text entry.

    Args:
        master (Widget or pygame.Surface): Parent widget or surface.
        items (list, optional): List of items to display.
        width (int, optional): Width of the combobox.
        height (int, optional): Height of the combobox.
        font (pygame.font.Font, optional): Font for item text.
        foreground (pygame.Color, optional): Text color.
        background (pygame.Color, optional): Background color.
        select_color (pygame.Color, optional): Selected item background color.
        editable (bool, optional): Allow text entry. Default is False.
        on_select (callable, optional): Callback when selection changes.
        **kwargs: Additional widget options.

    Attributes:
        items (list): List of items.
        selected (int): Index of selected item.
        text (str): Current text (selected or entered).
        dropdown_open (bool): Whether the dropdown is open.
        on_select (callable): Callback for selection change.
    """

    def __init__(
        self,
        master,
        items=None,
        width=120,
        height=32,
        font=None,
        foreground=(0, 0, 0),
        background=(255, 255, 255),
        select_color=(200, 220, 255),
        editable=False,
        on_select=None,
        **kwargs,
    ):
        self.items = items or []
        self.selected = 0 if self.items else -1
        self.text = self.items[self.selected] if self.selected >= 0 else ""
        self.dropdown_open = False
        self.on_select = on_select
        self.editable = editable

        self.font = font or pygame.font.SysFont(None, 20)
        self.foreground = foreground
        self.background = background
        self.select_color = select_color

        self._cursor_visible = True
        self._cursor_timer = 0
        self._blink_interval = 500  # ms
        self._cursor_pos = len(self.text)
        self._editing = False

        super().__init__(
            master,
            width=width,
            height=height,
            foreground=foreground,
            background=background,
            **kwargs,
        )

    def _perform_draw_(self, surface, *args, **kwargs):
        """Draw the combobox, text, and dropdown list if open."""
        rect = surface.get_rect()
        # Draw background and border
        surface.fill(self.background)
        pygame.draw.rect(surface, (120, 120, 120), rect, 1)

        # Draw text or selected item
        text_surf = self.font.render(self.text, True, self.foreground)
        text_rect = text_surf.get_rect()
        text_rect.centery = rect.centery
        text_rect.x = 8
        surface.blit(text_surf, text_rect)

        # Draw cursor if editing
        if self.editable and self._editing and self._cursor_visible:
            cursor_x = text_rect.x + self.font.size(self.text[: self._cursor_pos])[0]
            cursor_y = text_rect.y
            cursor_h = text_rect.height
            pygame.draw.line(
                surface,
                (0, 0, 0),
                (cursor_x, cursor_y),
                (cursor_x, cursor_y + cursor_h),
                1,
            )

        # Draw dropdown arrow
        arrow_x = rect.right - 18
        arrow_y = rect.centery
        pygame.draw.polygon(
            surface,
            self.foreground,
            [
                (arrow_x, arrow_y - 4),
                (arrow_x + 8, arrow_y - 4),
                (arrow_x + 4, arrow_y + 4),
            ],
        )

        # Draw dropdown list if open
        if self.dropdown_open and self.items:
            menu_width = rect.width
            menu_height = rect.height * len(self.items)
            menu_rect = pygame.Rect(rect.left, rect.bottom, menu_width, menu_height)
            pygame.draw.rect(surface, self.background, menu_rect)
            pygame.draw.rect(surface, (120, 120, 120), menu_rect, 1)
            for i, item in enumerate(self.items):
                item_rect = pygame.Rect(
                    menu_rect.left,
                    menu_rect.top + i * rect.height,
                    menu_rect.width,
                    rect.height,
                )
                if i == self.selected:
                    pygame.draw.rect(surface, self.select_color, item_rect)
                item_surf = self.font.render(str(item), True, self.foreground)
                surface.blit(
                    item_surf,
                    (
                        item_rect.left + 8,
                        item_rect.centery - item_surf.get_height() // 2,
                    ),
                )

    def _handle_event_(self, event, *args, **kwargs):
        """Handle mouse and keyboard events for ComboBox."""
        rect = self._rect
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = (event.pos[0] - rect.x, event.pos[1] - rect.y)
            if rect.collidepoint(event.pos):
                if self.editable:
                    self._editing = True
                self.dropdown_open = not self.dropdown_open
                self._dirty = True
            elif self.dropdown_open:
                menu_rect = pygame.Rect(
                    rect.left,
                    rect.bottom,
                    rect.width,
                    rect.height * len(self.items),
                )
                if menu_rect.collidepoint(event.pos[0] - rect.x, event.pos[1] - rect.y):
                    idx = (event.pos[1] - rect.y - rect.height) // rect.height
                    if 0 <= idx < len(self.items):
                        self.selected = idx
                        self.text = self.items[idx]
                        self.dropdown_open = False
                        self._editing = False
                        if self.on_select:
                            self.on_select(idx, self.text)
                        self._dirty = True
                else:
                    self.dropdown_open = False
                    self._editing = False
                    self._dirty = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.dropdown_open = False
            self._editing = False
            self._dirty = True

        if self.editable and self._editing:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self._editing = False
                    self.dropdown_open = False
                    if self.on_select:
                        self.on_select(self.selected, self.text)
                elif event.key == pygame.K_ESCAPE:
                    self._editing = False
                    self.dropdown_open = False
                elif event.key == pygame.K_BACKSPACE:
                    if self._cursor_pos > 0:
                        self.text = (
                            self.text[: self._cursor_pos - 1]
                            + self.text[self._cursor_pos :]
                        )
                        self._cursor_pos -= 1
                elif event.key == pygame.K_DELETE:
                    if self._cursor_pos < len(self.text):
                        self.text = (
                            self.text[: self._cursor_pos]
                            + self.text[self._cursor_pos + 1 :]
                        )
                elif event.key == pygame.K_LEFT:
                    if self._cursor_pos > 0:
                        self._cursor_pos -= 1
                elif event.key == pygame.K_RIGHT:
                    if self._cursor_pos < len(self.text):
                        self._cursor_pos += 1
                elif event.unicode:
                    self.text = (
                        self.text[: self._cursor_pos]
                        + event.unicode
                        + self.text[self._cursor_pos :]
                    )
                    self._cursor_pos += 1
                self._dirty = True
        elif self.dropdown_open and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                if self.selected < len(self.items) - 1:
                    self.selected += 1
                    self.text = self.items[self.selected]
                    self._dirty = True
            elif event.key == pygame.K_UP:
                if self.selected > 0:
                    self.selected -= 1
                    self.text = self.items[self.selected]
                    self._dirty = True
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self.dropdown_open = False
                self._editing = False
                if self.on_select:
                    self.on_select(self.selected, self.text)
                self._dirty = True
            elif event.key == pygame.K_ESCAPE:
                self.dropdown_open = False
                self._editing = False
                self._dirty = True

    def _perform_update_(self, delta, *args, **kwargs):
        """Update cursor blink if editing."""
        if self.editable and self._editing:
            self._cursor_timer += delta * 1000
            if self._cursor_timer >= self._blink_interval:
                self._cursor_visible = not self._cursor_visible
                self._cursor_timer = 0
                self._dirty = True
        else:
            self._cursor_visible = False

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
            if config == "items":
                return self.items
            if config == "selected":
                return self.selected
            if config == "text":
                return self.text
            return super().configure(config)
        if "items" in kwargs:
            self.items = kwargs["items"]
            self.selected = 0 if self.items else -1
            self.text = self.items[self.selected] if self.selected >= 0 else ""
            self._dirty = True
        if "selected" in kwargs:
            self.selected = kwargs["selected"]
            self.text = (
                self.items[self.selected]
                if 0 <= self.selected < len(self.items)
                else ""
            )
            self._dirty = True
        if "text" in kwargs:
            self.text = kwargs["text"]
            self._dirty = True
        return
