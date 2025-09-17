"""PygameUI RadioButton Widget

A RadioButton is a circular button that can be selected or deselected, typically used in groups
where only one button can be selected at a time. This widget provides a customizable radio button
with label, group management, and event handling.

Features:
    - Customizable size, colors, and label
    - Grouping support (only one button in a group can be selected)
    - Mouse interaction (select on click)
    - Callback support for selection changes

Example:
    rb1 = RadioButton(master, text="Option 1", group="group1", checked=True)
    rb2 = RadioButton(master, text="Option 2", group="group1")
    rb1.on_change = lambda checked: print("rb1 checked:", checked)

Author: Your Name & PygameUI Contributors
License: MIT
"""

import pygame

from uinex.core.widget import Widget
from uinex.core.themes import ThemeManager

__all__ = ["RadioButton"]

# Internal registry for radio button groups
_RADIO_GROUPS = {}


class RadioButton(Widget):
    """
    A circular radio button widget with label and group support.

    Args:
        master (Widget or pygame.Surface): Parent widget or surface.
        text (str): Label text for the radio button.
        group (str, optional): Group name for mutual exclusivity.
        checked (bool, optional): Initial checked state.
        radius (int, optional): Radius of the radio button circle.
        foreground (pygame.Color, optional): Text color.
        background (pygame.Color, optional): Background color.
        circle_color (pygame.Color, optional): Color of the radio circle.
        check_color (pygame.Color, optional): Color of the inner dot when checked.
        font (pygame.font.Font, optional): Font for the label.
        on_change (callable, optional): Callback when checked state changes.
        **kwargs: Additional widget options.

    Attributes:
        checked (bool): Whether the radio button is selected.
        text (str): The label text.
        group (str): The group name.
        on_change (callable): Callback for checked state changes.
    """

    def __init__(
        self,
        master,
        text="",
        group=None,
        checked=False,
        radius=12,
        foreground=(0, 0, 0),
        background=(255, 255, 255, 0),
        circle_color=(80, 80, 80),
        check_color=(30, 144, 255),
        font=None,
        on_change=None,
        **kwargs,
    ):
        self.text = text
        self.group = group
        self.checked = checked
        self.radius = radius
        self.circle_color = circle_color
        self.check_color = check_color
        self.on_change = on_change
        self.font = font or pygame.font.SysFont(None, 20)
        self._label_surface = self.font.render(self.text, True, foreground)
        width = 2 * radius + 8 + self._label_surface.get_width()
        height = max(2 * radius, self._label_surface.get_height()) + 4
        super().__init__(
            master,
            width=width,
            height=height,
            foreground=foreground,
            background=background,
            **kwargs,
        )

        # Register in group
        if group:
            _RADIO_GROUPS.setdefault(group, []).append(self)

    def _perform_draw_(self, surface, *args, **kwargs):
        """Draw the radio button and label."""
        # Draw background
        if self._background:
            surface.fill(self._background)

        # Draw radio circle
        center = (self.radius + 4, self._rect.centery)
        pygame.draw.circle(surface, self.circle_color, center, self.radius, 2)

        # Draw checked dot
        if self.checked:
            pygame.draw.circle(surface, self.check_color, center, self.radius - 5)

        # Draw label
        label_pos = (
            2 * self.radius + 8,
            (self._rect.height - self._label_surface.get_height()) // 2,
        )
        surface.blit(self._label_surface, label_pos)

    def _handle_event_(self, event, *args, **kwargs):
        """Handle mouse click to toggle checked state."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._rect.collidepoint(event.pos):
                if not self.checked:
                    self.select()

    def _perform_update_(self, delta, *args, **kwargs):
        """Update logic (not used for static radio button)."""

    def select(self):
        """Select this radio button and unselect others in the group."""
        if self.group:
            for rb in _RADIO_GROUPS.get(self.group, []):
                if rb is not self and rb.checked:
                    rb.checked = False
                    if rb.on_change:
                        rb.on_change(False)
        if not self.checked:
            self.checked = True
            if self.on_change:
                self.on_change(True)
        self._dirty = True

    def deselect(self):
        """Deselect this radio button."""
        if self.checked:
            self.checked = False
            if self.on_change:
                self.on_change(False)
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
            if config == "checked":
                return self.checked
            if config == "text":
                return self.text
            if config == "group":
                return self.group
            return super().configure(config)
        if "checked" in kwargs:
            if kwargs["checked"]:
                self.select()
            else:
                self.deselect()
        if "text" in kwargs:
            self.text = kwargs["text"]
            self._label_surface = self.font.render(self.text, True, self._foreground)
        if "group" in kwargs:
            old_group = self.group
            self.group = kwargs["group"]
            if old_group and self in _RADIO_GROUPS.get(old_group, []):
                _RADIO_GROUPS[old_group].remove(self)
            if self.group:
                _RADIO_GROUPS.setdefault(self.group, []).append(self)
