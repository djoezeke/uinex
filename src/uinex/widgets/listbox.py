"""PygameUI ListBox Widget

A ListBox is a widget that displays a list of items, allowing the user to select one or more items.
It supports keyboard and mouse navigation, customizable appearance, and callbacks for selection changes.

Features:
    - Single or multiple selection modes
    - Customizable font, colors, and item height
    - Scroll support for long lists
    - Mouse and keyboard interaction
    - Callback for selection change

Example:
    lb = ListBox(master, items=["Apple", "Banana", "Cherry"])
    lb.on_select = lambda idx, value: print("Selected:", idx, value)

Author: Your Name & PygameUI Contributors
License: MIT
"""

import pygame

from uinex.core.widget import Widget
from uinex.core.themes import ThemeManager

__all__ = ["ListBox"]


class ListBox(Widget):
    """
    A widget for displaying and selecting from a list of items.

    Args:
        master (Widget or pygame.Surface): Parent widget or surface.
        items (list, optional): List of items to display.
        width (int, optional): Width of the listbox.
        height (int, optional): Height of the listbox.
        font (pygame.font.Font, optional): Font for item text.
        foreground (pygame.Color, optional): Text color.
        background (pygame.Color, optional): Background color.
        select_color (pygame.Color, optional): Selected item background color.
        item_height (int, optional): Height of each item row.
        multi (bool, optional): Enable multiple selection.
        on_select (callable, optional): Callback when selection changes.
        **kwargs: Additional widget options.

    Attributes:
        items (list): List of items.
        selected (list): List of selected indices.
        on_select (callable): Callback for selection change.
    """

    def __init__(
        self,
        master,
        items=None,
        width=120,
        height=160,
        font=None,
        foreground=(0, 0, 0),
        background=(255, 255, 255),
        select_color=(200, 220, 255),
        item_height=24,
        multi=False,
        on_select=None,
        **kwargs,
    ):
        self.items = items or []
        self.selected = []
        self.multi = multi
        self.on_select = on_select

        self.font = font or pygame.font.SysFont(None, 20)
        self.foreground = foreground
        self.background = background
        self.select_color = select_color
        self.item_height = item_height

        self._scroll = 0  # For future scroll support

        super().__init__(
            master,
            width=width,
            height=height,
            foreground=foreground,
            background=background,
            **kwargs,
        )

    def _perform_draw_(self, surface, *args, **kwargs):
        """Draw the listbox and its items."""
        surface.fill(self.background)
        rect = surface.get_rect()
        visible_count = rect.height // self.item_height
        start = self._scroll
        end = min(start + visible_count, len(self.items))
        for idx in range(start, end):
            y = (idx - start) * self.item_height
            item_rect = pygame.Rect(0, y, rect.width, self.item_height)
            if idx in self.selected:
                pygame.draw.rect(surface, self.select_color, item_rect)
            item_surf = self.font.render(str(self.items[idx]), True, self.foreground)
            surface.blit(
                item_surf, (8, y + (self.item_height - item_surf.get_height()) // 2)
            )
            # Optional: draw separator line
            pygame.draw.line(
                surface,
                (220, 220, 220),
                (0, y + self.item_height - 1),
                (rect.width, y + self.item_height - 1),
            )

    def _handle_event_(self, event, *args, **kwargs):
        """Handle mouse and keyboard events for selection."""
        rect = self._rect
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos[0] - rect.x, event.pos[1] - rect.y
            idx = self._scroll + my // self.item_height
            if 0 <= idx < len(self.items):
                if self.multi:
                    if idx in self.selected:
                        self.selected.remove(idx)
                    else:
                        self.selected.append(idx)
                else:
                    self.selected = [idx]
                if self.on_select:
                    self.on_select(idx, self.items[idx])
                self._dirty = True
        elif event.type == pygame.KEYDOWN:
            if not self.items:
                return
            if not self.selected:
                self.selected = [0]
                self._dirty = True
                return
            idx = self.selected[-1]
            if event.key == pygame.K_UP:
                if idx > 0:
                    idx -= 1
                    self.selected = [idx]
                    if self.on_select:
                        self.on_select(idx, self.items[idx])
                    self._dirty = True
            elif event.key == pygame.K_DOWN:
                if idx < len(self.items) - 1:
                    idx += 1
                    self.selected = [idx]
                    if self.on_select:
                        self.on_select(idx, self.items[idx])
                    self._dirty = True

    def _perform_update_(self, delta, *args, **kwargs):
        """Update logic for ListBox (not used)."""
        pass

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
            return super().configure(config)
        if "items" in kwargs:
            self.items = kwargs["items"]
            self.selected = []
            self._dirty = True
        if "selected" in kwargs:
            self.selected = kwargs["selected"]
            self._dirty = True
        return super().configure(**kwargs)
