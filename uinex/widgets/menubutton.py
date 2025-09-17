"""PygameUI MenuButton Widget

A MenuButton is a button that displays a dropdown menu when clicked. It is commonly used
for toolbars, context menus, and navigation bars. The MenuButton supports custom labels,
menu items, callbacks, and integrates with the PygameUI event and layout system.

Features:
    - Displays a dropdown menu on click
    - Customizable label, font, and colors
    - Supports menu item callbacks
    - Keyboard and mouse interaction
    - Integrates with layout managers

Example:
    mb = MenuButton(master, text="File", menu_items=[("Open", on_open), ("Save", on_save)])
    mb.on_select = lambda label: print("Selected:", label)

Author: Your Name & PygameUI Contributors
License: MIT
"""

import pygame

from uinex.core.widget import Widget
from uinex.core.themes import ThemeManager

__all__ = ["MenuButton"]


class MenuButton(Widget):
    """
    A button that displays a dropdown menu when clicked.

    Args:
        master (Widget or pygame.Surface): Parent widget or surface.
        text (str): Button label.
        menu_items (list): List of (label, callback) tuples for menu items.
        width (int, optional): Width of the button.
        height (int, optional): Height of the button.
        font (pygame.font.Font, optional): Font for the label.
        foreground (pygame.Color, optional): Text color.
        background (pygame.Color, optional): Background color.
        menu_background (pygame.Color, optional): Menu background color.
        menu_foreground (pygame.Color, optional): Menu text color.
        on_select (callable, optional): Callback when a menu item is selected.
        **kwargs: Additional widget options.

    Attributes:
        text (str): Button label.
        menu_items (list): List of (label, callback) tuples.
        menu_open (bool): Whether the menu is open.
        selected_index (int): Index of the currently hovered menu item.
        on_select (callable): Callback for menu item selection.
    """

    def __init__(
        self,
        master,
        text="Menu",
        menu_items=None,
        width=100,
        height=32,
        font=None,
        foreground=(0, 0, 0),
        background=(230, 230, 230),
        menu_background=(255, 255, 255),
        menu_foreground=(0, 0, 0),
        on_select=None,
        **kwargs,
    ):
        self.text = text
        self.menu_items = menu_items or []
        self.menu_open = False
        self.selected_index = -1
        self.on_select = on_select

        self.font = font or pygame.font.SysFont(None, 20)
        self.foreground = foreground
        self.background = background
        self.menu_background = menu_background
        self.menu_foreground = menu_foreground

        super().__init__(
            master,
            width=width,
            height=height,
            foreground=foreground,
            background=background,
            **kwargs,
        )

    def _perform_draw_(self, surface, *args, **kwargs):
        """Draw the button and dropdown menu if open."""
        rect = surface.get_rect()
        # Draw button background
        surface.fill(self.background)
        # Draw button border
        pygame.draw.rect(surface, (120, 120, 120), rect, 1)
        # Draw label
        label_surf = self.font.render(self.text, True, self.foreground)
        label_rect = label_surf.get_rect(center=rect.center)
        surface.blit(label_surf, label_rect)
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
        # Draw menu if open
        if self.menu_open and self.menu_items:
            menu_width = rect.width
            menu_height = rect.height * len(self.menu_items)
            menu_rect = pygame.Rect(rect.left, rect.bottom, menu_width, menu_height)
            pygame.draw.rect(surface, self.menu_background, menu_rect)
            pygame.draw.rect(surface, (120, 120, 120), menu_rect, 1)
            for i, (label, _) in enumerate(self.menu_items):
                item_rect = pygame.Rect(
                    menu_rect.left,
                    menu_rect.top + i * rect.height,
                    menu_rect.width,
                    rect.height,
                )
                if i == self.selected_index:
                    pygame.draw.rect(surface, (200, 220, 255), item_rect)
                item_surf = self.font.render(str(label), True, self.menu_foreground)
                surface.blit(
                    item_surf,
                    (
                        item_rect.left + 8,
                        item_rect.centery - item_surf.get_height() // 2,
                    ),
                )

    def _handle_event_(self, event, *args, **kwargs):
        """Handle mouse and keyboard events for menu interaction."""
        rect = self._rect
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse = (event.pos[0] - rect.x, event.pos[1] - rect.y)
            if rect.collidepoint(event.pos):
                self.menu_open = not self.menu_open
                self.selected_index = -1
                self._dirty = True
            elif self.menu_open:
                menu_rect = pygame.Rect(
                    rect.left,
                    rect.bottom,
                    rect.width,
                    rect.height * len(self.menu_items),
                )
                if menu_rect.collidepoint(event.pos[0] - rect.x, event.pos[1] - rect.y):
                    idx = (event.pos[1] - rect.y - rect.height) // rect.height
                    if 0 <= idx < len(self.menu_items):
                        self.selected_index = idx
                        self._select_menu_item(idx)
                else:
                    self.menu_open = False
                    self.selected_index = -1
                    self._dirty = True
        elif event.type == pygame.MOUSEMOTION and self.menu_open:
            menu_rect = pygame.Rect(
                rect.left,
                rect.bottom,
                rect.width,
                rect.height * len(self.menu_items),
            )
            mx, my = event.pos[0] - rect.x, event.pos[1] - rect.y
            if menu_rect.collidepoint(mx, my):
                idx = (my - rect.height) // rect.height
                if 0 <= idx < len(self.menu_items):
                    if self.selected_index != idx:
                        self.selected_index = idx
                        self._dirty = True
                else:
                    if self.selected_index != -1:
                        self.selected_index = -1
                        self._dirty = True
            else:
                if self.selected_index != -1:
                    self.selected_index = -1
                    self._dirty = True
        elif event.type == pygame.KEYDOWN and self.menu_open:
            if event.key == pygame.K_DOWN:
                if self.selected_index < len(self.menu_items) - 1:
                    self.selected_index += 1
                    self._dirty = True
            elif event.key == pygame.K_UP:
                if self.selected_index > 0:
                    self.selected_index -= 1
                    self._dirty = True
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if 0 <= self.selected_index < len(self.menu_items):
                    self._select_menu_item(self.selected_index)
            elif event.key == pygame.K_ESCAPE:
                self.menu_open = False
                self.selected_index = -1
                self._dirty = True

    def _perform_update_(self, delta, *args, **kwargs):
        """Update logic for MenuButton (not used)."""
        pass

    def _select_menu_item(self, idx):
        """Select a menu item and trigger callback."""
        self.menu_open = False
        label, callback = self.menu_items[idx]
        if self.on_select:
            self.on_select(label)
        if callable(callback):
            callback()
        self.selected_index = -1
        self._dirty = True

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
            if config == "menu_items":
                return self.menu_items
            if config == "menu_open":
                return self.menu_open
            return super().configure(config)
        if "text" in kwargs:
            self.text = kwargs["text"]
        if "menu_items" in kwargs:
            self.menu_items = kwargs["menu_items"]
